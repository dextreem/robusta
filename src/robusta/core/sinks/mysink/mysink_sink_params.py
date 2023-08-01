from typing import Optional
from urllib.parse import urlparse

from pydantic import validator

from robusta.core.sinks.sink_base_params import SinkBaseParams
from robusta.core.sinks.sink_config import SinkConfigBase


class MysinkSinkParams(SinkBaseParams):
    webhook_url: str


class MysinkSinkConfigWrapper(SinkConfigBase):
    mysink_sink: MysinkSinkParams

    def get_params(self) -> SinkBaseParams:
        return self.mysink_sink
