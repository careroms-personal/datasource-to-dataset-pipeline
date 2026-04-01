import os
import yaml

from base_modules.base_executor import BaseExecutor
from base_modules.models.d2d_pipeline import D2DPipelineConfig
from base_modules.models.datasources.prometheus import PrometheusDatasourceConfig


class DatasourcesExecutor(BaseExecutor):
  def __init__(self, d2d_pipeline_config: D2DPipelineConfig):
    self.config_file_dir = d2d_pipeline_config.config_file_dir
    self.datasources = d2d_pipeline_config.datasources

    self.datasource_types = {
      "prometheus": PrometheusDatasourceConfig
    }

    self.datasource_executors = {
      "prometheus": self._call_prometheus_executor,
    }

  def _prepare_datasource(self, name: str):
    path = os.path.join(self.config_file_dir, "datasources", f"{name}.yaml")
    if not os.path.exists(path):
      raise FileNotFoundError(f"Datasource config not found: {path}")

    with open(path, "r") as f:
      yaml_data = yaml.safe_load(f)

    ds_type = yaml_data.get("type")
    if ds_type is None:
      raise ValueError(f"Missing 'type' in datasource config: {path}")

    model_class = self.datasource_types.get(ds_type)
    if model_class is None:
      raise ValueError(f"Unsupported datasource type: '{ds_type}' in {path}")

    return model_class(**yaml_data)

  def _call_prometheus_executor(self, name: str):
    pass

  def execute(self):
    for d_source in self.datasources:
      config = self._prepare_datasource(d_source.name)
      executor_fn = self.datasource_executors.get(config.type)
      executor_fn(d_source.name)
