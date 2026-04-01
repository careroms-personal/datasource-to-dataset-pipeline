from processor.processor import Processor
from processor.executors.datasources.executor import DatasourcesExecutor
from test_suits.global_test_config import TEST_CONFIG_PATH


def _make_executor(processor: Processor) -> tuple:
  """Helper — returns (config_file_dir, first pipeline, DatasourcesExecutor)."""
  config_file_dir = processor.d2d_pipeline_config.config_file_dir

  pipeline = processor.d2d_pipeline_config.pipelines[0]

  executor = DatasourcesExecutor(config_file_dir, pipeline)

  return config_file_dir, pipeline, executor


def test_datasource_executor_prepare():
  processor = Processor(TEST_CONFIG_PATH)
  _, pipeline, executor = _make_executor(processor)

  for d_source in pipeline.datasources:
    config = executor._prepare_datasource(d_source.name)

    print(f"\n✅ Loaded datasource: {d_source.name} | type: {config.type}")
    print(config.model_dump())


def test_datasources_executor_full():
  processor = Processor(TEST_CONFIG_PATH)
  _, _, ds_executor = _make_executor(processor)

  results = ds_executor.execute()

  print(f"\n✅ Datasources executor results:")

  for name, data in results.items():
    print(f"   [{name}] total results: {len(data)}")
    # print(f"   [{name}]: [{data}]")

  assert len(results) > 0
