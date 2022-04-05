import os
import yaml
import cv2
import numpy as np
from PIL import Image
from progress.bar import Bar

import scraper

with open('config.yaml', 'r') as f:
   config = yaml.load(f, Loader=yaml.FullLoader)
   
s = config['timelapse']['image-range']['start']
e = config['timelapse']['image-range']['end']
g = config['timelapse']['frame_granularity']

x = config['place-canvas']['top-left-coordinates']['x']
y = config['place-canvas']['top-left-coordinates']['y']
dx = config['place-canvas']['dimensions']['width']
dy = config['place-canvas']['dimensions']['height']

n = config['output']['name']
w = config['output']['dimensions']['width']
h = config['output']['dimensions']['height']

os.mkdir('image_cache')
ids = scraper.get_image_ids(s, e, g)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
vid = cv2.VideoWriter(f'{n}.mp4', fourcc, 30.0, (w, h))

bar = Bar('Creating the timelapse', max=len(ids))
for id in ids:
   img = scraper.get_image(id)
   img = img.crop((x, y, x + dx, y + dy))
   img = img.resize((w, h), Image.NEAREST)
   vid.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
   bar.next()
   
vid.release()