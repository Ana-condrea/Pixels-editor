import soundfile as sf
import numpy as np
import cv2
import random
lista_elem = [4096, 256, 8192, 16384, 2048, 512, 1024, 128, 1]


def make_new_image(sound_path):
    maxim = 32767
    elem = 0
    h, w = 0, 0
    data, samplerate = sf.read(sound_path)
    scaled = np.int16(data/np.max(np.abs(data)) * maxim)
    if len(scaled) == 220500:
        w = 500
        h = len(list(scaled))//w
    elif len(scaled) == 1323000:
        w = 1500
        h = len(list(scaled))//w
    list_px = list(scaled)
    new_image = np.zeros((h, w, 3), dtype=np.int16)
    rows, cols = new_image.shape[:2]
    c_list = list()
    for i in range(rows):
        for j in range(cols):
            if elem < len(list_px):
                if list_px[elem] < 0:
                    new_elem = abs(list_px[elem])
                    new_image[i, j] = 16384, new_elem,  len(format(new_elem, 'b'))
                    c_list.append(new_elem)
                else:
                    new_image[i, j] = 0, list_px[elem], len(format(list_px[elem], 'b'))
                    c_list.append(list_px[elem])
                elem = elem + 1
    # cv2.imshow("Image from audio", new_image)
    # cv2.waitKey(0)
    cv2.imwrite("audio_image.png", new_image)
    return new_image


def create_cover_image(number_sec):
    if number_sec == 1:
        image = np.zeros((600, 600, 3), dtype=np.int16)
    else:
        image = np.zeros((900, 1600, 3), dtype=np.int16)
    rows, cols = image.shape[:2]
    for i in range(rows):
        for j in range(cols):
            image[i, j] = random.randint(0, 32767), random.randint(0, 32767), random.randint(0, 32767)
            # image[i,j] = 600, 255, 32766
    # cv2.imshow("Image from audio", image)
    # cv2.waitKey(0)
    # cv2.imwrite("cover_image.png", image)
    return image


def get_binary_two(list_pixel: list) -> list:
    list_binary = list()
    for elem in list_pixel:
        new_elem = format(elem, 'b')
        list_binary.append(new_elem.ljust(15, '0'))
    return list_binary


def get_binary_first(elem):
    new_elem = format(elem, 'b').zfill(15)
    return new_elem


def get_binary(list_pixel: list) -> list:
    list_binary = list()
    for elem in list_pixel:
        list_binary.append(format(elem, 'b').zfill(15))
    return list_binary


def hide_image(list_img_1: list, list_img_2: list, no_byte: int) -> list:
    list_bites = list()
    for i in range(len(list_img_1)):
        if i == 2:
            modify_bits = list_img_2[i]
        else:
            modify_bits = list_img_1[i][:(15 - no_byte)] + list_img_2[i][:no_byte]
        list_bites.append(modify_bits)
    return list_bites


def convert_byte_to_int(list_bytes: list) -> list:
    final_list = list()

    for byte_elem in list_bytes:
        final_int = 0
        for b in byte_elem:
            final_int = final_int * 2 + int(b)
        final_list.append(final_int)
    return final_list


def modify_pixels(img1, img2, no_bytes: int) -> list:
    total_list = list()
    rows2, cols2 = img2.shape[:2]
    for i in range(rows2):
        for j in range(cols2):
            px = img1[i, j]
            px2 = img2[i, j]
            l1 = get_binary(px)
            l2 = get_binary_two(px2[:2])
            l2.append(format(px2[2], 'b'))
            lista = hide_image(l1, l2, no_bytes)
            new_px = convert_byte_to_int(lista)
            total_list.append(new_px)
    return total_list


def modify_image(img1, img2, no_bytes: int):
    elem = 0
    rows2, cols2 = img2.shape[:2]
    total_list = modify_pixels(img1, img2, no_bytes)
    for i in range(rows2):
        for j in range(cols2):
            img1[i, j] = total_list[elem]
            elem = elem + 1


def load_audio(no_bytes: int, audio_path, type_audio):

    img1 = create_cover_image(type_audio)
    img1_copy = img1.copy()
    img2 = make_new_image(audio_path)
    modify_image(img1, img2, no_bytes)
    return img1_copy, img2, img1


def final_load_audio(no_bytes: int, audio_path, type_audio):
    img1, img2, img3 = load_audio(no_bytes, audio_path, type_audio)
    cv2.imshow("Cover image", img1)
    cv2.waitKey(0)
    cv2.imwrite("cover_image.png", img1)
    img2 = make_new_image(audio_path)
    cv2.imshow("Image from audio", img2)
    cv2.waitKey(0)
    cv2.imwrite("audio_image.png", img2)
    cv2.imshow("Load image", img3)
    cv2.waitKey(0)
    cv2.imwrite("load_audio.png", img3)


def add_zero(list_binary: list, no_bytes: int, lenght: int):
    new_list = list()
    for elem in list_binary:
        no_zero = "0" * (15 - no_bytes)
        new_elem = elem[15 - no_bytes:] + no_zero
        copy_elem = new_elem[:lenght]
        new_list.append(copy_elem)
    return new_list


def unload_audio(no_bytes: int, audio_path, type_audio):
    img1, img_original, img = load_audio(no_bytes, audio_path, type_audio)
    rows, cols = img_original.shape[:2]
    total_list = []
    for i in range(rows):
        for j in range(cols):
            px = img[i, j]
            px_binary = get_binary(px[:2])
            new_px = add_zero(px_binary[:2], no_bytes, px[2])
            conv_px = convert_byte_to_int(new_px)
            conv_px.append(px[2])
            if conv_px[0] in lista_elem:
                total_list.append(-(conv_px[1]))
            else:
                total_list.append(conv_px[1])
    return total_list

# im1 = create_cover_image(1)
# im2 = make_new_image("five.wav")
# img_audio = load_audio(im1, im2, 14)
# list_px_img = unload_audio(img_audio, im2, 14)
#
# scaled = np.int16(list_px_img/np.max(np.abs(list_px_img)) * 32767)
# sf.write('test3_audio.wav', scaled, 44100)
