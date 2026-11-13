from pathlib import Path

import cv2

MODEL_DIR = Path(__file__).resolve().parent / "config"
INTERPOLATIONS = {
    "最近邻插值": cv2.INTER_NEAREST,
    "双线性插值": cv2.INTER_LINEAR,
    "双三次插值": cv2.INTER_CUBIC,
}
MODELS = {"ESPCN": "espcn", "FSRCNN": "fsrcnn"}
FFMPEG_FILTERS = {
    "最近邻插值": "neighbor",
    "双线性插值": "bilinear",
    "双三次插值": "bicubic",
}


def resize_im(image, scale, method):
    if method in INTERPOLATIONS:
        return cv2.resize(image, None, fx=scale, fy=scale, interpolation=INTERPOLATIONS[method])

    model = cv2.dnn_superres.DnnSuperResImpl_create()
    model.readModel(str(MODEL_DIR / f"{method}_x{scale}.pb"))
    model.setModel(MODELS[method], scale)
    return model.upsample(image)
