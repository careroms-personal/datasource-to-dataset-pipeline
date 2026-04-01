from base_modules.base_executor import BaseExecutor
from base_modules.models.d2d_pipeline import D2DPipelineConfig

class PrometheusDatasourceExecutor(BaseExecutor):
  def __init__(self, d2d_pipeline_config: D2DPipelineConfig):
    self.d2d_pipeline_config = d2d_pipeline_config

  def _start_end_convert(self):
    pass

  def _cilent(self):
    pass

  def _query(self):
    pass

  def _query_range(self):
    pass

  def execute(self):
    pass