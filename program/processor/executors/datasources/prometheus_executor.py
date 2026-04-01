from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from typing import List

from base_modules.base_executor import BaseExecutor
from base_modules.models.datasources.prometheus import (
  ClientConfig,
  OutputConfig,
  QueryResultExport,
  RangeConfig,
  PrometheusDatasourceConfig,
  PrometheusQueryConfig,
)


class PrometheusDatasourceExecutor(BaseExecutor):
  def __init__(self, config: PrometheusDatasourceConfig):
    self.config = config
    self.global_ = config.global_
    self.query_configs: List[PrometheusQueryConfig] = []

  def _resolve(self, named_list: list, ref: str, default_name: str = "default"):
    name = ref if ref else default_name
    return next((item for item in named_list if item.name == name), named_list[0])

  def _parse_time(self, value: str) -> datetime:
    now = datetime.now(timezone.utc)
    if not value or value == "now":
      return now
    v, unit = value[:-1], value[-1]
    n = int(v)
    if unit == "h":
      return now - relativedelta(hours=n)
    elif unit == "d":
      return now - relativedelta(days=n)
    elif unit == "w":
      return now - relativedelta(weeks=n)
    elif unit == "m":
      return now - relativedelta(months=n)
    return datetime.fromisoformat(value)

  def _parse_step_seconds(self, step: str) -> int:
    if step.endswith("s"):
      return int(step[:-1])
    elif step.endswith("m"):
      return int(step[:-1]) * 60
    elif step.endswith("h"):
      return int(step[:-1]) * 3600
    return int(step)

  def _slice_range(self, start: datetime, end: datetime, slice_str: str):
    if not slice_str:
      yield start, end
      return
    delta_map = {"h": "hours", "d": "days", "w": "weeks", "m": "months"}
    unit = slice_str[-1]
    n = int(slice_str[:-1])
    kwargs = {delta_map[unit]: n}
    current = start
    while current < end:
      next_ = min(current + relativedelta(**kwargs), end)
      yield current, next_
      current = next_

  def _build_queries(self):
    g = self.global_

    for q in self.config.queries.single:
      client = self._resolve(g.clients, q.clients)
      output = self._resolve(g.output_configs, q.output_configs)
      export = self._resolve(g.query_result_exports, q.query_result_exports)

      self.query_configs.append(PrometheusQueryConfig(
        name=q.name,
        query_type="query",
        promql=q.promql,
        client=client,
        output_config=output,
        query_result_export=export,
      ))

    for q in self.config.queries.range:
      client = self._resolve(g.clients, q.clients)
      output = self._resolve(g.output_configs, q.output_configs)
      export = self._resolve(g.query_result_exports, q.query_result_exports)
      range_cfg: RangeConfig = self._resolve(g.range_configs, q.range_configs)

      start = self._parse_time(range_cfg.start_time)
      end = self._parse_time(range_cfg.end_time)
      step = self._parse_step_seconds(range_cfg.step)

      for slice_start, slice_end in self._slice_range(start, end, range_cfg.start_end_slice):
        self.query_configs.append(PrometheusQueryConfig(
          name=q.name,
          query_type="query_range",
          promql=q.promql,
          start=int(slice_start.timestamp()),
          end=int(slice_end.timestamp()),
          step=step,
          client=client,
          output_config=output,
          query_result_export=export,
        ))

  def _query(self, qc: PrometheusQueryConfig):
    pass

  def _query_range(self, qc: PrometheusQueryConfig):
    pass

  def execute(self):
    self._build_queries()
    for qc in self.query_configs:
      if qc.query_type == "query":
        self._query(qc)
      else:
        self._query_range(qc)
