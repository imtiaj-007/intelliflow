from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SystemInfo(BaseModel):
    platform: str
    python_version: str
    uptime: str
    uptime_seconds: float


class CPUInfo(BaseModel):
    usage_percent: float
    cores: int
    logical_cores: int


class MemoryInfo(BaseModel):
    total_mb: float
    available_mb: float
    used_mb: float
    usage_percent: float


class DiskInfo(BaseModel):
    total_gb: float
    used_gb: float
    free_gb: float
    usage_percent: float


class ResourcesInfo(BaseModel):
    cpu: CPUInfo
    memory: MemoryInfo
    disk: DiskInfo


class ProcessInfo(BaseModel):
    memory_rss_mb: float
    memory_vms_mb: float
    cpu_percent: float
    thread_count: int
    create_time: datetime


class GPUInfo(BaseModel):
    available: bool = False
    gpu_usage_percent: Optional[float] = None
    gpu_memory_used_mb: Optional[float] = None
    gpu_memory_total_mb: Optional[float] = None
    gpu_temperature: Optional[float] = None
    message: Optional[str] = None


class DatabaseDetails(BaseModel):
    status: str
    version: Optional[str] = None
    active_connections: Optional[int] = None
    response_time_ms: Optional[str] = None
    error: Optional[str] = None


class ServicesInfo(BaseModel):
    database: str
    database_details: DatabaseDetails
    redis: str
    aws_s3: str
    api: str


class HealthResponse(BaseModel):
    status: str
    message: str
    version: str
    timestamp: datetime
    system: SystemInfo
    resources: ResourcesInfo
    process: ProcessInfo
    gpu: GPUInfo
    services: ServicesInfo


class LogOptions(BaseModel):
    format: str
    enqueue: bool
    rotation: str
    retention: str
    compression: str
    serialize: bool
    catch: bool


class AppCookies(BaseModel):
    _sid: str
    _uid: str