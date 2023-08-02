from robusta.core.sinks.sink_base_params import SinkBaseParams
from robusta.core.sinks.sink_config import SinkConfigBase


class IwMsTeamsSinkParams(SinkBaseParams):
    webhook_url: str


class IwMsTeamsSinkConfigWrapper(SinkConfigBase):
    iwms_teams_sink: IwMsTeamsSinkParams

    def get_params(self) -> SinkBaseParams:
        return self.iwms_teams_sink
