https://hf-mirror.com/OFA-Sys/chinese-clip-vit-base-patch16

# Chinese-CLIP-ViT-Base-Patch16

## Introduction

This is the base-version of the Chinese CLIP, with ViT-B/16 as the image encoder and RoBERTa-wwm-base as the text encoder. Chinese CLIP is a simple implementation of CLIP on a large-scale dataset of around 200 million Chinese image-text pairs. For more details, please refer to our technical report https://arxiv.org/abs/2211.01335 and our official github repo https://github.com/OFA-Sys/Chinese-CLIP (Welcome to star! 🔥🔥)

## Use with the official API

We provide a simple code snippet to show how to use the API of Chinese-CLIP to compute the image & text embeddings and similarities.
```
from PIL import Image
import requests
from transformers import ChineseCLIPProcessor, ChineseCLIPModel

model = ChineseCLIPModel.from_pretrained("OFA-Sys/chinese-clip-vit-base-patch16")
processor = ChineseCLIPProcessor.from_pretrained("OFA-Sys/chinese-clip-vit-base-patch16")

url = "https://clip-cn-beijing.oss-cn-beijing.aliyuncs.com/pokemon.jpeg"
image = Image.open(requests.get(url, stream=True).raw)
# Squirtle, Bulbasaur, Charmander, Pikachu in English
texts = ["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"]

# compute image feature
inputs = processor(images=image, return_tensors="pt")
image_features = model.get_image_features(**inputs)
image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)  # normalize

# compute text features
inputs = processor(text=texts, padding=True, return_tensors="pt")
text_features = model.get_text_features(**inputs)
text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)  # normalize

# compute image-text similarity scores
inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)
outputs = model(**inputs)
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)  # probs: [[1.2686e-03, 5.4499e-02, 6.7968e-04, 9.4355e-01]]

```



