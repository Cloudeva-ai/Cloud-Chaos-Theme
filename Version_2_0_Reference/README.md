# Version 2.0 - Working Video Implementation Reference

This folder contains the complete Version 2.0 code that had smooth, working videos.

## Key Difference: Video Handling

Version 2.0 used a simple, effective approach for video playback:

### 1. Video Data URI Function
```python
@st.cache_data
def _video_data_uri(path: str) -> str:
    video_path = Path(path)
    suffix = video_path.suffix.lower().lstrip(".") or "mp4"
    encoded = base64.b64encode(video_path.read_bytes()).decode("ascii")
    return f"data:video/{suffix};base64,{encoded}"
```

### 2. Video HTML Generation
```html
<video src="{base64_data}" autoplay loop muted playsinline webkit-playsinline 
       preload="metadata"
       poster=""
       onloadedmetadata="this.play().catch(() => {})"
       oncanplay="this.play().catch(() => {})"
       style="width:100%;height:140px;object-fit:cover;display:block;background:#fff">
</video>
```

## Why Version 2.0 Worked Well Locally

✅ **Direct src attribute** - Embedded video data directly in HTML  
✅ **Dual event handlers** - Multiple autoplay triggers for reliability  
✅ **webkit-playsinline** - iOS Safari compatibility  
✅ **Auto-detect mime type** - Less configuration needed  
✅ **Preview versions** - Used smaller preview files for faster loading  
✅ **metadata preload** - Faster initial playback start  

## Implementation Details

**Video Sources Used:**
- `Laptop_3d_preview.mp4` (0.38 MB)
- `SmartWatch_3d_preview.mp4` (2.19 MB)

**Key Attributes:**
- `autoplay` - Auto-start when loaded
- `loop` - Continuous playback
- `muted` - No sound output
- `playsinline` - Mobile friendly
- `webkit-playsinline` - iOS Safari support
- `preload="metadata"` - Fast initialization

**Event Handlers:**
- `onloadedmetadata="this.play().catch(() => {})"` - Start play when ready
- `oncanplay="this.play().catch(() => {})"` - Fallback trigger

## Git Commit Hash
Version 2.0: `3864019`

## Prize Pool Integration
Videos were seamlessly integrated into the prize pool section with:
- Laptop video on the left (1 winner)
- Smartwatch video on the right (3 winners)
- Both looping smoothly without any player controls
- Clean, professional appearance

## File Structure
```
static/
├── Laptop_3d.mp4 (1.27 MB) - Full version
├── Laptop_3d_preview.mp4 (0.38 MB) - Used in V2.0
├── SmartWatch_3d.mp4 (18.72 MB) - Full version
└── SmartWatch_3d_preview.mp4 (2.19 MB) - Used in V2.0
```

## Why It Worked Locally But Not on Streamlit Cloud

- ✅ Locally: Base64 encoding works when files exist
- ❌ Streamlit Cloud: Files don't exist in runtime, base64 fails
- ❌ No fallback mechanism in V2.0

## Current Solution (V4.7+)
The current implementation combines V2.0's quality with cloud compatibility:
- Tries local base64 encoding first (V2.0 style)
- Falls back to GitHub URLs when on Streamlit Cloud
- Uses `<source>` tags for better Streamlit compatibility
- Includes `crossorigin="anonymous"` for GitHub access
