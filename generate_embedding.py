from transformers import CLIPModel, CLIPProcessor
import cv2
from PIL import Image
import os
from glob import glob
import json
import torch
import pickle
from tqdm import tqdm
def read_image(image_path):
    """
    Reads an image from a file into a numpy array.
    Args:
        image_path (str): The path to the image file.
    Returns:
        np.ndarray: The image as a numpy array.
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

if __name__ == "__main__":
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14").cuda().eval()
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    train_json_path = "/data/zeping_data/map2loc/xml2txt/"
    train_image_path = "/data/mls_data/USGS_Map_Gallery/USGS_Histo_Maps_24000_Training/"
    all_image_path = glob(train_image_path+"*.tif")
    dict = {}


    for img_file in tqdm(all_image_path):
        txt_file = os.path.join(train_json_path,os.path.basename(img_file).split(".")[0]+".txt")
        with open(txt_file) as f:
            data = f.readlines()[0]
        if os.path.exists(img_file):
            try:
                image = Image.open(img_file).convert('RGB')
            except:
                continue
            image = processor(images=image, return_tensors="pt")
            image = image.to(model.device)
            with torch.no_grad():
                img_emb = model.get_image_features(**image)[0]
        dict.update({img_file: (img_emb, data)})

    with open('/data/zeping_data/map2loc/train_embedding_from_clip_new.pkl', 'wb') as f:
        pickle.dump(dict, f)







