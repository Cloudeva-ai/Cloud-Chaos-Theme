# Version 2.0 vs Version 1.0 Video Code Comparison

## Version 2.0 Implementation (Better - Direct src)

### 1. Video Data URI Function

```python
@st.cache_data
def _video_data_uri(path: str) -> str:
    video_path = Path(path)
    suffix = video_path.suffix.lower().lstrip(".") or "mp4"
    encoded = base64.b64encode(video_path.read_bytes()).decode("ascii")
    return f"data:video/{suffix};base64,{encoded}"
```

### 2. Video HTML (Direct src attribute)

```html
<video src="{base64_data}" autoplay loop muted playsinline webkit-playsinline 
       preload="metadata"
       poster=""
       onloadedmetadata="this.play().catch(() => {})"
       oncanplay="this.play().catch(() => {})"
       style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
</video>
```

---

## Version 1.0 Implementation (Original - Source tags)

### 1. Video Data URI Function

```python
def _video_data_uri(path: str, mime_type: str) -> str:
    video_path = Path(path)
    encoded = base64.b64encode(video_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"
```

### 2. Video HTML (Using source tags)

```html
<video autoplay loop muted playsinline preload="auto" poster=""
       onloadedmetadata="this.play().catch(() => {})"
       style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
  <source src="{base64_data}" type="video/mp4">
</video>
```

---

## Version 1.0 Complete Implementation

```python
# Load video files
laptop_video_mp4 = Path(__file__).parent / "static" / "Laptop_3d.mp4"
watch_video = Path(__file__).parent / "static" / "SmartWatch_3d.mp4"

# Default fallback HTML
laptop_video_html = "<div style='height:140px;display:flex;align-items:center;justify-content:center;color:var(--muted)'>Laptop</div>"
watch_video_html = "<div style='height:140px;display:flex;align-items:center;justify-content:center;color:var(--muted)'>Watch</div>"

# Generate base64 encoded video HTML if file exists
if laptop_video_mp4.exists():
    laptop_src = _video_data_uri(str(laptop_video_mp4), "video/mp4")
    laptop_video_html = f"""
    <video autoplay loop muted playsinline preload="auto"
           poster=""
           onloadedmetadata="this.play().catch(() => {{}})"
           style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
      <source src="{laptop_src}" type="video/mp4">
    </video>
    """

if watch_video.exists():
    watch_src = _video_data_uri(str(watch_video), "video/mp4")
    watch_video_html = f"""
    <video autoplay loop muted playsinline preload="auto"
           poster=""
           onloadedmetadata="this.play().catch(() => {{}})"
           style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
      <source src="{watch_src}" type="video/mp4">
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
```

---

## Key Differences

| Feature | Version 1.0 | Version 2.0 |
|---------|------------|------------|
| **Function signature** | `_video_data_uri(path, mime_type)` | `_video_data_uri(path)` |
| **File detection** | Full filenames (`.mp4`) | Preview versions (`.mp4`) |
| **Video tag src** | Uses `<source>` tags | Direct `src` attribute |
| **Media type** | Passed as parameter | Auto-detected from suffix |
| **Preload** | `preload="auto"` | `preload="metadata"` |
| **Path handling** | `str(laptop_video_mp4)` | Direct Path object |
| **Event handlers** | Single: `onloadedmetadata` | Dual: `onloadedmetadata` + `oncanplay` |
| **webkit-playsinline** | Not included | Included for iOS |

---

## Why Version 2.0 Was Better

1. **Direct src attribute** - More reliable with base64 data
2. **Dual event handlers** - Fallback if one event doesn't trigger
3. **webkit-playsinline** - Better iOS Safari support
4. **Auto-detect mime type** - Less error-prone
5. **Preview versions** - Smaller file sizes for faster loading
6. **metadata preload** - Faster playback start

---

## Why Videos Still Might Not Play on Streamlit Cloud

**Version 1.0 & 2.0 Problem**: Both used base64 encoding which only works locally.

**When deployed to Streamlit Cloud**:
- Files don't exist in the runtime
- Base64 encoding fails
- No fallback to GitHub URLs
- Videos don't play

**Solution**: Use GitHub raw URLs as fallback (as implemented in current fix)
