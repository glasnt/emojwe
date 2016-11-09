import json
import requests

from collections import defaultdict
from random import random
from time import sleep

from bs4 import BeautifulSoup

from util import EMOJIS, TYPES


def fetch(url):
    return BeautifulSoup(requests.get(url).content, "html.parser")


data = defaultdict(dict)
for e in EMOJIS:
    print('\n{}...'.format(e))
    for t in TYPES:
        url = 'http://emojipedia.org/{}{}/'.format(
            e, '' if t == '0' else '-type-{}'.format(t),
        )
        print('fetching {}'.format(url))
        soup = fetch(url)

        sc = soup.find('ul', class_='shortcodes')
        sc = [li.text for li in (sc.findAll('li') if sc else [])]

        entry = {
            'base': e,
            'emoji': soup.find('input', class_='emoji-copy').get('value'),
            'name': soup.find('h1').text,
            'shortcodes': sc,
            'url': url,
            'type': t,
        }

        img_data = []
        img_divs = soup.findAll('div', class_='vendor-rollout-target')
        for d in img_divs:
            img = d.find('img')
            info = {
                'title': d.find('a').text,
                'alt': img.get('alt'),
                'size': '{}x{}'.format(img.get('width'), img.get('height')),
                'url': img.get('srcset').split(' ')[0],
                'url2': img.get('src'),
            }
            img_data.append(info)
        entry['imgs'] = img_data

        print(json.dumps(entry))
        data[e][t] = entry
        sleep(1 + random())

with open('output/json/data.json', 'w') as f:
    json.dump(dict(data), f, ensure_ascii=False)
