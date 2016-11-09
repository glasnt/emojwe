import glob
import os
import shutil

from PIL import Image

from util import EMOJIS, SOURCES, TYPES


def get_match_ct(emoji, source):
    ptn = 'output/img-all/{}/*/{}.png'.format(emoji, source)
    return len(glob.glob(ptn))


for e in EMOJIS:
    print('\n{}...'.format(e))

    # only keep emojis that have all race variants for apple platform
    if get_match_ct(e, 'apple') < len(TYPES):
        continue

    for s in SOURCES:
        # only make dirs for sources that have all race variants
        match_ct = get_match_ct(e, s)
        if match_ct < 6:
            print('skipping {} {} ({} variants)'.format(s, e, match_ct))
            continue

        base = 'output/img-subset'
        png_dir = '{}/png/{}/{}'.format(base, e, s)
        jpg_dir = '{}/jpg/{}/{}'.format(base, e, s)
        os.makedirs(png_dir)
        os.makedirs(jpg_dir)

        for t in TYPES:
            # move png to new dir structure
            old_file = 'output/img-all/{}/{}/{}.png'.format(e, t, s)
            new_file = '{}/{}.png'.format(png_dir, t)
            shutil.copy(old_file, new_file)

            # create a jpg from png and save it
            img = Image.open(new_file).convert('RGBA')
            img_jpg = Image.new('RGBA', img.size, (255, 255, 255, 255))
            img_jpg.paste(img, img)
            img_jpg.save('{}/{}.jpg'.format(jpg_dir, t))
