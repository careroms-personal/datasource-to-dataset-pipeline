import pandas as pd

from pydantic import BaseModel
from typing import Annotated, Any, List, Union
from pydantic import Field

from base_modules.models.datasources.prometheus import PrometheusDatasourceConfig


class DatasourceResult(BaseModel):
  type_: str
  name: str
  df_results: List[pd.DataFrame]
  df_jsons: List[Any]

  model_config = {"arbitrary_types_allowed": True}


DatasourceConfig = Annotated[
  Union[PrometheusDatasourceConfig],
  Field(discriminator="type")
]


class DatasourcesConfig(BaseModel):
  type_: str
  config: DatasourceConfig
