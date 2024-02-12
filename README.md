# SDM.SQLgeneration

The SDM.SQLgeneration service is a Python server that generates a **SQL Schema** based on the model description of a **Smart Data Model**. 

It provides an OpenAPI specification with two paths: `/version` and `/generate`.

**Path: `/version`**

- The `/version` path is used to provide clients with version information, including details such as the document, git hash, version, release date, and uptime.

**Path: `/generate`**

- The `/generate` path is a POST operation designed to generate a SQL Schema based on the provided data model.

- Request Body: The API expects a JSON object in the payload with the details of the GitHub URL to the Data Model model.yaml from which the SQL Schema will be generated, along with other necessary details

This service simplifies the generation of SQL Schemas by providing a clear and structured API. It is particularly useful for automating the process of creating SQL Schemas based on data models, thereby streamlining the development and maintenance of databases

# Create a Python Virtual Environement 

Please note that this is a Python 3.11 project, to install it, check this [link](https://www.python.org/downloads/).

To create a virtual environment in Python using the `venv` module, the following command can be executed in the terminal:

```shell
python3 -m venv venv
```
To activate a virtual environment named "venv" in the root path, you can use the following command:

```shell
source venv/bin/activate
```

# Poetry Initialization - Running the Project Locally 

To manage the dependencies in this project and for Python package management, Poetry is used. 

1. **Install Poetry:** 
Execute the following command in the terminal: 

    ```shell
    curl -sSL https://install.python-poetry.org | python -
    ```

2. **Activate the Virtual Environment:**
    Since this project has a virtual environment managed by Poetry, it can be activated using the following command:

    ```shell
    poetry env use 3.11
    poetry shell
    ```

    To deactivate and exit the Poetry Virtual Environment run:
    ```
    exit
    ```

3. **Install Dependencies:**
    If the project's dependencies are not installed, the following command can be used to install them based on the pyproject.toml and poetry.lock files:

    ```shell
    poetry install
    ```
    Another alternative is to use this command: 
    ```shell
    pip install -r requirements.txt
    ```
4. **Exit the virtual environment**: 
Once done, make sure to exit from the virtual environment by running this command:
    ```shell
    deactivate
    ```

# Running the code 
To run the code use the following commands and instructions: 

```
Usage:
  generator.py run (--input FILE) [--output]
  generator.py server [--host HOST] [--port PORT]
  generator.py (-h | --help)
  generator.py --version

Arguments:
  FILE   input file
  PORT   http port used by the service

Options:
  -i, --input FILEIN  description to specify the file to the script
  -o, --output        generate the corresponding output file
  -h, --host HOST     launch the server in the corresponding host
                      [default: 127.0.0.1]
  -p, --port PORT     launch the server in the corresponding port
                      [default: 5500]

  -H, --help          show this help message and exit
  -v, --version       show version and exit
```

# OpenAPI documentation 

the full OpenAPI specification is located under [doc/openapi.yaml](doc/openapi.yaml).

This OpenAPI specification defines two paths`/version` and `/generate`. 

## The `/version` path

- The purpose of the /version path is to provide clients with version information, including details such as the document, git hash, version, release date, and uptime. 
- The API defines an endpoint for retrieving version information. 
- When a `GET` request is sent to the `/version` path, the API returns a JSON object containing details such as the document, git hash, version, release date, and uptime. 
- The API logs relevant information, such as the request for version information, using the provided logger.

## The `/generate` path

- The API is a POST operation at the `/generate` path. 
- It is designed to generate a SQL Schema based on the provided data model. 

Here is the documentation for the API:
- Path: /generate
- Method: POST
- Summary: Generating a SQL Schema
- Request Body: The API expects a JSON object in the payload with the details of the GitHub URL to the Data Model model.yaml from which the SQL Schema will be generated, along with other necessary details.

    Example:
    ```shell
    {
    "url": "https://github.com/your-repo/your-model.yaml",
    "email": "your-email@example.com",
    "tests": 10
    }
    ```
    Responses:
    200 OK: If the request is successful, the API returns the generated SQL Schema.

    Example Response:
    ```shell
    {
    "message": "Generated SQL Schema Here..."
    }
    ```
    - 400 Bad Request: If the request payload is missing or invalid, the API returns an error message.

    Example Response:
    ```shell
    {
    "message": "It is needed to provide a JSON object in the payload with the details of the GitHub URL to the Data Model model.yaml from which you want to generate the SQL Schema"
    }
    ```

- Upon receiving a request, the API logs relevant information, such as the request for generating a SQL Schema from a specific URL. It then validates the provided GitHub URL and, if valid, proceeds to generate the SQL Schema. If the URL is invalid, it returns an error message.

