import os
import re
import sys 
import requests
import ruamel.yaml as yaml


# Regular expression pattern to extract owner, repository, branch, and file path
github_url_pattern = r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)"


def convert_to_raw_github_url(input_url):   
    match = re.match(github_url_pattern, input_url)
    
    if match:
        owner = match.group(1)
        repository = match.group(2)
        branch = match.group(3)
        file_path = match.group(4)
        raw_github_url = f"https://raw.githubusercontent.com/{owner}/{repository}/{branch}/{file_path}"
        return raw_github_url
    else:
        print("Invalid GitHub URL format")


def open_yaml(file_url):
    try:
        _, file_extension = os.path.splitext(file_url)
        if file_extension.lower() != '.yaml':
            print("Invalid file format. The file should have a .yaml extension.")

        if file_url.startswith("http"):
            if re.match(github_url_pattern, file_url):
                raw_github_url = convert_to_raw_github_url(file_url)
                response = requests.get(raw_github_url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                return yaml.safe_load(response.content.decode('utf-8'))
            else:
                response = requests.get(file_url)
                response.raise_for_status()
                return yaml.safe_load(response.content.decode('utf-8'))
        else:
            with open(file_url, "r") as file:
                return yaml.safe_load(file)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch content from URL: {e}")
    except Exception as e:
        print(f"Error: {e}")


def yaml_to_postgresql_schema(yamlfile)-> dict:
    """
    Generate a PostgreSQL schema SQL script from the model.yaml representation of a Smart Data Model.

    This function takes a dictionary representing a model.yaml file, extracts relevant information,
    and creates a PostgreSQL schema SQL script.

    Args:
        yamlfile (dict): A dictionary representing the content of a model.yaml file.

    Returns:
        str: A string containing the PostgreSQL schema SQL script.
    """
    # Get the entity name
    entity = list(yamlfile.keys())[0]

    # Initialize SQL schema statements
    sql_schema_statements = []
    sql_type_statement = []

    sql_data_types= ""

    # Define format mappings for YAML formats to postgreSQL Schema types
    type_mapping = {
        "string": "TEXT",
        "integer": "INTEGER",
        "number": "NUMERIC",
        "boolean": "BOOLEAN",
        "object": "JSON",
        "array": "JSON",
    }

    # Define format mappings for YAML formats to postgreSQL Schema types
    format_mapping = {
        "date-time": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "uri": "TEXT",
        "email": "TEXT",
        "idn-email": "TEXT",
        "hostname": "TEXT",
        "duration": "TEXT"
    }

    # Start by creating the table
    table_create_statement = f"CREATE TABLE {entity} ("

    for key, value in yamlfile[entity]["properties"].items():
        field_type = "JSON"  # Default to JSON if type is not defined

        # Field type mapping
        if "type" in value:
            if "format" in value:
                # format type mapping (format overrides type)
                field_type = format_mapping.get(value["format"])
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")
            
            elif "enum" in value:
                enum_values = value["enum"]
                enum_values = [str(element) for element in enum_values]
                if key == "type":
                    field_type = f"{entity}_type"
                else:
                    field_type = f"{key}_type"
                # create sql create type statment
                sql_type_statement.append(f"CREATE TYPE {field_type} AS ENUM ({','.join(map(repr, enum_values))});")

                sql_data_types += "CREATE TYPE " + field_type + " AS ENUM ("
                sql_data_types += f"{','.join(map(repr, enum_values))}"
                sql_data_types += ");<br>"

                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")

            else:
                field_type = type_mapping.get(value["type"])
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")
        elif "oneOf" in value:
            field_type = "JSON"
            sql_schema_statements.append(f"{key} {field_type}")

        # Handle the case when "allOf" exists
        if key == "allOf" and isinstance(value, list):
            for values in value:
                for sub_key, sub_value in values.items():
                    if isinstance(sub_value, dict):
                        if "format" in sub_value:
                            sub_field_type = format_mapping.get(sub_value["format"])
                            sql_schema_statements.append(f"{sub_key} {sub_field_type}")
                        if "type" in sub_value:
                            sub_field_type = type_mapping.get(sub_value["type"])
                            sql_schema_statements.append(f"{sub_key} {sub_field_type}")
        
        if key == "id":
            field_type = "TEXT PRIMARY KEY"
            # add attribute to the SQL schema statement
            sql_schema_statements.append(f"{key} {field_type}")

    # Complete the CREATE TABLE statement
    table_create_statement += ", ".join(sql_schema_statements)
    table_create_statement += ");"
    # PostgreSQL schema 
    result = sql_data_types + "<br>" + table_create_statement

    print(result)

    return result

##########################################
#          Executing the code            #
##########################################

#model_yaml_url = "https://raw.githubusercontent.com/smart-data-models/dataModel.UrbanMobility/master/TransitManagement/model.yaml"

# get the argument variable 
model_yaml_url = sys.argv[1]

model_json = open_yaml(model_yaml_url)

yaml_to_postgresql_schema(model_json)


