import os
import yaml
import sys

from pathlib import Path
from pydantic import ValidationError

from base_modules.models.d2d_pipeline import D2DPipelineConfig

class Processor:
  def __init__(self, config_path: str):
    self.config = self._load_and_validate_config(config_path=config_path)

  def _load_and_validate_config(self, config_path: str) -> D2DPipelineConfig:
    if not Path(config_path).exists():
      print(f"❌ Config file not found: {config_path}")
      sys.exit(1)

    try:
      with open(config_path, 'r') as f:
        yaml_data = yaml.safe_load(f)

      config = D2DPipelineConfig(**yaml_data)
      config.config_file_dir = os.path.dirname(os.path.abspath(config_path))
      
      return config

    except ValidationError as e:
      print(f"❌ Invalid config file:")
      for error in e.errors():
        print(f"   - {error['loc']}: {error['msg']}")
      sys.exit(1)

  def execute(self):
    pass
