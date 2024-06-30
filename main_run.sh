#!/bin/bash

# ________________________________________________________________________________________ #
#                                           Read in user input
# 

auto_run=False

while getopts "fh" flag;
do
    case $flag in
        f) auto_run=True;;
        h) 
        echo -e """\n\nOptions:
        -f: indicates a full run which will not ask for permision before overwriting 
        local folders with the most recent versions of data

        -h: list of flags
        """
        exit 0;;
    esac
done

# ________________________________________________________________________________________ #
#                                           Checks
# 
# This section is used to ensure that the scripts are running in the proper location
#

# Virtual Env Check
#current_venv=$CONDA_DEFAULT_ENV
#expected_venv="parking_lot"
#if [ $current_venv = $expected_venv ]; then 
#    echo -e "\n> Enviroment check: Passed\n"
#else 
#    echo -e "\n> Enviroment Check: Failed"
#    echo -e "\t> Current Enviroment: $current_venv"
#    echo -e "\t> Expected Enviroment: $expected_venv \n" 
#    echo >&2 -e "Enviroment Error: You must be in the '$expected_venv' venv to run this script\n"; exit 1;
#fi 

# Directory Check
current_dir="$(basename $PWD)"
expected_dir="parking_lot"

if [ $current_dir = $expected_dir ]; then 
    echo -e "\n> Directory check: Passed\n"
else 
    echo -e "\n> Directory Check: Failed"
    echo -e "\t> Current Directory: $current_dir"
    echo -e "\t> Expected Directory: $expected_dir \n" 
    echo >&2 -e "Directory Error: You must be in the '$expected_dir' folder to run this script\n"; exit 1;
fi

echo -e "> Installing repo requirments\n"
pip3 install -qr requirements.txt 2>/dev/null   

# User Check
echo "> All checks have passed. YOLO imports and requirment installs will follow."
while [ "$auto_run" = False ]
do
    read -r -p '> Do you want to continue ([y]/n)? ' choice
    case "$choice" in
      n) exit 1;;
      y) break;;
      *) echo 'Response not valid';;
    esac
done


# ________________________________________________________________________________________ #
#                                        Setup For Parking
# echo -e "\n\t \n" 
#
# Setting up the enviroment for the project 

echo -e "\n> Starting Install\n"

# Clone YOLO v5 repo
echo -e "\t> Clone YOLO v5 to $current_dir\n" 
if [ -d yolov5 ] && [ "$auto_run" = False ]; then
    while true
    echo -e "\t> A yolov5 directory already exsists"
    do
        read -e -r -p '        > Would you like to use the present yolov5 dir ([y]/n)? ' choice
        case "$choice" in
        n) rm -rf yolov5
            git clone https://github.com/ultralytics/yolov5 2>/dev/null  
            break;;
        y) break;;
        *) echo -e '\n\t> Response not valid. Please select "y" or "n"\n';;
        esac
    done
else
    if [ -d yolov5 ]; then
        rm -rf yolov5
    fi
    git clone https://github.com/ultralytics/yolov5 2>/dev/null  
fi

echo -e "\n\t> Importing yolo requirments \n" 
# Instaling YOLO Requirments
pip3 install -qr yolov5/requirements.txt #2>/dev/null   

echo -e "\n> Importing finetuning dataset from Roboflow & adjusting .yaml files\n" 
# Imports roboflow and sets nc config in yolo yaml files
python3 src/support/set_yml_config.py $auto_run parking_space


# ________________________________________________________________________________________ #
#                                     Training For Parking
# 
# Fine tuning the model on the data we've pulled in from roboflow

echo -e "\n> Tranining model\n"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
# Start training
cd "yolov5" 
python3 train.py --img 640 --batch 2 --epochs 300 --data ../Car-Space-Find-2/data.yaml --cfg ./models/yolov5s.yaml --weights yolov5s.pt --name yolov5s_results  --cache
cd ".."

if [ -d yolov5_parking_spot ]; then
    rm -rf yolov5_parking_spot
fi

mv yolov5/ yolov5_parking_spot

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -


# ________________________________________________________________________________________ #
#                                        Setup For People
# echo -e "\n\t \n" 
#
# Setting up the enviroment for the project 

echo -e "\n> Starting Install\n"

# Clone YOLO v5 repo
echo -e "\t> Clone YOLO v5 to $current_dir\n" 
if [ -d yolov5 ] && [ "$auto_run" = False ]; then
    while true
    echo -e "\t> A yolov5 directory already exsists"
    do
        read -e -r -p '        > Would you like to use the present yolov5 dir ([y]/n)? ' choice
        case "$choice" in
        n) rm -rf yolov5
            git clone https://github.com/ultralytics/yolov5 2>/dev/null  
            break;;
        y) break;;
        *) echo -e '\n\t> Response not valid. Please select "y" or "n"\n';;
        esac
    done
else
    if [ -d yolov5 ]; then
        rm -rf yolov5
    fi
    git clone https://github.com/ultralytics/yolov5 2>/dev/null  
fi

echo -e "\n\t> Importing yolo requirments \n" 
# Instaling YOLO Requirments
pip3 install -qr yolov5/requirements.txt 2>/dev/null   

echo -e "\n> Importing finetuning dataset from Roboflow & adjusting .yaml files\n" 
# Imports roboflow and sets nc config in yolo yaml files
python3 src/support/set_yml_config.py $auto_run person

# ________________________________________________________________________________________ #
#                                     Training For People
# 
# Fine tuning the model on the data we've pulled in from roboflow

echo -e "\n> Tranining model\n"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
# Start training
cd "yolov5" 
python3 train.py --img 640 --batch 2 --epochs 300 --data ../Parking-Detection-2/data.yaml --cfg ./models/yolov5s.yaml --weights yolov5s.pt --name yolov5s_results  --cache
cd ".."

if [ -d yolov5_person ]; then
    rm -rf yolov5_person
fi
mv yolov5/ yolov5_person

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
