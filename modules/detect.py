import cv2
import torch

class ObjectDetection():

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='../resources/yolov5s.pt')

    def detect(self, imgs):
        # Inference
        results = self.model(imgs)

        # Results
        results.print()
        
        if len(results.pandas().xyxy) == 0:
            return []

        return self.count_number_objects(results.pandas().xyxy[0]['name'])

    def count_number_objects(self, detected_list):
        detected_objects = []
        detected_dict = dict()

        for detection in detected_list:
            if detection not in detected_dict:
                detected_dict[detection] = 1
            else:
                detected_dict[detection] = detected_dict[detection] + 1

        for name, occurrences in detected_dict.items():
            detected_object = self.create_object( name,occurrences)
            detected_objects.append(detected_object)

        return detected_objects
            
    def create_object(self, name, occurrences):
        return {
            "name": name,
            "occurrences": occurrences
        }


# python3 modules/detect.py
#object_detection = ObjectDetection()
#image = cv2.imread("resources/zidane.jpeg")
#result = object_detection.detect(image)
#print(result)