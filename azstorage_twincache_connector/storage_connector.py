# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.
import logging
import os
import tempfile

from azure.identity import EnvironmentCredential
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger(__name__)


class StorageConnector:
    """
    Connector class to fetch data from Azure Storage account
    """

    def __init__(self, account_name: str = "", container_name: str = "", storage_path: str = ""):
        self.account_name = account_name
        self.container_name = container_name
        self.storage_path = storage_path
        self.blobClient = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net/",
                                            credential=EnvironmentCredential()).get_container_client(container_name)

    def list_files(self):
        return self.blobClient.list_blobs(self.storage_path)

    def download_files(self) -> str:
        tempdir = tempfile.mkdtemp()
        print("Getting blobs...")
        for b in self.blobClient.list_blobs(self.storage_path):
            print(f'Downloading "{b.name}"')
            os.makedirs(os.path.join(tempdir, os.path.dirname(b.name)), exist_ok=True)
            with open(os.path.join(tempdir, b.name), 'wb') as f:
                f.write(self.blobClient.download_blob(b.name).readall())
        return tempdir


