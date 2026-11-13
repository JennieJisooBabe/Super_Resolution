from pathlib import Path

import streamlit as st
from streamlit.runtime import Runtime

ROOT = Path(__file__).resolve().parent
IMAGE_PAGE = "0📸_图像超分辨率.py"
VIDEO_PAGE = "pages/1📽_视频超分辨率.py"
ABOUT_PAGE = "pages/2🔗_关于.py"


def render_page(title, subtitle, icon):
    st.set_page_config(
        page_title=f"{title} · 超分辨率工作台",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="auto",
    )
    st.html(ROOT / "workspace.css")
    with st.sidebar:
        st.divider()
        show_online_count()
    st.title(title)
    st.markdown(f'<p class="sr-subtitle">{subtitle}</p>', unsafe_allow_html=True)


@st.fragment(run_every="15s")
def show_online_count():
    if not Runtime.exists():
        return
    count = len(Runtime.instance()._session_mgr.list_active_sessions())
    st.html(
        '<div class="sr-online"><span class="sr-dot" aria-hidden="true"></span>'
        f'<span>当前在线人数</span><strong>{count}</strong></div>'
    )
