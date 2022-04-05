import yaml
import cv2
import numpy as np

from PIL import Image
from tqdm import tqdm

import scraper

with open('config.yaml', 'r') as f:
   config = yaml.load(f, Loader=yaml.FullLoader)
   
s = config['timelapse']['image-range']['start']
e = config['timelapse']['image-range']['end']
g = config['timelapse']['frame-granularity']
t = config['timelapse']['download-threads']

x = config['place-canvas']['top-left-coordinates']['x']
y = config['place-canvas']['top-left-coordinates']['y']
dx = config['place-canvas']['dimensions']['width']
dy = config['place-canvas']['dimensions']['height']

n = config['output']['name']
w = config['output']['dimensions']['width']
h = config['output']['dimensions']['height']

ids = scraper.get_image_ids(s, e, g)
scraper.init_fetch_images(ids, t)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
vid = cv2.VideoWriter(f'{n}.mp4', fourcc, 30.0, (w, h))

for id in tqdm(ids, 
               desc='Timelapse creation',
               ascii=True,
               leave=False):
   img = scraper.get_image(id)
   img = img.crop((x, y, x + dx, y + dy))
   img = img.resize((w, h), Image.Resampling.NEAREST)
   vid.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
   
vid.release()
print(f'\nDone, check {n}.mp4')