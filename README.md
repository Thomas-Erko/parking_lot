# Parking Lot Project


## File Descriptions

#### Home
- script_1_yolov5_setup.sh
    - Inital script to import yolo, requirments, and roboflow training 
    - Also changes configurations in preperation for fine tuning

    **/src**
    - None

    **/src/support**
    - src/support/set_yml_config.py
        - Supports the cript_1_yolov5_setup.sh script by:
        - Importing the roboflow datasets 
        - Retriving the nc (number of choices) for the model
        - Changing the nc in the yolov5 model of choice