# Version 2.0 Video Code - Complete Prize Pool Implementation

## 1. Video Data URI Function

```python
@st.cache_data
def _video_data_uri(path: str) -> str:
    video_path = Path(path)
    suffix = video_path.suffix.lower().lstrip(".") or "mp4"
    encoded = base64.b64encode(video_path.read_bytes()).decode("ascii")
    return f"data:video/{suffix};base64,{encoded}"
```

## 2. Video Asset Selection Function

```python
def _static_asset_url(filename: str) -> str:
    return f"/app/static/{filename}"
```

## 3. Prize Pool Video Rendering (in screen_register function)

```python
# Load video files
laptop_video_mp4 = Path(__file__).parent / "static" / "Laptop_3d_preview.mp4"
watch_video = Path(__file__).parent / "static" / "SmartWatch_3d_preview.mp4"

# Default fallback HTML
laptop_video_html = "<div style='height:140px;display:flex;align-items:center;justify-content:center;color:var(--muted)'>Laptop</div>"
watch_video_html = "<div style='height:140px;display:flex;align-items:center;justify-content:center;color:var(--muted)'>Watch</div>"

# Generate base64 encoded video HTML if file exists
if laptop_video_mp4.exists():
    laptop_src = _video_data_uri(laptop_video_mp4)
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
```

## Key Features of Version 2.0

✅ **Simple Function** - `_video_data_uri()` uses base64 encoding  
✅ **Direct src attribute** - `<video src="{base64_data}">`  
✅ **Event-based autoplay** - Uses `onloadedmetadata` and `oncanplay` handlers  
✅ **Self-executing play** - `this.play().catch(() => {})`  
✅ **No loops or complexity** - Direct Streamlit markdown rendering  
✅ **Seamless playback** - Videos loop automatically  
✅ **No player controls** - Clean, minimal UI  

## Video Attributes Explained

```html
<video 
  src="{base64_encoded_data}"  <!-- Direct embedding -->
  autoplay                      <!-- Auto starts -->
  loop                          <!-- Loops seamlessly -->
  muted                         <!-- No audio -->
  playsinline                   <!-- Mobile friendly -->
  webkit-playsinline            <!-- iOS Safari -->
  preload="metadata"            <!-- Load video metadata -->
  poster=""                     <!-- No preview image -->
  onloadedmetadata="this.play().catch(() => {})"  <!-- Play when ready -->
  oncanplay="this.play().catch(() => {})"         <!-- Fallback play trigger -->
  style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
</video>
```

## Why This Worked

1. **Base64 encoding** - Videos embedded directly in HTML, no external requests
2. **Event handlers** - Ensures playback starts immediately when browser is ready
3. **Muted & loop** - Plays continuously without user interaction
4. **Error handling** - `.catch(() => {})` silently ignores autoplay restrictions
