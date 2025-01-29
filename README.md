# SDM.SQLgeneration

Python Server to generate a SQL Schema based on the model description of a Smart Data Model.

**Path: `/version`**

- The `/version` path is used to provide clients with version information, including details such as the document, 
git hash, version, release date, and uptime.

**Path: `/generate`**

- Description: A POST operation used to perform the SQL Schema Generation based on a data model.
- Request Body: Expects a JSON payload with details of the data model (link to the model.yaml file in GitHub).

    '''json
    {
      "url": "<url to the model.yaml file>"  
    }'''

# uv initialization - Running the Project Locally 

Please note that this is a **Python 3.13** project. The installation is based on uv, an extremely fast Python package 
and project manager, written in Rust. Please follow the [link](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) 
to install locally.

1. **Activate the virtual environment:**
    It can be activated using the following command:

    ```shell
    uv venv --python 3.13
    ```

    This operation will create the corresponding `.venv` and in case that the version of python is not installed, uv 
    will install the corresponding version of python. After that operation you can activate the virtual environment 
    executing the command:

    ```shell
    source .venv/bin/activate
    ```

2. **Install Dependencies:**
    If the project's dependencies are not installed, the following command can be used to install them based on the pyproject.toml and poetry.lock files:

    ```shell
    uv pip install -r requirements.txt
    ```
    
3. **Deactivate and exit the virtual environment**: 
Once done, make sure to exit from the virtual environment by running this command:

    ```shell
    deactivate
    ```

# Running the code 
To run the code use the following commands and instructions: 

```shell
SDM SQL schema generator

Usage:
  generator.py run (--input FILE) [--output]
  generator.py server [--host HOST] [--port PORT]
  generator.py (-h | --help)
  generator.py --version

Arguments:
  FILE   input file
  PORT   http port used by the service

Options:
  -i, --input FILEIN  specify the RDF turtle file to parser
  -o, --output        generate the corresponding files of the parser RDF turtle file
  -h, --host HOST     launch the server in the corresponding host
                      [default: 127.0.0.1]
  -p, --port PORT     launch the server in the corresponding port
                      [default: 5500]

  -H, --help          show this help message and exit
  -v, --version       show version and exit
```

To run the service, it is needed to define the corresponding full path to the cert and key files in the 
[./common/config.json] file.

## The `/version` path

- The purpose of the /version path is to provide clients with version information, including details such as the document, git hash, version, release date, and uptime. 
- The API defines an endpoint for retrieving version information. 
- When a `GET` request is sent to the `/version` path, the API returns a JSON object containing details such as the document, git hash, version, release date, and uptime. 
- The API logs relevant information, such as the request for version information, using the provided logger.

## The `/generate` path

- The `/generate` path serves as an endpoint for performing the sql generation of a data model. 
- When a `POST` operation is sent to this path, the API expects a JSON payload containing the url of the model.yaml file of the data model in the GitHub (e.g., `https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherObserved/model.yaml`) 
- Upon receiving the request, the API processes the information and generate the corresponding SQL Schema for that model.

Example of a request should be:

```shell
curl -X POST http://localhost:5500/generate \
 -d '{
       "url": "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherObserved/model.yaml"
      }'
```

And the response of the server should be:

```json
{
  "message": "CREATE TYPE WeatherObserved_type AS ENUM ('WeatherObserved');\nCREATE TABLE WeatherObserved (address JSON, airQualityIndex NUMERIC, airQualityIndexForecast NUMERIC, airTemperatureForecast NUMERIC, airTemperatureTSA JSON, alternateName TEXT, aqiMajorPollutant TEXT, aqiMajorPollutantForecast TEXT, areaServed TEXT, atmosphericPressure NUMERIC, dataProvider TEXT, dateCreated TIMESTAMP, dateModified TIMESTAMP, dateObserved TIMESTAMP, description TEXT, dewPoint NUMERIC, diffuseIrradiation NUMERIC, directIrradiation NUMERIC, feelsLikeTemperature NUMERIC, gustSpeed NUMERIC, id TEXT PRIMARY KEY, illuminance NUMERIC, location JSON, name TEXT, owner JSON, precipitation NUMERIC, precipitationForecast NUMERIC, pressureTendency JSON, refPointOfInterest TEXT, relativeHumidity NUMERIC, relativeHumidityForecast NUMERIC, seeAlso JSON, snowHeight NUMERIC, solarRadiation NUMERIC, source TEXT, streamGauge NUMERIC, temperature NUMERIC, type WeatherObserved_type, uVIndexMax NUMERIC, weatherType TEXT, windDirection NUMERIC, windSpeed NUMERIC);"
}
```

# License
These scripts are licensed under Apache License 2.0.
