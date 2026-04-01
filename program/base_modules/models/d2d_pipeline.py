from typing import List, Optional
from pydantic import BaseModel


class DatasourceRef(BaseModel):
  name: str


class DatasetRef(BaseModel):
  name: str


class AnalysisRef(BaseModel):
  name: str


class PipelineConfig(BaseModel):
  name: str = ""
  datasources: List[DatasourceRef] = []
  datasets: List[DatasetRef] = []
  analysis: List[AnalysisRef] = []


class D2DPipelineConfig(BaseModel):
  config_file_dir: Optional[str] = ""
  pipelines: List[PipelineConfig] = []
