import cv2
import numpy as np
import soundfile as sf
from second_alg_random_poz import load_text_random
from third_alg import make_new_image
from hide_image_in_audio import extract_list


def load_text_in_audio(text, audio_image):
    dictionar_pozitii_text = load_text_random(audio_image, text)
    return audio_image, dictionar_pozitii_text


def get_chr(list_ord):
    message = ""
    for elem in list_ord:
        chr_elem = chr(elem)
        message = message + chr_elem
    return message


def extract_text(image, dictionary_poz):
    list_text = list()
    for key, value in dictionary_poz.items():
        r = image[value][0]
        g = image[value][1]
        b = image[value][2]
        list_text.append(r)
        list_text.append(g)
        list_text.append(b)
    text = get_chr(list_text)
    return text


def unload_text_from_audio(image, dictionary_poz):
    txt = extract_text(image, dictionary_poz)
    return txt


# text1 = "Ana are mere.Length of the text should be lower that 256 character.!"
# im2 = make_new_image("five.wav")
# img, pozitii_chr = load_text_in_audio(text1, im2)
# lista_px = extract_list(img)
# scaled = np.int16(lista_px/np.max(np.abs(lista_px)) * 32767)
# sf.write('neext.wav', scaled, 44100)
# print(unload_text_from_audio(img, pozitii_chr))
