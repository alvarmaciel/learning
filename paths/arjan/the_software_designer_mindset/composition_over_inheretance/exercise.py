from dataclasses import dataclass
from cloudengine import CloudProvider
from cloudengine.google import GoogleAuth

BUCKET_NAME="video-backup.arjancodes.com"
REGION="eu-west-1c"

@dataclass
class ACCloud:
    cloud_provider: CloudProvider
    bucket_name: str

    def find_files(self, query: str, max_result: int) -> list[str]:
        response = self.cloud_provider.filter_by_query(
            bucket=self.bucket_name, query=query, max=max_result
        )
        return response["result"]["data"][0]
