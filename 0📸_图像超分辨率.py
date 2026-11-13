from hashlib import sha256
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

from algorithm import INTERPOLATIONS, MODELS, resize_im
from comparison import show_comparison
from workspace_ui import render_page

MAX_OUTPUT_PIXELS = 24_000_000

render_page("图像超分辨率", "上传图片，选择算法和倍率，再拖动滑块比较处理前后的效果。", "📸")
controls, preview = st.columns([1, 2], gap="large")

with controls, st.container(border=True):
    st.subheader("上传与设置")
    uploaded = st.file_uploader("上传图片", type=["png", "jpg", "jpeg", "gif"])
    st.caption("支持 PNG、JPEG 和 GIF。GIF 仅处理首帧。")
    method = st.selectbox("增强算法", [*MODELS, *INTERPOLATIONS])
    scale = st.selectbox(
        "放大倍率",
        [2, 3, 4] if method in MODELS else [2, 3, 4, 5, 6],
        format_func=lambda value: f"{value}×",
    )
    process = st.button(
        "开始增强", type="primary", disabled=uploaded is None, use_container_width=True
    )

with preview, st.container(border=True):
    st.subheader("效果预览")
    if uploaded is None:
        st.session_state.pop("image_result", None)
        st.html('<div class="sr-empty">上传图片后在这里预览</div>')
        st.stop()

    source = uploaded.getvalue()
    key = (sha256(source).hexdigest(), method, scale)
    result = st.session_state.get("image_result")
    if result is not None and result["key"] != key:
        st.session_state.pop("image_result")
        result = None
    try:
        original = cv2.imdecode(np.frombuffer(source, np.uint8), cv2.IMREAD_COLOR)
    except cv2.error:
        original = None
    if original is None:
        st.error("无法读取这张图片，请尝试上传其他文件。")
        st.stop()

    height, width = original.shape[:2]
    if process:
        if width * height * scale ** 2 > MAX_OUTPUT_PIXELS:
            st.error("输出将超过 2400 万像素，请降低放大倍率或上传较小的图片。")
        else:
            try:
                with st.spinner("正在增强图像…"):
                    enhanced = resize_im(original, scale, method)
                    encoded_ok, encoded = cv2.imencode(".png", enhanced)
                    if not encoded_ok:
                        raise ValueError("PNG encoding failed")
                    result = {"key": key, "bytes": encoded.tobytes()}
                    st.session_state.image_result = result
            except (cv2.error, ValueError):
                st.error("图像处理失败，请尝试较低倍率或其他算法。")

    if result is None:
        st.image(original, channels="BGR", caption=f"原图 · {width} × {height}", width="stretch")
    else:
        enhanced = cv2.imdecode(np.frombuffer(result["bytes"], np.uint8), cv2.IMREAD_COLOR)
        out_height, out_width = enhanced.shape[:2]
        show_comparison(original, enhanced)
        st.html(f'<p class="sr-sizes">{width} × {height} → {out_width} × {out_height}</p>')
        st.download_button(
            "下载增强图像",
            data=result["bytes"],
            file_name=f"{Path(uploaded.name).stem}_{scale}x.png",
            mime="image/png",
            on_click="ignore",
            type="primary",
        )
