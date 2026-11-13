# 超分辨率工作台

基于 Streamlit 的图像和视频超分辨率工具。图像使用 OpenCV 和仓库内的
ESPCN / FSRCNN 权重，视频使用 FFmpeg 插值并导出 MP4。

## 本地启动

建议使用 Python 3.10 或 3.11。进入项目根目录后运行：

```sh
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run "0📸_图像超分辨率.py"
```

macOS / Linux：

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run "0📸_图像超分辨率.py"
```

## 更新已有 Streamlit Community Cloud 部署

1. 将本包文件按原目录结构合并到 `main` 分支。确认已添加隐藏目录
   `.streamlit`，模型权重仍位于 `config`。
2. 保留原应用的入口 `0📸_图像超分辨率.py`，提交后由 Cloud 自动构建。
3. 打开原网址，用小图片和短 MP4 分别验证上传、处理、预览与下载。
   用另一个浏览器窗口验证在线人数变化，并打开「关于」检查参考文献。

在线人数按同一个 Streamlit 服务进程中的活跃连接会话统计，每 15 秒刷新。
同一个人打开多个独立页面时可能被计为多个会话。
