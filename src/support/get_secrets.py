import json
import sys

def get_value_from_json(json_file, key, sub_key):
   try:
       with open(json_file) as f:
           data = json.load(f)
           return data[key][sub_key]
   except Exception as e:
       print("Error: ", e)

# Getting Values for Roboflow
def get_roboflow_secrets(index):
    api_key = str(get_value_from_json("etc/secrets.json", index, "api_key"))
    workspace_name = str(get_value_from_json("etc/secrets.json", index, "workspace"))
    project_name = str(get_value_from_json("etc/secrets.json", index, "project"))
    download_version = get_value_from_json("etc/secrets.json", index, "download_version")
    model_version = get_value_from_json("etc/secrets.json", index, "model_used")
    robo_path = get_value_from_json("etc/secrets.json", index, "path")

    return api_key, workspace_name, project_name, download_version, model_version, robo_path




