from robusta.core.reporting.base import Finding
from robusta.core.sinks.mysink.mysink_sink_params import MysinkSinkConfigWrapper
from robusta.core.sinks.sink_base import SinkBase

import json


class MysinkSink(SinkBase):
    def __init__(self, sink_config: MysinkSinkConfigWrapper, registry):
        super().__init__(sink_config.mysink_sink, registry)

    def write_finding(self, finding: Finding, platform_enabled: bool):
        print("Hello from the Sink!")
        print(json.dumps(finding))

        f = open("innoweek.txt", "w")
        f.write("Hello from the Sink!")
        f.write(json.dumps(finding))
        f.close()
