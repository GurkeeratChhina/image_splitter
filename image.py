#A simple script to split a source image into several destination images
#by randomly assigning each pixel in the source to one of the destinations

from PIL import Image, ImageDraw
from math import sqrt
from math import ceil

def image_templater(i):
    def make_image():
        return Image.new('RGBA', i.size, color = (0,0,0,0))
    return make_image

#pick which image to split, and convert to a format we can work with
img = Image.open('crop_circle.png').convert("RGBA")
d = img.getdata()
maker = image_templater(img)

#how many files to split the image into
split_num = 3
imgs = [maker() for _ in range(0, split_num)]

# Transformation function
# src is the input image after being converted to the correct form
# dsts is where the output will be saved
# circle_rad determines how many pixels will be grouped together. Use circle_rad = 1 for individual pixels
def transform_random(src, dsts, circle_rad):
    import random
    h = src.height
    w = src.width
    circle_centers_x = (range(0,w,ceil(sqrt(2)*circle_rad)+4))
    circle_centers_y = (range(0,h,ceil(sqrt(2)*circle_rad)+4))
    for center_x in circle_centers_x:
        for center_y in circle_centers_y:
            layer = random.choice(dsts)
            for delta_x in range(-1*circle_rad, circle_rad+1):
                for delta_y in range(-1*circle_rad, circle_rad+1):
                    if delta_x**2 + delta_y**2 < circle_rad**2:
                        x = center_x + delta_x
                        y = center_y + delta_y
                        if x in range(w) and y in range(h):
                            layer.putpixel((x,y),src.getpixel((x,y)))

transform_random(img, imgs, 10)

for i, to_save in enumerate(imgs):
    to_save.save(f'circle_{i}.png')