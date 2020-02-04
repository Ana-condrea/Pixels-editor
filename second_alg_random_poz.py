import cv2
import random

dictionary_poz = {}

def get_ord(message):
    list_ord = list()
    for elem in message:
        ord_elem = ord(elem)
        list_ord.append(ord_elem)
    return list_ord


def modify_image(image, text):
    ordin = get_ord(text)
    text_len = len(text)
    row, col = image.shape[:2]
    no = 0
    global dictionary_poz
    counter = 1
    new_px_r, new_px_g, new_px_b = 0, 0, 0
    if len(text) % 3 == 0:
        number_of_randint = len(text)/3
    else:
        number_of_randint = len(text) // 3 + 1
        text_len = text_len + 3
    for i in range(row):
        for j in range(col):
            px = image[i, j]
            if i == 0 and j == 0 and no < text_len:
                new_px = text_len
                image[i, j] = (px[0], px[1], new_px)
            elif no <= text_len:
                poz_x = random.randint(0, row-1)
                poz_y = random.randint(0, col-1)
                if ((poz_x, poz_y) != (0, 0) or (poz_x, poz_y) not in dictionary_poz.values()) and \
                        counter <= number_of_randint + 1:
                    dictionary_poz[counter] = (poz_x, poz_y)
                    counter = counter + 1
                    if len(ordin[no-3:no]) == 3:
                        new_px_r = ordin[no - 3]
                        new_px_g = ordin[no - 2]
                        new_px_b = ordin[no - 1]
                    if len(ordin[no-3:no]) == 2:
                        new_px_r = ordin[no - 3]
                        new_px_g = ordin[no - 2]
                        new_px_b = 0
                    if len(ordin[no-3:no]) == 1:
                        new_px_r = ordin[no - 3]
                        new_px_g = 0
                        new_px_b = 0
                    image[poz_x, poz_y] = (new_px_r, new_px_g, new_px_b)
                elif (i, j) not in dictionary_poz.values():
                    image[i, j] = (px[0], px[1], px[2])
            no = no + 3
    return dictionary_poz

def load_text_random(image, text):
    dictionar_pozitii = modify_image(image, text)
    cv2.imshow("Load text in image", image)
    cv2.waitKey(0)
    image_final = image.copy()
    cv2.imwrite("load_text_visible.png", image_final)
    return dictionar_pozitii


def get_chr(list_ord):
    message = ""
    for elem in list_ord:
        chr_elem = chr(elem)
        message = message + chr_elem
    return message


def extract_text(image):
    list_text = list()
    for key, value in dictionary_poz.items():
        r = image[value[0], value[1]][0]
        g = image[value[0], value[1]][1]
        b = image[value[0], value[1]][2]
        list_text.append(r)
        list_text.append(g)
        list_text.append(b)
    text = get_chr(list_text)
    return text


def unload_text_random(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    txt = extract_text(image)
    return txt



# image1 = cv2.imread("images.jpg", cv2.IMREAD_COLOR)
# text1 = "Ana are mere.Length of the text should be lower that 256 character.!Ana are mere.Length of the text should be lower that 256 character.!Ana are mere.Length of the text should be lower that 256 character.!Anahould be lower that 256 character.!"
# print(len(text1))
# if len(text1) > 255:
#     raise ValueError("Length of the text should be lower that 256 character")
# load_text_random(image1, text1)
# print(unload_text_random("Load_text_visible.png"))
