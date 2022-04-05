import os
import io
import sys
import requests

from PIL import Image
from bs4 import BeautifulSoup
from progress.bar import Bar

url = 'https://rplace.space/combined/'

def get_image_ids(start_id, end_id, granularity):
   res = requests.get(url)
   
   start = 0
   ids = []
   if res.status_code == 200:
      soup = BeautifulSoup(res.text, 'html.parser')
      for a in soup.find_all('a'):
         id = os.path.splitext(a.get('href'))[0]
         try:
            id = int(id)
            start = len(ids) if id == start_id else start
            ids.append(id)
         except ValueError: # skip <a> tags that aren't image links
            continue
         if id == end_id:
            break
   else: 
      print(f'Could not get image ids from {url}')
      sys.exit()
      
   return ids[start::granularity]


def get_image(id):
    img_path = f'image_cache/{id}.png'
    try:
      img = Image.open(img_path)
    except:
      img_url = f'https://rplace.space/combined/{id}.png'
      res = requests.get(img_url, stream = True)
      if res.status_code == 200:
         img = Image.open(io.BytesIO(res.content))
      else:
         print(f'Could not download image')
         sys.exit()
      img.save(img_path, 'PNG')
    return img