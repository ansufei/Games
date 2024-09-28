from bs4 import BeautifulSoup
import requests
import io
from PIL import Image, ImageEnhance
import numpy as np
import itertools


def save_img(source, image, name):
    image.save(source + name)

def save_vector_images(n):
    url = 'https://publicdomainvectors.org'
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    wrapper = soup.find('div', {'id': 'vectors'})
    img_tags = wrapper.findAll('img')
    img_url = img_tags[n].get('src')
    if img_url.endswith('.webp'):
        img_response = requests.get(url + img_url)
        img_data = io.BytesIO(img_response.content)
        
        img = Image.open(img_data)
    # extract image name
    name = img_url.split('/')[-1].replace('webp','jpg')
    #save_img('img/', img, name)
    return img, name

def use_tmp_img():
    img = Image.open('img/bell-boy-publicdomainvector.jpg')
    return img, 'bell-boy-publicdomainvector.jpg'

#Crop image (and remove banner)
def remove_blank_col(image):
    empty_col = []
    for i in range(image.shape[1]):
        col = image[:,i].tolist()
        if col[1:] == col[:-1]:
            empty_col.append(i)
    image = np.delete(image, empty_col, axis=1)
    return image

def remove_blank_rows(image):
    empty_row = []
    for i in range(image.shape[0]):
        row = image[i,:].tolist()
        if row[1:] == row[:-1]:
            empty_row.append(i)
    image = np.delete(image, empty_row, axis=0)
    return image

def crop_image(img, banner=True):
    w, h = img.size
    if banner:
        img = img.crop((0, 0, w, h-50))
    img_arr = np.asarray(img)
    crop_v = remove_blank_rows(img_arr)
    crop_h = remove_blank_col(crop_v)
    return crop_h

#Resize and adjust colors

def pixelize(n, img):
    nw, nh = img.size
    new_width =  int(nw * n / nh)
    image = img.resize((new_width, n),resample=Image.BILINEAR)
    return image

def remove_light_colors(image_arr, n):
    high_value_filter = image_arr > n
    image_arr[high_value_filter] = 255
    return Image.fromarray(image_arr)

def simplify_colors(image, nb_colors=3):
    image = image.convert('P', palette=Image.ADAPTIVE, colors=nb_colors)
    return image.convert("RGB", palette=Image.ADAPTIVE, colors=nb_colors)

def increase_sharpness(image, n):
    sharpness = ImageEnhance.Sharpness(image)
    return sharpness.enhance(n)

def increase_contrast(image, n):
    contrast = ImageEnhance.Contrast(image)
    return contrast.enhance(n)

# create nonogram grid
def count_consecutive_colors(grid):
    """
    Count number of consecutive colors by row
    Associate the corresponding color to each count 
    """
    row_colors = []
    for row in grid:
        row_colors.append([{len(list(group)): int(key)} for key, group in itertools.groupby(row) if key != 0])
    return row_colors