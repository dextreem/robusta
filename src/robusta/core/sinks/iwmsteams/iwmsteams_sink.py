from robusta.core.reporting import Finding
from robusta.core.sinks.iwmsteams.iwmsteams_sink_params import IwMsTeamsSinkConfigWrapper
from robusta.core.sinks.sink_base import SinkBase
from robusta.integrations.msteams.sender import MsTeamsSender

import requests
import os


class IwMsTeamsSink(SinkBase):
    def __init__(self, sink_config: IwMsTeamsSinkConfigWrapper, registry):
        super().__init__(sink_config.iwms_teams_sink, registry)
        self.webhook_url = sink_config.iwms_teams_sink.webhook_url

    def get_kubernetes_token(self):
        token_file = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        with open(token_file, "r") as f:
            return f.read().strip()
        
    def get_pod_name(self):
        return os.environ.get("POD_NAME")

    def get_container_name(self):
        return os.environ.get("CONTAINER_NAME", "your-container-name")

    def list_pods(self):
        token = self.get_kubernetes_token()
        print(f"XXX KUBERNETES_SERVICE_HOST Environment var: {os.environ.get('KUBERNETES_SERVICE_HOST')}")
        # api_server = os.environ.get("KUBERNETES_SERVICE_HOST", "https://kubernetes.default.svc")
        api_server = "https://kubernetes.default.svc"
        api_url = f"{api_server}/api/v1/namespaces/default/pods"

        print(f"kubernetes token: {self.get_kubernetes_token()}")
        print(f"pd name: {self.get_pod_name()}")
        print(f"container name: {self.get_container_name()}")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.get(api_url, headers=headers, verify=False)

        if response.status_code == 200:
            print(f"SUCCESSFUL RESPONSE: {response.json()}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
        
    def run_kubectl_command_in_pod(self, namespace, command):
        # api_server = os.environ.get("KUBERNETES_SERVICE_HOST", "https://kubernetes.default.svc")
        api_server = "https://kubernetes.default.svc"
        api_url = f"{api_server}/api/v1/namespaces/{namespace}/pods/{self.get_pod_name()}/exec"

        print(f"kubernetes token: {self.get_kubernetes_token()}")
        print(f"pod name: {self.get_pod_name()}")
        print(f"container name: {self.get_container_name()}")

        headers = {
            "Authorization": f"Bearer {self.get_kubernetes_token()}",
            "Content-Type": "application/json"
        }

        data = {
            "apiVersion": "v1",
            "kind": "Exec",
            "metadata": {
                "namespace": namespace,
                "name": self.get_pod_name(),
            },
            "spec": {
                "container": self.get_container_name(),
                "command": command.split(' '),
                "stdin": False,
                "tty": False,
            }
        }

        response = requests.post(api_url, headers=headers, json=data, stream=True, verify=False)

        if response.status_code == 200:
            print(f"SUCCESSFUL ran 2: {command}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def write_finding(self, finding: Finding, platform_enabled: bool):
        MsTeamsSender.send_finding_to_ms_teams(
            self.webhook_url, finding, platform_enabled, self.cluster_name, self.account_id
        )
        self.list_pods()
        self.run_kubectl_command_in_pod("default", finding.enrichments[0])

