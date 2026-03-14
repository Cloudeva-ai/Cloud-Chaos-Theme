"""
database.py — Robust SQLAlchemy ORM + CRUD layer for Cloud Chaos.

Schema
──────
players         — one row per unique registrant
game_sessions   — one row per completed game attempt (FK → players)
selections      — one row per pain·column selection (FK → game_sessions)
events          — audit / analytics log for every meaningful action

All timestamps are stored as UTC ISO-8601 strings for portability.
"""

from __future__ import annotations

import json
import os
import re
import threading
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    event,
    select,
    text,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

# ─────────────────────────────────────────────────────────────
#  ENGINE SETUP
# ─────────────────────────────────────────────────────────────
DB_PATH = Path(__file__).parent / "cloud_chaos.db"
REGISTRATION_BACKUP_PATH = Path(__file__).parent / "player_registrations_backup.xlsx"
REGISTRATION_BACKUP_CSV_PATH = Path(__file__).parent / "player_registrations_backup.csv"
REGISTRATION_BACKUP_DIR = Path(__file__).parent / "registration_backups"
BACKUP_LOCK = threading.Lock()
ENGINE  = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False, "timeout": 30},
    echo=False,
)

# Enable WAL mode and foreign keys on every new connection
@event.listens_for(ENGINE, "connect")
def _set_sqlite_pragmas(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA synchronous=FULL;")
    cursor.execute("PRAGMA busy_timeout=30000;")
    cursor.close()

SessionFactory = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, expire_on_commit=False)


# ─────────────────────────────────────────────────────────────
#  ORM MODELS
# ─────────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Player(Base):
    """
    One row per unique player (identified by email).
    A player can have many game sessions.
    """
    __tablename__ = "players"
    __table_args__ = (
        UniqueConstraint("email", name="uq_player_email"),
        CheckConstraint("length(trim(name)) > 0", name="ck_player_name_non_empty"),
        CheckConstraint("length(trim(company)) > 0", name="ck_player_company_non_empty"),
    )

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(120), nullable=False)
    company     = Column(String(120), nullable=False)
    email       = Column(String(200), nullable=False)
    created_at  = Column(DateTime(timezone=True), default=_now, nullable=False)
    last_seen   = Column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)
    total_plays = Column(Integer, default=0, nullable=False)
    best_score  = Column(Integer, default=0, nullable=False)
    best_time   = Column(Integer, nullable=True)   # seconds for the best-score run

    sessions = relationship("GameSession", back_populates="player",
                            cascade="all, delete-orphan", lazy="select")
    events   = relationship("Event", back_populates="player",
                            cascade="all, delete-orphan", lazy="select")

    def __repr__(self):
        return f"<Player id={self.id} name={self.name!r} email={self.email!r}>"


class GameSession(Base):
    """
    One row per completed (or timed-out) game attempt.
    Stores aggregate result + metadata.
    """
    __tablename__ = "game_sessions"
    __table_args__ = (
        Index("ix_session_player", "player_id"),
        Index("ix_session_score_time", "score", "time_used"),
        CheckConstraint("score >= 0", name="ck_session_score_non_negative"),
        CheckConstraint("time_used >= 0", name="ck_session_time_non_negative"),
    )

    id           = Column(Integer, primary_key=True, autoincrement=True)
    player_id    = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    score        = Column(Integer,  nullable=False, default=0)
    time_used    = Column(Integer,  nullable=False, default=90)   # seconds
    completed_at = Column(DateTime(timezone=True), default=_now,  nullable=False)
    timed_out    = Column(Boolean,  nullable=False, default=False)
    # Derived flags stored for fast query
    is_perfect   = Column(Boolean,  nullable=False, default=False)

    player     = relationship("Player",    back_populates="sessions")
    selections = relationship("Selection", back_populates="session",
                              cascade="all, delete-orphan", lazy="select")

    def __repr__(self):
        return f"<GameSession id={self.id} player_id={self.player_id} score={self.score}>"


