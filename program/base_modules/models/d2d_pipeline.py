from typing import List, Optional
from pydantic import BaseModel


class DatasourceRef(BaseModel):
  name: str


class AnalysisRef(BaseModel):
  name: str


class DatasetRef(BaseModel):
  name: str


class D2DPipelineConfig(BaseModel):
  config_file_dir: Optional[str] = ""
  datasources: List[DatasourceRef] = []
  analysis: List[AnalysisRef] = []
  datasets: List[DatasetRef] = []
