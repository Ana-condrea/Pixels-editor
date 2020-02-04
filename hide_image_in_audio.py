import cv2
import numpy as np
import soundfile as sf
from third_alg import make_new_image, get_binary, convert_byte_to_int
import random
dictionary_poz = {}

def add_image_to_audio(audio_image, pixels_image):
    rows, cols = audio_image.shape[:2]
    counter_dict = 1
    count_list = 0
    for i in range(rows):
        for j in range(cols):
            px = audio_image[i, j]
            poz_x = random.randint(0, rows - 1)
            poz_y = random.randint(0, cols - 1)
            if (poz_x, poz_y) not in dictionary_poz.values() and count_list < len(pixels_image):
                dictionary_poz[counter_dict] = (poz_x, poz_y)
                counter_dict = counter_dict + 1
                audio_image[poz_x, poz_y] = (pixels_image[count_list], pixels_image[count_list + 1],
                                             pixels_image[count_list + 2])
                count_list = count_list + 3
            elif (i, j) not in dictionary_poz.values():
                audio_image[i, j] = (px[0], px[1], px[2])
    return dictionary_poz


def extract_pixels(image):
    rows, cols = image.shape[:2]
    list_pixels = list()
    for i in range(rows):
        for j in range(cols):
            list_pixels.extend(image[i, j])
    return list_pixels

def load_image(image, list_px):
    dictionar_pozitii = add_image_to_audio(image, list_px)
    cv2.imshow("Load image in audio", image)
    cv2.waitKey(0)
    return dictionar_pozitii


def load_image_in_audio(audio_image, image):
    pixels = extract_pixels(image)
    dictionar_pozitii_image = load_image(audio_image, pixels)
    return audio_image, dictionar_pozitii_image

def extract_list(audio_with_text):
    total_list = []
    rows, cols = audio_with_text.shape[:2]
    for i in range(rows):
        for j in range(cols):
            px = audio_with_text[i, j]
            px_binary = get_binary(px[:2])
            conv_px = convert_byte_to_int(px_binary)
            conv_px.append(px[2])
            if conv_px[0] == 16384:
                total_list.append(-(conv_px[1]))
            else:
                total_list.append(conv_px[1])
    return total_list


def extract_image_px(image, dictionary_poz):
    list_pixels_image = list()
    for key, value in dictionary_poz.items():
        r = image[value][0]
        g = image[value][1]
        b = image[value][2]
        list_pixels_image.append(r)
        list_pixels_image.append(g)
        list_pixels_image.append(b)
    return list_pixels_image

def compute_image(list_pixels_img, size_img):
    img = np.zeros(size_img, np.uint8)
    rows, cols = img.shape[:2]
    count = 0
    for i in range(rows):
        for j in range(cols):
            img[i, j] = (list_pixels_img[count], list_pixels_img[count + 1], list_pixels_img[count + 2])
            count = count + 3
    cv2.imshow("result", img)
    cv2.waitKey(0)


# img_to_hide = cv2.imread("small4.png", cv2.IMREAD_COLOR)
# size = list()
# size.extend(img_to_hide.shape[:3])
# im2 = make_new_image("five.wav")
# img_audio, pozitii_img = load_image_in_audio(im2, img_to_hide)
# lista_px = extract_list(img_audio)
# scaled = np.int16(lista_px/np.max(np.abs(lista_px)) * 32767)
# sf.write('neext_image.wav', scaled, 44100)
# list_from_audio = extract_image_px(img_audio, dictionary_poz)
# compute_image(list_from_audio, size)

