from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class ViewType(str, Enum):
    SIDE = "side"
    REAR = "rear"

class Handedness(str, Enum):
    RIGHT = "right"
    LEFT = "left"

class ScaleMethod(str, Enum):
    MARKER = "marker"
    AUTO = "auto"

class QCStatus(str, Enum):
    GOOD = "GOOD"
    WARN = "WARN"
    FAIL = "FAIL"

class MetaInfo(BaseModel):
    fps: float
    frames: int
    view: str
    handedness: str
    scale_method: str
    m_per_px: float

class EventFrames(BaseModel):
    penultimate_frame: Optional[int] = None
    plant_frame: Optional[int] = None
    release_frame: Optional[int] = None

class Metrics(BaseModel):
    release_angle_deg: Optional[float] = None
    release_height_m: Optional[float] = None
    release_height_ratio: Optional[float] = None
    release_speed_mps: Optional[float] = None
    plant_to_release_ms: Optional[float] = None
    plant_foot_progression_deg: Optional[float] = None
    shoulder_hip_separation_deg: Optional[float] = None
    lane_alignment_error_cm: Optional[float] = None

class QualityControl(BaseModel):
    release_fit_r2: Optional[float] = None
    foot_visibility: Optional[float] = None
    pose_confidence: Optional[float] = None
    overall_status: str = "WARN"
    notes: List[str] = []

class AnalyzeResponse(BaseModel):
    meta: MetaInfo
    events: EventFrames
    metrics: Metrics
    qc: QualityControl
    annotated_video_path: Optional[str] = None
    error: Optional[str] = None
