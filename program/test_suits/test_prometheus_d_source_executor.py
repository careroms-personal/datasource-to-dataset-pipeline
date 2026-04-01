from processor.processor import Processor
from processor.executors.datasources.executor import DatasourcesExecutor
from processor.executors.datasources.prometheus_executor import PrometheusDatasourceExecutor
from base_modules.models.datasources.prometheus import PrometheusDatasourceConfig
from test_suits.global_test_config import TEST_CONFIG_PATH


def _make_prometheus_executor(processor: Processor) -> PrometheusDatasourceExecutor:
  """Helper — returns a PrometheusDatasourceExecutor for the first prometheus datasource."""
  config_file_dir = processor.d2d_pipeline_config.config_file_dir
  pipeline = processor.d2d_pipeline_config.pipelines[0]
  ds_executor = DatasourcesExecutor(config_file_dir, pipeline)

  for d_source in pipeline.datasources:
    config = ds_executor._prepare_datasource(d_source.name)
    if isinstance(config, PrometheusDatasourceConfig):
      return PrometheusDatasourceExecutor(config)

  raise RuntimeError("No prometheus datasource found in test config")


def test_build_queries_slicing():
  processor = Processor(TEST_CONFIG_PATH)
  prom_executor = _make_prometheus_executor(processor)
  prom_executor._build_queries()

  print(f"\n✅ Total query configs built: {len(prom_executor.query_configs)}")

  range_queries = [qc for qc in prom_executor.query_configs if qc.query_type == "query_range"]
  assert len(range_queries) > 0, "Expected at least one range query slice"
  for qc in range_queries:
    assert qc.start is not None
    assert qc.end is not None
    assert qc.start < qc.end


def test_prometheus_query():
  processor = Processor(TEST_CONFIG_PATH)
  prom_executor = _make_prometheus_executor(processor)
  prom_executor._build_queries()

  single_queries = [qc for qc in prom_executor.query_configs if qc.query_type == "query"]
  assert len(single_queries) > 0, "Expected at least one single query"

  for qc in single_queries:
    print(f"\n🔍 Querying: {qc.name}")
    result = prom_executor._query(qc)
    print(f"   series: {len(result)}")
    print(f"   sample: {result[0] if result else 'empty'}")
    assert isinstance(result, list)


def test_prometheus_query_range():
  processor = Processor(TEST_CONFIG_PATH)
  prom_executor = _make_prometheus_executor(processor)
  prom_executor._build_queries()

  range_queries = [qc for qc in prom_executor.query_configs if qc.query_type == "query_range"]
  assert len(range_queries) > 0, "Expected at least one range query slice"

  # test only first slice to avoid flooding
  qc = range_queries[0]
  print(f"\n🔍 Range query: {qc.name} | slice [{qc.start} → {qc.end}]")
  result = prom_executor._query_range(qc)
  print(f"   series: {len(result)}")
  print(f"   sample: {result[0] if result else 'empty'}")
  assert isinstance(result, list)


def test_prometheus_execute_full():
  processor = Processor(TEST_CONFIG_PATH)
  prom_executor = _make_prometheus_executor(processor)
  results = prom_executor.execute()

  print(f"\n✅ Prometheus executor results:")
  for query_name, data in results.items():
    print(f"   [{query_name}] total series: {len(data)}")
    print(f"   sample: {data[0] if data else 'empty'}")

  assert len(results) > 0
