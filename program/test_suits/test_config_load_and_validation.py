from processor.processor import Processor
from test_suits.global_test_config import TEST_CONFIG_PATH


def test_load_and_validate_config():
  processor = Processor(TEST_CONFIG_PATH)
  assert processor.config is not None
  assert processor.config.config_file_dir != ""
  print(f"\n✅ config_file_dir: {processor.config.config_file_dir}")
  print(f"✅ datasources: {processor.config.datasources}")
