# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.

set -x

docker run \
--network="host" \
--env-file="./docker_envvars"
azStorage-twincache-connector
