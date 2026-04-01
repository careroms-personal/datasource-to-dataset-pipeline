from processor.processor import Processor
from processor.executors.datasources.executor import DatasourcesExecutor
from processor.executors.datasources.prometheus_executor import PrometheusDatasourceExecutor
from base_modules.models.datasources.prometheus import PrometheusDatasourceConfig
from test_suits.global_test_config import TEST_CONFIG_PATH


def test_datasource_executor_prepare():
  processor = Processor(TEST_CONFIG_PATH)
  executor = DatasourcesExecutor(processor.config)

  for d_source in processor.config.datasources:
    config = executor._prepare_datasource(d_source.name)
    print(f"\n✅ Loaded datasource: {d_source.name} | type: {config.type}")
    print(config.model_dump())


def test_build_queries_slicing():
  processor = Processor(TEST_CONFIG_PATH)
  ds_executor = DatasourcesExecutor(processor.config)

  for d_source in processor.config.datasources:
    config = ds_executor._prepare_datasource(d_source.name)

    if isinstance(config, PrometheusDatasourceConfig):
      prom_executor = PrometheusDatasourceExecutor(config)
      prom_executor._build_queries()

      print(f"\n✅ Datasource: {d_source.name}")
      print(f"   Total query configs built: {len(prom_executor.query_configs)}")

      for qc in prom_executor.query_configs:
        print(f"\n   [{qc.query_type}] {qc.name}")
        print(f"   promql: {qc.promql}")
        if qc.query_type == "query_range":
          print(f"   start : {qc.start}")
          print(f"   end   : {qc.end}")
          print(f"   step  : {qc.step}s")

      range_queries = [qc for qc in prom_executor.query_configs if qc.query_type == "query_range"]
      assert len(range_queries) > 0, "Expected at least one range query slice"
      for qc in range_queries:
        assert qc.start is not None
        assert qc.end is not None
        assert qc.start < qc.end
