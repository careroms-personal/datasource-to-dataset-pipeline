from typing import List, Optional
from pydantic import BaseModel, Field


class ClientConfig(BaseModel):
  url: str = ""
  api: str = "api/v1"
  timeout: int = 30


class RangeConfig(BaseModel):
  start_time: str = ""
  end_time: str = ""
  step: str = ""
  start_end_slice: str = ""


class WriteOutput(BaseModel):
  type: str = ""
  dir: str = ""


class OutputConfig(BaseModel):
  relative_path: str = ""
  print_output: bool = False
  write_output: List[WriteOutput] = []


class ExportMetric(BaseModel):
  name: str = ""
  override: str = ""


class QueryResultExport(BaseModel):
  export_metric: List[ExportMetric] = []


class Query(BaseModel):
  name: str = ""
  promql: str = ""
  client: Optional[ClientConfig] = None
  output_config: Optional[OutputConfig] = None
  query_result_export: Optional[QueryResultExport] = None


class RangeQuery(Query):
  range_config: Optional[RangeConfig] = None


class Queries(BaseModel):
  single: List[Query] = []
  range: List[RangeQuery] = []


class PrometheusConfig(BaseModel):
  client: ClientConfig = ClientConfig()
  range_config: RangeConfig = RangeConfig()
  query_result_export: QueryResultExport = QueryResultExport()
  output_config: OutputConfig = OutputConfig()


class PrometheusDatasourceFile(BaseModel):
  """Mirrors the yaml file structure — used for loading and validating datasource config files."""
  global_: PrometheusConfig = Field(default_factory=PrometheusConfig, alias="global")
  queries: Queries = Queries()

  model_config = {"populate_by_name": True}


class PrometheusQuery(BaseModel):
  """Flat resolved model for instant query — global + per-query merged, ready for executor."""
  name: str = ""
  promql: str = ""
  client: ClientConfig = ClientConfig()
  output_config: OutputConfig = OutputConfig()
  query_result_export: QueryResultExport = QueryResultExport()


class PrometheusQueryRange(PrometheusQuery):
  """Flat resolved model for range query — extends PrometheusQuery with range_config."""
  range_config: RangeConfig = RangeConfig()