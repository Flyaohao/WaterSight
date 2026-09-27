import os

import torch
import cv2 as cv

def yolo_detect(img):
    model = torch.hub.load('..', 'custom', path='../pretrained/yolov5s.pt', source='local')
    # BGR to RGB
    img_bgr  = cv.imread(img)
    img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
    results = model(img_rgb)
    results.render()
    img_with_detections = results.imgs[0]
    img_with_detections_bgr = cv.cvtColor(img_with_detections, cv.COLOR_RGB2BGR)
    output_path = "./result/ok_"+img
    cv.imwrite(output_path, img_with_detections_bgr)
    return results

if __name__ == "__main__":
    yolo_detect("bus.jpg")