class Selection(Base):
    """
    One row per pain point per session — detailed answer tracking.
    Stores both what the player picked and whether it was correct.
    """
    __tablename__ = "selections"
    __table_args__ = (
        Index("ix_selection_session", "session_id"),
        UniqueConstraint("session_id", "pain_idx", name="uq_selection_per_pain"),
        CheckConstraint("pain_idx >= 0", name="ck_selection_pain_non_negative"),
    )

    id               = Column(Integer, primary_key=True, autoincrement=True)
    session_id       = Column(Integer, ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    pain_idx         = Column(Integer, nullable=False)  # 0-4
    owner_orig_idx   = Column(Integer, nullable=True)   # which owner was chosen (orig index)
    impact_orig_idx  = Column(Integer, nullable=True)   # which impact was chosen (orig index)
    owner_correct    = Column(Boolean, nullable=False, default=False)
    impact_correct   = Column(Boolean, nullable=False, default=False)
    both_correct     = Column(Boolean, nullable=False, default=False)

    session = relationship("GameSession", back_populates="selections")

    def __repr__(self):
        return (f"<Selection session={self.session_id} pain={self.pain_idx} "
                f"ok={self.both_correct}>")


class Event(Base):
    """
    Lightweight audit / analytics log.
    Records every significant player action with a JSON-friendly payload.
    """
    __tablename__ = "events"
    __table_args__ = (
        Index("ix_event_player", "player_id"),
        Index("ix_event_type",   "event_type"),
    )

    id          = Column(Integer, primary_key=True, autoincrement=True)
    player_id   = Column(Integer, ForeignKey("players.id", ondelete="SET NULL"), nullable=True)
    event_type  = Column(String(60),  nullable=False)   # e.g. "game_start", "game_submit"
    payload     = Column(Text,        nullable=True)     # JSON string for extra context
    created_at  = Column(DateTime(timezone=True), default=_now, nullable=False)

    player = relationship("Player", back_populates="events")

    def __repr__(self):
        return f"<Event id={self.id} type={self.event_type!r} player={self.player_id}>"


# ─────────────────────────────────────────────────────────────
#  INITIALISATION
# ─────────────────────────────────────────────────────────────
def init_db() -> None:
    """Create all tables if they don't exist. Safe to call on every startup."""
    Base.metadata.create_all(ENGINE)
    _export_registration_backup()


def _invalidate_read_caches() -> None:
    for cache_name in (
        "_get_leaderboard_cached",
        "_get_full_leaderboard_cached",
        "_get_player_history_cached",
        "_get_session_breakdown_cached",
        "_get_stats_cached",
        "_get_perfect_score_players_cached",
    ):
        cache_fn = globals().get(cache_name)
        if cache_fn is not None and hasattr(cache_fn, "cache_clear"):
            cache_fn.cache_clear()


# ─────────────────────────────────────────────────────────────
#  CRUD HELPERS
# ─────────────────────────────────────────────────────────────
def _validate_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def _normalize_registration_fields(name: str, company: str, email: str) -> tuple[str, str, str]:
    clean_name = " ".join(name.strip().split())
    clean_company = " ".join(company.strip().split())
    clean_email = email.strip().lower()

    if not clean_name or not clean_company or not clean_email:
        raise ValueError("Name, company, and email are all required.")
    if len(clean_name) > 120 or len(clean_company) > 120:
        raise ValueError("Name and company must be 120 characters or fewer.")
    if len(clean_email) > 200:
        raise ValueError("Email must be 200 characters or fewer.")
    if not _validate_email(clean_email):
        raise ValueError(f"Invalid email address: {email!r}")
    return clean_name, clean_company, clean_email


def _validate_event_payload(payload: str) -> str:
    clean_payload = payload.strip()
    if not clean_payload:
        return ""
    try:
        json.loads(clean_payload)
    except json.JSONDecodeError as exc:
        raise ValueError("Event payload must be valid JSON.") from exc
    return clean_payload


def _export_registration_backup() -> None:
    """
    Export the registration table to an Excel workbook atomically.
    This gives the event team a non-database backup they can open directly.
    """
    with SessionFactory() as db:
        rows = db.execute(text("""
            SELECT
                id,
                name,
                company,
                email,
                created_at,
                last_seen,
                total_plays,
                best_score,
                best_time
            FROM players
            ORDER BY created_at ASC, id ASC
        """)).mappings().all()

    df = pd.DataFrame([dict(row) for row in rows])
    if df.empty:
        df = pd.DataFrame(columns=[
            "id", "name", "company", "email", "created_at",
            "last_seen", "total_plays", "best_score", "best_time",
        ])

    temp_path = REGISTRATION_BACKUP_PATH.with_suffix(".tmp.xlsx")
    temp_csv_path = REGISTRATION_BACKUP_CSV_PATH.with_suffix(".tmp.csv")
    snapshot_stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    snapshot_excel_path = REGISTRATION_BACKUP_DIR / f"player_registrations_{snapshot_stamp}.xlsx"
    snapshot_csv_path = REGISTRATION_BACKUP_DIR / f"player_registrations_{snapshot_stamp}.csv"
    with BACKUP_LOCK:
        REGISTRATION_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        df.to_excel(temp_path, index=False, sheet_name="registrations")
        df.to_csv(temp_csv_path, index=False)
        os.replace(temp_path, REGISTRATION_BACKUP_PATH)
        os.replace(temp_csv_path, REGISTRATION_BACKUP_CSV_PATH)
        df.to_excel(snapshot_excel_path, index=False, sheet_name="registrations")
        df.to_csv(snapshot_csv_path, index=False)


def upsert_player(name: str, company: str, email: str) -> tuple[Player, bool]:
    """
    Insert a new player or update last_seen + name/company if the email already
    exists.  Returns (player, is_new_player).
    """
    clean_name, clean_company, clean_email = _normalize_registration_fields(name, company, email)

    with SessionFactory() as db:
        player = db.scalar(select(Player).where(Player.email == clean_email))
        is_new = player is None

        if is_new:
            player = Player(name=clean_name, company=clean_company, email=clean_email)
            db.add(player)
        else:
            player.name = clean_name
            player.company = clean_company
            player.last_seen = _now()

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            player = db.scalar(select(Player).where(Player.email == clean_email))
            if player is None:
                raise
            player.name = clean_name
            player.company = clean_company
            player.last_seen = _now()
            db.commit()
            is_new = False

        _export_registration_backup()
        _invalidate_read_caches()
        return player, is_new


def log_event(player_id: Optional[int], event_type: str, payload: str = "") -> None:
    """Append a lightweight analytics event."""
    event_name = event_type.strip()
    if not event_name:
        raise ValueError("Event type is required.")
    if len(event_name) > 60:
        raise ValueError("Event type must be 60 characters or fewer.")
    clean_payload = _validate_event_payload(payload)

    with SessionFactory() as db:
        db.add(Event(player_id=player_id, event_type=event_name, payload=clean_payload))
        db.commit()
    _invalidate_read_caches()


def save_game_session(
    player_id:  int,
    score:      int,
    time_used:  int,
    timed_out:  bool,
    selections: dict[int, dict[str, Optional[int]]],
) -> GameSession:
    """
    Persist a completed game session with per-pain selections.
    Also updates the player's aggregate stats (total_plays, best_score, best_time).

    `selections` format:
        { pain_idx: {"owner": orig_idx | None, "impact": orig_idx | None} }
    """
    if score < 0:
        raise ValueError("Score cannot be negative.")
    if time_used < 0:
        raise ValueError("Time used cannot be negative.")
    if not selections:
        raise ValueError("Selections are required.")
    for pain_idx, selection in selections.items():
        if pain_idx < 0:
            raise ValueError("Pain index cannot be negative.")
        if not isinstance(selection, dict):
            raise ValueError("Each selection must be a dictionary.")
        if "owner" not in selection or "impact" not in selection:
            raise ValueError("Each selection must include owner and impact keys.")

    with SessionFactory() as db:
        player = db.get(Player, player_id)
        if player is None:
            raise ValueError(f"Unknown player id: {player_id}")

        session = GameSession(
            player_id=player_id,
            score=score,
            time_used=time_used,
            timed_out=timed_out,
            is_perfect=(score == 5),
        )
        db.add(session)
        db.flush()  # get session.id before inserting children

        for pain_idx, sel in selections.items():
            owner_pick   = sel.get("owner")
            impact_pick  = sel.get("impact")
            owner_ok     = owner_pick  == pain_idx
            impact_ok    = impact_pick == pain_idx
            db.add(Selection(
                session_id      = session.id,
                pain_idx        = pain_idx,
                owner_orig_idx  = owner_pick,
                impact_orig_idx = impact_pick,
                owner_correct   = owner_ok,
                impact_correct  = impact_ok,
                both_correct    = owner_ok and impact_ok,
            ))

        # Update player aggregate stats
        player.total_plays += 1
        player.last_seen = _now()
        if score > player.best_score or (
            score == player.best_score and
            (player.best_time is None or time_used < player.best_time)
        ):
            player.best_score = score
            player.best_time = time_used

        db.commit()
        _invalidate_read_caches()
        return session


# ─────────────────────────────────────────────────────────────
#  READ / QUERY HELPERS
# ─────────────────────────────────────────────────────────────
def get_leaderboard(limit: int = 20) -> list[dict[str, Any]]:
    """
    Return top `limit` unique-player best sessions, sorted by:
        1. score  DESC
        2. time   ASC  (faster is better)
        3. completed_at ASC  (earliest winner wins tiebreaker)
    One row per player (their personal best run only).
    """
    return [dict(row) for row in _get_leaderboard_cached(limit)]


@lru_cache(maxsize=16)
def _get_leaderboard_cached(limit: int) -> tuple[tuple[tuple[str, Any], ...], ...]:
    with SessionFactory() as db:
        rows = db.execute(text("""
            WITH ranked AS (
                SELECT
                    gs.id          AS session_id,
                    p.name         AS name,
                    p.company      AS company,
                    gs.score       AS score,
                    gs.time_used   AS time_used,
                    gs.is_perfect  AS is_perfect,
                    gs.completed_at AS completed_at,
                    p.total_plays  AS total_plays,
                    ROW_NUMBER() OVER (
                        PARTITION BY p.id
                        ORDER BY gs.score DESC, gs.time_used ASC, gs.completed_at ASC
                    ) AS rn
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
            )
            SELECT name, company, score, time_used, is_perfect,
                   total_plays, completed_at
            FROM ranked
            WHERE rn = 1
            ORDER BY score DESC, time_used ASC, completed_at ASC
            LIMIT :limit
        """), {"limit": limit}).mappings().all()
        return tuple(tuple(dict(r).items()) for r in rows)


def get_full_leaderboard(limit: int = 100) -> list[dict[str, Any]]:
    """All sessions (not de-duplicated by player) — useful for admin view."""
    with SessionFactory() as db:
        rows = db.execute(text("""
            SELECT
                p.name, p.company, p.email,
                gs.score, gs.time_used, gs.is_perfect,
                gs.timed_out, gs.completed_at,
                gs.id AS session_id
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC, gs.time_used ASC, gs.completed_at ASC
            LIMIT :limit
        """), {"limit": limit}).mappings().all()
        return [dict(r) for r in rows]


def get_player_history(email: str) -> list[dict[str, Any]]:
    """All sessions for a specific player, newest first."""
    normalized_email = email.strip().lower()
    return [dict(row) for row in _get_player_history_cached(normalized_email)]


@lru_cache(maxsize=64)
def _get_player_history_cached(email: str) -> tuple[tuple[tuple[str, Any], ...], ...]:
    with SessionFactory() as db:
        rows = db.execute(text("""
            SELECT
                gs.score, gs.time_used, gs.is_perfect,
                gs.timed_out, gs.completed_at, gs.id AS session_id
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            WHERE LOWER(p.email) = :email
            ORDER BY gs.completed_at DESC
        """), {"email": email}).mappings().all()
        return tuple(tuple(dict(r).items()) for r in rows)


def get_session_breakdown(session_id: int) -> list[dict[str, Any]]:
    """Per-pain selection detail for a given session."""
    return [dict(row) for row in _get_session_breakdown_cached(session_id)]


@lru_cache(maxsize=128)
def _get_session_breakdown_cached(session_id: int) -> tuple[tuple[tuple[str, Any], ...], ...]:
    with SessionFactory() as db:
        rows = db.execute(text("""
            SELECT pain_idx, owner_orig_idx, impact_orig_idx,
                   owner_correct, impact_correct, both_correct
            FROM selections
            WHERE session_id = :sid
            ORDER BY pain_idx
        """), {"sid": session_id}).mappings().all()
        return tuple(tuple(dict(r).items()) for r in rows)


def get_stats() -> dict[str, Any]:
    """
    Aggregate stats for the register screen and admin dashboard:
     - total unique players
     - total sessions played
     - perfect scores (5/5) count
     - average score
     - per-pain accuracy rates
    """
    return dict(_get_stats_cached())


@lru_cache(maxsize=1)
def _get_stats_cached() -> tuple[tuple[str, Any], ...]:
    with SessionFactory() as db:
        totals = db.execute(text("""
            SELECT
                (SELECT COUNT(*) FROM players)                           AS total_players,
                (SELECT COUNT(*) FROM game_sessions)                     AS total_sessions,
                (SELECT COUNT(*) FROM game_sessions WHERE is_perfect=1)  AS perfect_count,
                (SELECT ROUND(AVG(score),2) FROM game_sessions)          AS avg_score
        """)).mappings().first()

        pain_accuracy = db.execute(text("""
            SELECT
                pain_idx,
                COUNT(*)                                AS total,
                SUM(CASE WHEN both_correct=1 THEN 1 ELSE 0 END) AS correct_count,
                ROUND(
                    100.0 * SUM(CASE WHEN both_correct=1 THEN 1 ELSE 0 END) / COUNT(*),
                    1
                ) AS accuracy_pct
            FROM selections
            GROUP BY pain_idx
            ORDER BY pain_idx
        """)).mappings().all()

        result = {
            "total_players":  totals["total_players"]  or 0,
            "total_sessions": totals["total_sessions"] or 0,
            "perfect_count":  totals["perfect_count"]  or 0,
            "avg_score":      totals["avg_score"]       or 0.0,
            "pain_accuracy":  [dict(r) for r in pain_accuracy],
        }
        return tuple(result.items())


def get_perfect_score_players() -> list[dict[str, Any]]:
    """All players who achieved at least one perfect score — for prize draw."""
    with SessionFactory() as db:
        rows = db.execute(text("""
            SELECT DISTINCT p.name, p.company, p.email,
                   MIN(gs.time_used) AS best_time,
                   MIN(gs.completed_at) AS first_perfect
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            WHERE gs.is_perfect = 1
            GROUP BY p.id
            ORDER BY best_time ASC, first_perfect ASC
        """)).mappings().all()
        return [dict(r) for r in rows]


def get_registration_backup_path() -> Path:
    """Return the current Excel backup path for registration data."""
    return REGISTRATION_BACKUP_PATH


def is_email_registered(email: str) -> bool:
    """Fast existence check for registration blocking."""
    normalized_email = email.strip().lower()
    if not normalized_email:
        return False
    with SessionFactory() as db:
        return db.scalar(select(Player.id).where(Player.email == normalized_email)) is not None
