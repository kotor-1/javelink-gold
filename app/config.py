from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
MODEL_DIR = BASE_DIR / "models"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

MAX_VIDEO_SIZE_MB = 100
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".webm"}
DEFAULT_FPS = 30
MAX_PROCESS_TIME_SEC = 60

POSE_CONFIDENCE_THRESHOLD = 0.5
OBJECT_CONFIDENCE_THRESHOLD = 0.3
FOOT_CONTACT_VELOCITY_THRESHOLD = 0.05
RELEASE_DISTANCE_THRESHOLD = 0.1

DEFAULT_PERSON_HEIGHT = 1.75
MARKER_SIZE_M = 1.0
AUTO_SCALE_COEFFICIENT = 1.05

SAVGOL_WINDOW = 7
SAVGOL_POLY = 2

QC_GOOD_R2 = 0.9
QC_WARN_R2 = 0.75
QC_GOOD_VISIBILITY = 0.8
QC_WARN_VISIBILITY = 0.6

APP_TITLE = "Javelink Lite"
UPLOAD_HINT_SIDE = "From the side of throwing arm"
UPLOAD_HINT_REAR = "From behind the runway center"

ERROR_NO_MARKER = "Marker not detected"
ERROR_NO_OBJECT = "Object not detected"
ERROR_LOW_FPS = "Low frame rate"
ERROR_SHORT_CLIP = "Insufficient frames"
