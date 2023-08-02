from robusta.core.reporting import Finding
from robusta.core.sinks.iwmsteams.iwmsteams_sink_params import IwMsTeamsSinkConfigWrapper
from robusta.core.sinks.sink_base import SinkBase
from robusta.integrations.msteams.sender import MsTeamsSender


class IwMsTeamsSink(SinkBase):
    def __init__(self, sink_config: IwMsTeamsSinkConfigWrapper, registry):
        super().__init__(sink_config.iwms_teams_sink, registry)
        self.webhook_url = sink_config.iwms_teams_sink.webhook_url

    def write_finding(self, finding: Finding, platform_enabled: bool):
        MsTeamsSender.send_finding_to_ms_teams(
            self.webhook_url, finding, platform_enabled, self.cluster_name, self.account_id
        )
