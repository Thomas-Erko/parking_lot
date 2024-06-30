import torch 
import numpy as np
import cv2
import streamlit as st


class Detector():
    
    def __init__(self, vid_path, model_path):
        # Initilization of class and key values 

        self.vid = vid_path
        self.model = model_path
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def get_mdl(self):
        self.model = torch.hub.load('../../yolov5', 'custom', path=self.model, source='local',force_reload=True) 
        #self.model = torch.hub.load('yolov5', 'custom', path=self.model, source='local',force_reload=True) 


    def plot_box(self, results, frame):
        labels, cord = results

        x_shape = frame.shape[1]
        y_shape = frame.shape[0]

        for i in range(len(labels)):
            row = cord[i]
            if row[4] >= 0.3:
                x1 = int(row[0]*x_shape)
                y1 = int(row[1]*y_shape)
                x2 = int(row[2]*x_shape)
                y2 = int(row[3]*y_shape)

                clr = (0, 255, 0)

                cv2.rectangle(frame, (x1,y1), (x2, y2), clr, 2)
        
        return frame
    
    def score_frame(self, frame):
        self.model.to(self.device)
        frame= [frame]
        results = self.model(frame)
        labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

        return labels, cords

    def __call__(self):

        self.get_mdl()

        cap = cv2.VideoCapture(0)
        assert cap.isOpened()

        while True:

            ret, frame = cap.read()
            assert ret 

            frame = cv2.resize(frame, (416,416))

            #md_str = f"python detect.py --weights {self.model} --img 416 --conf 0.4 --source {frame}"

            #results = subprocess.call(cmd_str)

            results = self.score_frame(frame)

            frame = self.plot_box(results=results, frame=frame)

            cv2.imshow("preds", frame)

            # st.image(frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()

det = Detector(vid_path="tester.mp4", model_path="../../yolov5/runs/train/yolov5s_results/weights/best.pt")

det()
