from hashlib import sha256
from pathlib import Path

import streamlit as st

from algorithm import FFMPEG_FILTERS
from video_processing import enhance_video
from workspace_ui import render_page

RESOLUTIONS = {
    "720p · 1280 × 720": (1280, 720),
    "1080p · 1920 × 1080": (1920, 1080),
    "1440p · 2560 × 1440": (2560, 1440),
    "4K · 3840 × 2160": (3840, 2160),
}
VIDEO_FORMATS = ["mp4", "mov", "avi", "wmv", "mpg", "mpeg"]

render_page("视频超分辨率", "选择输出分辨率，将视频放大并导出为 MP4。", "📽")
controls, preview = st.columns([1, 2], gap="large")

with controls, st.container(border=True):
    st.subheader("上传与设置")
    uploaded = st.file_uploader("上传视频", type=VIDEO_FORMATS)
    st.caption("支持 MP4、MOV、AVI、WMV、MPG 和 MPEG。")
    method = st.selectbox("缩放算法", list(FFMPEG_FILTERS), index=2)
    resolution_label = st.selectbox("输出分辨率", list(RESOLUTIONS))
    st.caption("保留画面比例，必要时补黑边。分辨率越高，处理时间越长。")
    process = st.button(
        "开始增强", type="primary", disabled=uploaded is None, use_container_width=True
    )

with preview, st.container(border=True):
    st.subheader("视频预览")
    if uploaded is None:
        st.session_state.pop("video_result", None)
        st.html('<div class="sr-empty">上传视频后在这里查看进度和结果</div>')
        st.stop()

    source = uploaded.getvalue()
    suffix = Path(uploaded.name).suffix.lower()
    key = (sha256(source).hexdigest(), method, resolution_label)
    result = st.session_state.get("video_result")
    if result is not None and result["key"] != key:
        st.session_state.pop("video_result")
        result = None

    if process:
        status = st.status("正在读取视频…", expanded=True)
        progress = status.empty()

        def update(stage, seconds, duration):
            if stage == "导出视频":
                status.update(label="正在准备下载…")
                progress.progress(100, text="读取视频 → 增强帧 → 导出视频")
            elif duration:
                percent = min(99, int(100 * seconds / duration))
                status.update(label="正在增强视频…")
                progress.progress(percent, text=f"增强帧 · {percent}%")
            else:
                status.update(label="正在增强视频…")
                progress.caption(f"已处理 {seconds:.1f} 秒")

        try:
            data, original_size, duration = enhance_video(
                source, suffix, RESOLUTIONS[resolution_label], method, update
            )
        except (OSError, RuntimeError, ValueError):
            status.update(label="视频处理失败", state="error", expanded=False)
            st.error("请尝试上传较短的 MP4，或选择较低的输出分辨率。")
        else:
            result = {
                "key": key, "bytes": data, "original_size": original_size, "duration": duration
            }
            st.session_state.video_result = result
            status.update(label="视频已处理完成", state="complete", expanded=False)

    options = ["增强视频", "原视频"] if result is not None else ["原视频"]
    selected = st.radio("预览内容", options, horizontal=True, label_visibility="collapsed")
    if selected == "增强视频":
        st.video(result["bytes"], format="video/mp4")
    elif suffix in {".mp4", ".mov"}:
        st.video(source, format="video/quicktime" if suffix == ".mov" else "video/mp4")
        st.caption("原视频能否播放取决于浏览器和原文件编码。")
    else:
        st.info("已上传原视频。处理完成后可在这里播放 MP4 结果。")

    if result is not None:
        width, height = result["original_size"]
        out_width, out_height = RESOLUTIONS[resolution_label]
        st.html(f'<p class="sr-sizes">{width} × {height} → {out_width} × {out_height}</p>')
        if result["duration"]:
            st.caption(f'原视频时长约 {result["duration"]:.1f} 秒')
        st.download_button(
            "下载增强视频",
            data=result["bytes"],
            file_name=f"{Path(uploaded.name).stem}_{out_height}p.mp4",
            mime="video/mp4",
            on_click="ignore",
            type="primary",
        )
