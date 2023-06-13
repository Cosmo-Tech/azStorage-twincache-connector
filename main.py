# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.
import logging
import os
import sys
import csv
import copy
import ast

from azstorage_twincache_connector.storage_connector import StorageConnector
from CosmoTech_Acceleration_Library.Modelops.core.io.model_importer import ModelImporter


main_logger_name = "azStorageTwincacheConnector_main"

env_var_required = ["AZURE_CLIENT_ID", "AZURE_TENANT_ID", "AZURE_CLIENT_SECRET",
                    "ACCOUNT_NAME", "CONTAINER_NAME", "STORAGE_PATH",
                    "TWIN_CACHE_HOST", "TWIN_CACHE_PORT", "TWIN_CACHE_NAME"]

missing_env_vars = []

ST_DETECT = [('source', 'target'), ('src', 'dest')]


def check_env_var():
    """
    Check if all required environment variables are specified
    """
    for env_var in env_var_required:
        if env_var not in os.environ:
            missing_env_vars.append(env_var)


def extend_name(file_path, extend):
    path, extention = file_path.rsplit('.', 1)
    return path + extend + '.' + extention


def transform_header(header):
    return set(map(lambda h: h.split('.')[0], header))


def infer(s):
    try:
        return ast.literal_eval(s)
    except Exception:
        return str(s)


def transform(reader):
    for row in reader:
        new_msg = copy.deepcopy(row)
        for j in row:
            if row[j] in (None, ''):
                new_msg.pop(j)
                continue
            if '.' in j:
                # infer type
                typed_row = infer(row[j])
                map_split = j.split('.')
                if map_split[0] not in new_msg:
                    new_msg[map_split[0]] = {}
                new_msg[map_split[0]][map_split[1]] = typed_row
                new_msg.pop(j)
            elif j in [src for src, dest in ST_DETECT[1:]]:
                new_msg['source'] = new_msg[j]
                new_msg.pop(j)
            elif j in [dest for src, dest in ST_DETECT[1:]]:
                new_msg['target'] = new_msg[j]
                new_msg.pop(j)
        yield new_msg


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
            output_file_path = os.path.join(r, 'output', filz)
            os.makedirs(os.path.join(r, 'output'), exist_ok=True)
            with open(file_path) as f, open(output_file_path, 'w') as out:
                csv_r = csv.DictReader(f)
                new_header = list(transform_header(csv_r.fieldnames))

                m = list(map(lambda st: st[0] in new_header and st[1] in new_header, ST_DETECT))
                if any(m):
                    print(f'{filz} is rel')
                    src, dest = [val for use, val in zip(m, ST_DETECT) if use][0]
                    new_header.pop(new_header.index(src))
                    new_header.insert(0, 'source')
                    new_header.pop(new_header.index(dest))
                    new_header.insert(1, 'target')
                    rels.append(output_file_path)
                else:
                    print(f'{filz} is twin')
                    new_header.insert(0, new_header.pop(new_header.index('id')))
                    twins.append(output_file_path)

                csv_w = csv.DictWriter(out, new_header)
                csv_w.writeheader()
                csv_w.writerows(transform(csv_r))

    twingraph = ModelImporter(host=twin_cache_host, port=twin_cache_port,
                              name=twin_cache_name,
                              source_url=f'{storage_account_name}/{container_name}', graph_rotation=twin_cache_rotation,
                              password=twin_cache_password)
    twingraph.bulk_import(twins, rels)
