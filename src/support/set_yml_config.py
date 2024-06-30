import yaml
from roboflow import Roboflow
import os
import shutil
import sys
from get_secrets import get_roboflow_secrets

index = str(sys.argv[2])
api_key, workspace_name , project_name, download_version, model_version, robo_path  = get_roboflow_secrets(index)

term_size = os.get_terminal_size()
print('_' * term_size.columns)

rf = Roboflow(api_key=api_key)

auto_run = str(sys.argv[1])

def downoad_dataset(rf):
    # Specify path
    path = robo_path
    
    # Check whether the specified
    # path exists or not
    isExist = os.path.exists(path)

    if isExist and auto_run == "False":
        while True:
            ask1 = input('\t> Dataset already exsists would you like to use the exsisting dataset ([y],n)?')
            if ask1 == 'n':
                print("\t> Deleting current dataset and installing requested dataset\n")
                try:
                    shutil.rmtree(path=path)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
       
                project = rf.workspace(workspace_name).project(project_name)
                dataset = project.version(download_version).download(model_version)

                break
            
            elif ask1 == 'y':
                print('\t> Continuting with current dataset\n')
                project = rf.workspace(workspace_name).project(project_name)
                dataset = project.version(download_version).download(model_version)
                break
            else:
                print('invalid answer')
    else:
        if isExist:
            try:
                shutil.rmtree(path=path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        project = rf.workspace(workspace_name).project(project_name)
        dataset = project.version(download_version).download(model_version)
        
        
    return dataset

def get_nc(dataset):
    with open(dataset.location + "/data.yaml", 'r') as stream:
        num_classes = str(yaml.safe_load(stream)['nc'])

    return num_classes

def set_nc(nc):
    with open("yolov5/models/yolov5s.yaml", 'r') as f:
        doc = yaml.unsafe_load(f)

    doc['nc'] = nc
    with open("yolov5/models/yolov5s.yaml", 'w') as f:
        yaml.dump(doc, f, sort_keys=False, default_flow_style=True)


# need to change the data.yaml file in the dataset from:
# test: ../test/images
# train: my_folder/train/images
# val: my_folder/valid/images
# 
# to this
#
# test: ../my_folder/test/images
# train: ../my_folder/train/images
# val: ../my_folder/valid/images
def change_data_yaml():
    with open(robo_path + "/data.yaml", 'r') as f:
        doc = yaml.unsafe_load(f)

    doc['test'] = '../' + robo_path + '/test/images'
    doc['train'] = '../' + robo_path + '/train/images'
    doc['val'] = '../' + robo_path + '/valid/images'
    with open(robo_path + "/data.yaml", 'w') as f:
        yaml.dump(doc, f, sort_keys=False, default_flow_style=True)


dataset = downoad_dataset(rf=rf)
nc = get_nc(dataset=dataset)
set_nc(nc=nc)
change_data_yaml()

print('_' * term_size.columns)
print(f"\n\t> Number of detection options : {nc}")
print(f"\n\t> Imports and yaml edits for yolo & roboflow are complete")


