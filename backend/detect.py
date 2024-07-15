import torch
from pathlib import Path

def run_detection(image_path):
    model_path = 'C:/Data/prog_projects/cut-in-detection/prototype-3/yolov5_training/yolov5_training/exp_third20/weights/best.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Data/prog_projects/cut-in-detection/prototype-3/yolov5_training/yolov5_training/exp_third20/weights/best.pt')
    model.eval()
    img = Path(image_path)  # Ensure the image_path is valid
    results = model(img)
    return results.pandas().xyxy[0].to_dict(orient='records')
