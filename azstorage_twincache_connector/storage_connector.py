# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.
import logging

from azure.identity import EnvironmentCredential
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger(__name__)


class StorageConnector:
    """
    Connector class to fetch data from Azure Storage account
    """

    def __init__(self, account_name: str = "", container_name: str = ""):
        self.account_name = account_name
        self.container_name = container_name
        self.blobClient = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net/",
                                            credential=EnvironmentCredential()).get_container_client(container_name)

    def list_files(self):
        return self.blobClient.list_blobs()
