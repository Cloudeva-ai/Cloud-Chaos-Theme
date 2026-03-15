# Version 2.0 - app.py (Key Sections for Video Implementation)
# Complete file hash: 3864019
# This file shows the working video implementation from Version 2.0

# ─────────────────────────────────────────────────────────────
# IMPORTS & SETUP
# ─────────────────────────────────────────────────────────────
from __future__ import annotations
import base64
import json
import time
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import database as db
import game_data as gd
import game_engine as ge

# ─────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS - IMAGE & VIDEO HANDLING
# ─────────────────────────────────────────────────────────────

@st.cache_data
def _image_data_uri(path: str) -> str:
    """Convert image file to base64 data URI."""
    image_path = Path(path)
    suffix = image_path.suffix.lower().lstrip(".") or "png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/{suffix};base64,{encoded}"


@st.cache_data
def _video_data_uri(path: str) -> str:
    """
    VERSION 2.0 IMPLEMENTATION
    Convert video file to base64 data URI.
    This works perfectly locally - simple and effective.
    """
    video_path = Path(path)
    suffix = video_path.suffix.lower().lstrip(".") or "mp4"
    encoded = base64.b64encode(video_path.read_bytes()).decode("ascii")
    return f"data:video/{suffix};base64,{encoded}"


def _static_asset_url(filename: str) -> str:
    """Reference static asset via Streamlit path."""
    return f"/app/static/{filename}"


# ─────────────────────────────────────────────────────────────
# SCREEN: REGISTER - Prize Pool Section
# ─────────────────────────────────────────────────────────────

def screen_register():
    """Registration screen with Prize Pool videos."""
    
    # ... (logo and hero section) ...
    
    # VERSION 2.0: VIDEO HANDLING
    # Load video files - using preview versions for smaller size
    laptop_video_mp4 = Path(__file__).parent / "static" / "Laptop_3d_preview.mp4"
    watch_video = Path(__file__).parent / "static" / "SmartWatch_3d_preview.mp4"

    # Default fallback HTML
    laptop_video_html = "<div style='height:140px;display:flex;align-items:center;justify-content:center;color:var(--muted)'>Laptop</div>"
    watch_video_html = "<div style='height:140px;display:flex;align-items:center;justify-content:center;color:var(--muted)'>Watch</div>"

    # Generate base64 encoded video HTML if file exists
    if laptop_video_mp4.exists():
        laptop_src = _video_data_uri(laptop_video_mp4)
        # VERSION 2.0: Direct src attribute with dual event handlers
        laptop_video_html = f"""
        <video src="{laptop_src}" autoplay loop muted playsinline webkit-playsinline preload="metadata"
               poster=""
               onloadedmetadata="this.play().catch(() => {{}})"
               oncanplay="this.play().catch(() => {{}})"
               style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
        </video>
        """

    if watch_video.exists():
        watch_src = _video_data_uri(watch_video)
        # VERSION 2.0: Direct src attribute with dual event handlers
        watch_video_html = f"""
        <video src="{watch_src}" autoplay loop muted playsinline webkit-playsinline preload="metadata"
               poster=""
               onloadedmetadata="this.play().catch(() => {{}})"
               oncanplay="this.play().catch(() => {{}})"
               style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
        </video>
        """

    # Render the prize banner with videos
    st.markdown(f"""
    <div class="prize-banner">
      <div class="prize-top-label">Prize Pool</div>
      <div style="display:flex;gap:8px;margin-bottom:6px">
        <div style="flex:1;background:rgba(255,255,255,0.92);border:1px solid rgba(15,23,42,.08);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;align-items:center;">
          <div style="width:100%">{laptop_video_html}</div>
          <div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#335369;padding:10px 0 4px;text-align:center">Laptop</div>
          <div style="font-size:12px;font-weight:700;color:#00111f;padding-bottom:10px">1 winner</div>
        </div>
        <div style="flex:1;background:rgba(255,255,255,0.92);border:1px solid rgba(15,23,42,.08);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;align-items:center;">
          <div style="width:100%">{watch_video_html}</div>
          <div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#335369;padding:10px 0 4px;text-align:center">Smartwatch</div>
          <div style="font-size:12px;font-weight:700;color:#00111f;padding-bottom:10px">3 winners</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ... (registration form continues) ...


# ─────────────────────────────────────────────────────────────
# VERSION 2.0 KEY FEATURES
# ─────────────────────────────────────────────────────────────
"""
WHAT MADE VERSION 2.0 WORK WELL:

1. **Simple Function Design**
   - _video_data_uri(path) - minimal parameters
   - Auto-detects file type from suffix
   - Single responsibility

2. **Direct src Attribute** (Key Difference from V1.0)
   - <video src="{base64}"> instead of <source> tags
   - More reliable with base64 data
   - Direct HTML5 approach

3. **Dual Event Handlers** (Reliability)
   - onloadedmetadata: Primary trigger
   - oncanplay: Fallback trigger
   - Ensures playback starts even in slow conditions

4. **iOS Compatibility**
   - webkit-playsinline: Essential for iOS Safari
   - playsinline: Standard attribute
   - Works on both mobile and desktop

5. **Performance Optimization**
   - Uses preview versions (small files)
   - preload="metadata" (fast initialization)
   - Laptop_3d_preview.mp4: 0.38 MB
   - SmartWatch_3d_preview.mp4: 2.19 MB

6. **Clean Implementation**
   - No complex JavaScript
   - Minimal HTML attributes
   - Self-executing play via onloadedmetadata/oncanplay

WHY IT WORKED LOCALLY:
- Files always exist in development environment
- Base64 encoding works when files are readable
- No runtime dependencies
- Smooth, instant playback

LIMITATION FOR CLOUD:
- Base64 encoding fails when files don't exist (Streamlit Cloud)
- No fallback mechanism
- Would need GitHub URL fallback for cloud deployment
"""
