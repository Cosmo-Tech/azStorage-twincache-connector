# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.
import logging
import os
import sys


main_logger_name = "azStorageTwincacheConnector_main"

env_var_required = ["AZURE_CLIENT_ID", "AZURE_TENANT_ID", "AZURE_CLIENT_SECRET", "STORAGE_NAME", "STORAGE_PATH",
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
        storage_account_name = os.getenv("STORAGE_NAME")
        storage_blob_path = os.getenv("STORAGE_PATH")
        twin_cache_host = os.getenv("TWIN_CACHE_HOST")
        twin_cache_port = os.getenv("TWIN_CACHE_PORT")
        twin_cache_name = os.getenv("TWIN_CACHE_NAME")
        twin_cache_rotation = os.getenv("TWIN_CACHE_ROTATION")
        twin_cache_password = os.getenv("TWIN_CACHE_PASSWORD")
    else:
        raise Exception(f"Missing environment variables named {missing_env_vars}")
