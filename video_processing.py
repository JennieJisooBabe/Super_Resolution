import math
import subprocess
import tempfile
from pathlib import Path

import cv2
import imageio_ffmpeg

from algorithm import FFMPEG_FILTERS


def video_info(source):
    capture = cv2.VideoCapture(str(source))
    try:
        if not capture.isOpened():
            raise ValueError("无法读取这个视频，请检查文件是否完整。")
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = capture.get(cv2.CAP_PROP_FPS)
        frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frames / fps if frames > 0 and math.isfinite(fps) and fps > 0 else None
        return width, height, duration
    finally:
        capture.release()


def convert_video(source, output, resolution, method, update):
    width, height = resolution
    filter_flags = FFMPEG_FILTERS[method]
    video_filter = (
        f"scale={width}:{height}:flags={filter_flags}:"
        "force_original_aspect_ratio=decrease:force_divisible_by=2,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    )
    command = [
        imageio_ffmpeg.get_ffmpeg_exe(),
        "-hide_banner", "-loglevel", "error", "-nostdin",
        "-progress", "pipe:1", "-nostats",
        "-i", str(source), "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", video_filter,
        "-c:v", "libx264", "-threads", "2", "-preset", "veryfast",
        "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-movflags", "+faststart",
        str(output),
    ]
    with tempfile.TemporaryFile() as errors:
        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=errors, text=True, encoding="utf-8",
            errors="replace",
        ) as process:
            try:
                for line in process.stdout:
                    name, _, value = line.strip().partition("=")
                    if name == "out_time_us" and value.lstrip("-").isdigit():
                        update(max(0, int(value)) / 1_000_000)
                exit_code = process.wait()
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()
        if exit_code != 0 or not output.is_file() or output.stat().st_size == 0:
            errors.seek(0)
            detail = errors.read().decode("utf-8", errors="replace").strip()
            raise RuntimeError(detail or "FFmpeg did not produce a video")


def enhance_video(data, suffix, resolution, method, update):
    with tempfile.TemporaryDirectory(prefix="super-resolution-") as folder:
        source = Path(folder) / f"input{suffix}"
        output = Path(folder) / "enhanced.mp4"
        source.write_bytes(data)
        width, height, duration = video_info(source)
        update("增强帧", 0.0, duration)

        def update_time(seconds):
            update("增强帧", seconds, duration)

        convert_video(source, output, resolution, method, update_time)
        update("导出视频", None, duration)
        return output.read_bytes(), (width, height), duration
