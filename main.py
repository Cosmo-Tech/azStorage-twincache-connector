# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.
import logging
import os
import sys
import csv

from azstorage_twincache_connector.storage_connector import StorageConnector
from CosmoTech_Acceleration_Library.Modelops.core.io.model_importer import ModelImporter


main_logger_name = "azStorageTwincacheConnector_main"

env_var_required = ["AZURE_CLIENT_ID", "AZURE_TENANT_ID", "AZURE_CLIENT_SECRET",
                    "ACCOUNT_NAME", "CONTAINER_NAME", "STORAGE_PATH",
                    "TWIN_CACHE_HOST", "TWIN_CACHE_PORT", "TWIN_CACHE_NAME"]

missing_env_vars = []


def check_env_var():
    """
    Check if all required environment variables are specified
    """
    for env_var in env_var_required:
        if env_var not in os.environ:
            missing_env_vars.append(env_var)


if __name__ == "__main__":

    log_level_name = os.getenv("LOG_LEVEL") if "LOG_LEVEL" in os.environ else "INFO"
    log_level = logging.getLevelName(log_level_name)
    logging.basicConfig(stream=sys.stdout, level=log_level,
                        format='%(levelname)s(%(name)s) - %(asctime)s - %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S')
    logger = logging.getLogger(__name__)

    check_env_var()
    if not missing_env_vars:
        storage_account_name = os.getenv("ACCOUNT_NAME")
        container_name = os.getenv("CONTAINER_NAME")
        storage_path = os.getenv("STORAGE_PATH")
        twin_cache_host = os.getenv("TWIN_CACHE_HOST")
        twin_cache_port = os.getenv("TWIN_CACHE_PORT")
        twin_cache_name = os.getenv("TWIN_CACHE_NAME")
        twin_cache_rotation = int(os.getenv("TWIN_CACHE_ROTATION", 3))
        twin_cache_password = os.getenv("TWIN_CACHE_PASSWORD")
    else:
        raise Exception(f"Missing environment variables named {missing_env_vars}")

    # download files
    storage_connector = StorageConnector(account_name=storage_account_name,
                                         container_name=container_name,
                                         storage_path=storage_path)
    dataset_folder = storage_connector.download_files()
    print(f"Dataset is in {dataset_folder}")

    twins = []
    rels = []
    for r, d, files in os.walk(dataset_folder):
        for filz in files:
            file_path = os.path.join(r, filz)
            with open(file_path) as f:
                h = csv.DictReader(f).fieldnames
                if 'src' in h:
                    print(f'{filz} is rel')
                    rels.append(file_path)
                else:
                    print(f'{filz} is twin')
                    twins.append(file_path)

    twingraph = ModelImporter(host=twin_cache_host, port=twin_cache_port,
                              name=twin_cache_name,
                              source_url=f'{storage_account_name}/{container_name}', graph_rotation=twin_cache_rotation,
                              password=twin_cache_password)
    twingraph.bulk_import(twins, rels)
