from robusta.core.sinks.sink_base_params import SinkBaseParams
from robusta.core.sinks.sink_config import SinkConfigBase


class IwMsTeamsSinkParams(SinkBaseParams):
    webhook_url: str


class IwMsTeamsSinkConfigWrapper(SinkConfigBase):
    ms_teams_sink: IwMsTeamsSinkParams

    def get_params(self) -> SinkBaseParams:
        return self.ms_teams_sink
