import json
import os

from random import random
from time import sleep
from urllib.request import urlretrieve


with open('output/json/data.json') as f:
    data = json.loads(f.read())


for emoji, e_data in data.items():
    print('{}...'.format(emoji))
    for mod, mod_data in e_data.items():
        new_dir = 'output/img-all/{}/{}'.format(emoji, mod)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        imgs = mod_data['imgs']
        for img in imgs:
            name = img['title'].lower().replace(' ', '-')
            urlretrieve(img['url'], '{}/{}.png'.format(new_dir, name))

        sleep(1 + random())
