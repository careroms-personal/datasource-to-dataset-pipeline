from enum import StrEnum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class OutputType(StrEnum):
  CSV = "csv"
  JSON = "json"


class ClientConfig(BaseModel):
  name: str = "default"
  url: str = ""
  api: str = "api/v1"
  timeout: int = 30


class RangeConfig(BaseModel):
  name: str = "default"
  start_time: str = ""
  end_time: str = ""
  step: str = ""
  start_end_slice: str = ""


class WriteOutput(BaseModel):
  type: OutputType
  dir: str = ""


class OutputConfig(BaseModel):
  name: str = "default"
  relative_path: str = ""
  print_output: bool = False
  write_output: List[WriteOutput] = []


class ExportMetric(BaseModel):
  name: str = ""
  override: str = ""


class QueryResultExport(BaseModel):
  name: str = "default"
  export_metric: List[ExportMetric] = []


class Query(BaseModel):
  name: str = ""
  promql: str = ""
  clients: Optional[str] = None               # ref to named ClientConfig, None = use default
  output_configs: Optional[str] = None        # ref to named OutputConfig, None = use default
  query_result_exports: Optional[str] = None  # ref to named QueryResultExport, None = use default


class RangeQuery(Query):
  range_configs: Optional[str] = None         # ref to named RangeConfig, None = use default


class Queries(BaseModel):
  single: List[Query] = []
  range: List[RangeQuery] = []


class PrometheusConfig(BaseModel):
  clients: List[ClientConfig] = [ClientConfig()]
  range_configs: List[RangeConfig] = [RangeConfig()]
  query_result_exports: List[QueryResultExport] = [QueryResultExport()]
  output_configs: List[OutputConfig] = [OutputConfig()]


class PrometheusDatasourceConfig(BaseModel):
  """Mirrors the yaml file structure — used for loading and validating datasource config files."""
  type: Literal["prometheus"]
  global_: PrometheusConfig = Field(default_factory=PrometheusConfig, alias="global")
  queries: Queries = Queries()

  model_config = {"populate_by_name": True}


class PrometheusQueryConfig(BaseModel):
  name: str
  query_type: Literal["query", "query_range"]
  start: Optional[int] = None
  end: Optional[int] = None
  step: Optional[int] = None
  promql: str = ""
  client: ClientConfig = ClientConfig()
  output_config: OutputConfig = OutputConfig()
  export_metric: List[ExportMetric] = []
