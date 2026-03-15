# Version 2.0 - CSS and Styling for Prize Pool

The following CSS styles were used in Version 2.0 to style the prize pool section.

## Prize Banner CSS

```css
.prize-banner {
  border-radius: var(--radius);
  padding: 18px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.16), rgba(3,94,137,0.22)),
    radial-gradient(circle at 12% 18%, rgba(236,250,247,0.18), transparent 22%),
    radial-gradient(circle at 86% 26%, rgba(6,194,172,0.18), transparent 24%);
  border: 1px solid rgba(255,255,255,0.22);
  position: relative;
  overflow: hidden;
  margin-bottom: 16px;
  text-align: center;
  box-shadow: var(--shadow2), inset 0 1px 0 rgba(255,255,255,0.22);
  backdrop-filter: blur(20px) saturate(145%);
  -webkit-backdrop-filter: blur(20px) saturate(145%);
}

.prize-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(255,255,255,0.5) 0%, transparent 70%);
  pointer-events: none;
}

.prize-top-label {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #77c4a5;
  margin-bottom: 12px;
}

.prize-items {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
  flex-wrap: nowrap;
}

.prize-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.prize-video {
  width: 100%;
  height: 140px;
  object-fit: cover;
  display: block;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.prize-item-name {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #335369;
  padding: 10px 0 4px;
  text-align: center;
}

.prize-item-count {
  font-size: 12px;
  font-weight: 700;
  color: #00111f;
  padding-bottom: 10px;
}

.prize-banner::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,.4) 50%, transparent 70%);
  background-size: 200% auto;
  animation: shimmer 3s linear infinite;
  pointer-events: none;
  border-radius: var(--radius);
}

@keyframes shimmer {
  from {
    background-position: 200% 0;
  }
  to {
    background-position: -200% 0;
  }
}
```

## Design Tokens (Global CSS Variables)

```css
:root {
  --bg:      #0470a2;
  --surface: rgba(255,255,255,0.16);
  --light-wash: rgba(236,250,247,0.22);
  --border:  rgba(255,255,255,0.22);
  --accent:  #023c57;
  --accent2: #06c2ac;
  --green:   #77c4a5;
  --text:    #f7fffe;
  --muted:   #d5ecef;
  --shadow:  0 16px 34px rgba(0,0,0,0.18);
  --shadow2: 0 24px 48px rgba(0,0,0,0.24);
  --radius:  22px;
}
```

## HTML Structure Used

```html
<div class="prize-banner">
  <div class="prize-top-label">Prize Pool</div>
  <div style="display:flex;gap:8px;margin-bottom:6px">
    <!-- Laptop Prize Card -->
    <div style="flex:1;background:rgba(255,255,255,0.92);border:1px solid rgba(15,23,42,.08);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;align-items:center;">
      <div style="width:100%">
        <!-- VIDEO EMBEDDED HERE -->
      </div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#335369;padding:10px 0 4px;text-align:center">Laptop</div>
      <div style="font-size:12px;font-weight:700;color:#00111f;padding-bottom:10px">1 winner</div>
    </div>
    
    <!-- Smartwatch Prize Card -->
    <div style="flex:1;background:rgba(255,255,255,0.92);border:1px solid rgba(15,23,42,.08);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;align-items:center;">
      <div style="width:100%">
        <!-- VIDEO EMBEDDED HERE -->
      </div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#335369;padding:10px 0 4px;text-align:center">Smartwatch</div>
      <div style="font-size:12px;font-weight:700;color:#00111f;padding-bottom:10px">3 winners</div>
    </div>
  </div>
</div>
```

## Color Scheme

- **Background**: Blue gradient `#0470a2`
- **Card Background**: Near white with transparency `rgba(255,255,255,0.92)`
- **Accent Green**: `#77c4a5` (for "Prize Pool" label)
- **Text**: Light text `#f7fffe`
- **Muted**: Grayed text `#d5ecef`
- **Dark**: Deep blue-black `#00111f`

## Effects

1. **Glass-morphism**: Frosted glass effect with `backdrop-filter: blur(20px) saturate(145%)`
2. **Shimmer Animation**: Animated gradient overlay that sweeps across the banner
3. **Shadow**: Deep shadow with inset highlight `box-shadow: 0 24px 48px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.22)`
4. **Glow**: Radial gradient from top creating a subtle glow effect

## Mobile Responsiveness

The design uses flexible layout:
- `flex: 1` on each prize card ensures equal width
- `gap: 8px` provides consistent spacing
- `overflow: hidden` clips video to rounded corners
- Adapts to container width without hardcoded pixels
