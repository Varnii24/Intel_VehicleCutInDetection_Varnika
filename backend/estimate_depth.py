# backend/estimate_depth.py
import torch
from torchvision import transforms
from PIL import Image
import numpy as np

# Load Monodepth2 models
encoder = torch.load('models/monodepth2/encoder.pth')
depth_decoder = torch.load('models/monodepth2/depth.pth')

def run_depth_estimation(image_path):
    input_image = Image.open(image_path).convert('RGB')
    original_width, original_height = input_image.size

    feed_height = 192
    feed_width = 640

    input_image_resized = input_image.resize((feed_width, feed_height), Image.LANCZOS)
    input_image_resized = transforms.ToTensor()(input_image_resized).unsqueeze(0)

    with torch.no_grad():
        features = encoder(input_image_resized)
        outputs = depth_decoder(features)

    disp = outputs[("disp", 0)]
    disp_resized = torch.nn.functional.interpolate(disp, (original_height, original_width), mode="bilinear", align_corners=False)
    depth_map = disp_resized.squeeze().cpu().numpy()

    return depth_map.tolist()
