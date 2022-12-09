# Azure Storage -> Cosmo Tech Twin Cache connector

The aim of this project is to read data from an Azure storage and store data into Cosmo Tech Twin Cache solution

## Changelog

### Version 1.0.1-rc

#### Features

- Read Azure Storage blob files regarding environment variables
- Store data into Cosmo Tech Twin Cache instance
- Data rotation is handled

## Environment variables :

Here is the list of environment variables:

- **AZURE_CLIENT_ID** : the Azure client id (can be found under the App registration screen)
- **AZURE_TENANT_ID** : the Azure Tenant id (can be found under the App registration screen)
- **AZURE_CLIENT_SECRET** : the app client secret (an already created secret can not be retrieved, thus it must be asked from its creator or a new one should be created)
- **ACCOUNT_NAME** : the targeted storage account name
- **CONTAINER_NAME** : the targeted container name
- **STORAGE_PATH** : the targeted file path
- **TWIN_CACHE_HOST**: the twin cache host
- **TWIN_CACHE_PORT**: the twin cache port
- **TWIN_CACHE_NAME**: the twin cache key name where data will be stored
- **TWIN_CACHE_ROTATION**: defined the data rotation (a.k.a. the amount of keys to keep until data is overwritten) (default 1)
- **TWIN_CACHE_PASSWORD**: default account/user password (default None)

## Log level

Default log level defined is "INFO".
We use the logging API [logging](https://docs.python.org/3/library/logging.html).
You can change the log level by setting an environment variable named: **LOG_LEVEL**.
Log levels used for identifying the severity of an event. Log levels are organized from most specific to least:

- CRITICAL
- ERROR
- WARNING
- INFO
- DEBUG
- NOTSET

## How to run your image locally

### Build the docker image

`docker build -t azstorage-twincache-connector .`

### Run the docker image

Fill the file docker_envvars with your information:

```
AZURE_CLIENT_ID=<<azure_client_id>>
AZURE_TENANT_ID=<azure_tenant_id>
AZURE_CLIENT_SECRET=<azure_client_secret>
ACCOUNT_NAME=<storage_account_name>
CONTAINER_NAME=<storage_container_name>
STORAGE_PATH=<storage_path>
TWIN_CACHE_HOST=<twin_cache_host>
TWIN_CACHE_NAME=<twin_cache_name>
TWIN_CACHE_PORT=<twin_cache_port>
TWIN_CACHE_PASSWORD=<twin_cache_password>
TWIN_CACHE_ROTATION=1
LOG_LEVEL=DEBUG
```

Then run:

`./run.sh`

**N.B:**

- Default log level is set to 'debug'
- Default graph rotation is set to 1

## Data format

Data format authorized is CSV files. 
The azStorage-twincache-connector will fetch all data regarding <ACCOUNT_NAME> <CONTAINER_NAME> and <STORAGE_PATH>, read all csv files.

The connector will read CSV files header and check if src is present as header in order to discriminate CSV files twins and CSV files relationships.

Bulk insert is based on [redisgraph-bulk-loader](https://github.com/RedisGraph/redisgraph-bulk-loader)

**N.B:**
In the current version (1.0.1-rc), the schema enforcement is not handled, so you should respect the default format, i.e:
- for Twin CSV files: See [node-identifiers](https://github.com/RedisGraph/redisgraph-bulk-loader#node-identifiers)
  - the first column of the file should be the twin id (preferred header name: id) 
- for Relationships CSV files: See [relationships-identifiers](https://github.com/RedisGraph/redisgraph-bulk-loader#relationship-files)
  - the first column is the relationship source id (preferred header name: src) 
  - the second column is the relationship destination id (preferred header name: dest)









