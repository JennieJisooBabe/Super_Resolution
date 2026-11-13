import streamlit as st

from workspace_ui import IMAGE_PAGE, VIDEO_PAGE, render_page

render_page("关于", "了解超分辨率工作台的功能、算法和参考文献。", "🔗")

with st.container(border=True):
    st.subheader("项目简介")
    st.write("上传低分辨率的图片或视频，选择放大参数，预览并下载处理结果。")
    image_link, video_link = st.columns(2)
    with image_link:
        st.page_link(IMAGE_PAGE, label="处理图像", icon="📸")
    with video_link:
        st.page_link(VIDEO_PAGE, label="处理视频", icon="📽")

with st.container(border=True):
    st.subheader("功能与使用")
    st.markdown(
        "- **图像超分辨率**：支持 ESPCN、FSRCNN 和三种插值算法。"
        "拖动滑块对比原图和增强图，下载 PNG。\n"
        "- **视频超分辨率**：用最近邻、双线性或双三次插值放大视频，"
        "预览并下载 MP4。"
    )

with st.container(border=True):
    st.subheader("使用提示")
    st.write("放大可以提高输出分辨率，细节效果取决于原素材和所选算法。"
             "处理时间会随输出尺寸和视频时长增加。")
    st.caption("左侧在线人数按当前连接的浏览器会话统计。")

with st.container(border=True):
    st.subheader("参考文献")
    st.markdown(
        "1. [Real-Time Single Image and Video Super-Resolution Using an Efficient "
        "Sub-Pixel Convolutional Neural Network](https://arxiv.org/pdf/1609.05158.pdf)\n"
        "2. [Accelerating the Super-Resolution Convolutional Neural Network]"
        "(https://mmlab.ie.cuhk.edu.hk/projects/FSRCNN.html)\n"
        "3. [Deep Laplacian Pyramid Networks for Fast and Accurate Super-Resolution]"
        "(https://arxiv.org/pdf/1704.03915.pdf)\n"
        "4. [Enhanced Deep Residual Networks for Single Image Super-Resolution]"
        "(https://arxiv.org/pdf/1707.02921.pdf)"
    )

    st.markdown(
        "[GitHub 源代码](https://github.com/JennieJisooBabe/Super_Resolution)"
    )
