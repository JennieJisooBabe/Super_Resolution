from base64 import b64encode

import cv2
import streamlit.components.v1 as components


def preview_uri(image):
    height, width = image.shape[:2]
    scale = min(1, 1200 / max(height, width))
    if scale < 1:
        image = cv2.resize(
            image,
            (max(1, round(width * scale)), max(1, round(height * scale))),
            interpolation=cv2.INTER_AREA,
        )
    _, encoded = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 92])
    return "data:image/jpeg;base64," + b64encode(encoded.tobytes()).decode("ascii")


def show_comparison(original, enhanced):
    height, width = original.shape[:2]
    frame_height = min(510, max(210, round(600 * height / width)))
    components.html(
        f"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<style>
* {{box-sizing:border-box}}
body {{margin:0;color:#172033;font:14px system-ui,sans-serif}}
.preview {{position:relative;height:{frame_height}px;overflow:hidden;border-radius:12px;
  background:#e9eef6;--cut:50%}}
img {{position:absolute;width:100%;height:100%;object-fit:contain}}
.original {{clip-path:inset(0 calc(100% - var(--cut)) 0 0)}}
.line {{position:absolute;left:var(--cut);height:100%;border-left:2px solid white;
  box-shadow:0 0 3px #172033;pointer-events:none}}
.handle {{position:absolute;top:50%;left:0;transform:translate(-50%,-50%);display:grid;
  place-items:center;width:36px;height:36px;border-radius:50%;background:white;
  font-weight:700;box-shadow:0 1px 6px #17203366}}
.badge {{position:absolute;top:12px;padding:4px 8px;border-radius:6px;
  color:white;background:#172033e8;pointer-events:none}}
.before {{left:12px}} .after {{right:12px}}
input {{position:absolute;inset:0;width:100%;height:100%;opacity:0;margin:0;cursor:ew-resize}}
.preview:focus-within {{outline:2px solid #2563eb;outline-offset:-2px}}
</style></head>
<body><div class="preview">
<img src="{preview_uri(enhanced)}" alt="增强图">
<img class="original" src="{preview_uri(original)}" alt="原图">
<div class="line" aria-hidden="true"><div class="handle">❮ ❯</div></div>
<span class="badge before">原图</span><span class="badge after">增强图</span>
<input type="range" min="0" max="100" value="50" aria-label="调整原图与增强图的对比位置"
  oninput="this.parentElement.style.setProperty('--cut', this.value + '%')">
</div></body></html>""",
        height=frame_height,
    )
