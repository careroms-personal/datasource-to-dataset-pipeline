from typing import List, Literal, Union, Annotated, Optional
from pydantic import BaseModel, Field

from .datasources.prometheus import PrometheusConfig


class PrometheusDatasource(PrometheusConfig):
  type: Literal["prometheus"]


DatasourceConfig = Annotated[
  Union[PrometheusDatasource],
  Field(discriminator="type")
]


class D2DPipelineConfig(BaseModel):
  config_file_dir: Optional[str] = ""
  datasources: List[DatasourceConfig] = []
  analysis: Optional[List[str]] = []
  datasets: Optional[List[str]] = []
