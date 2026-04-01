from base_modules.base_executor import BaseExecutor
from base_modules.models.d2d_pipeline import D2DPipelineConfig
from .exporters.csv_exporter import csv_export
from .exporters.json_exporter import json_export

class OutputExecutor(BaseExecutor):
  def __init__(self, d2d_pipeline_config: D2DPipelineConfig):
    pass

  def _export_data(self):
    pass

  def execute(self):
    pass