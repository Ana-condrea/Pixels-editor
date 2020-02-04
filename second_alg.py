import cv2


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
    for i in range(row):
        for j in range(col):
            px = image[i, j]
            if i == 0 and j == 0 and no < text_len:
                new_px = text_len
            elif no <= text_len:
                new_px = ordin[no-1]
            else:
                new_px = px[2]
            image[i, j] = (px[0], px[1], new_px)
            no = no + 1


def load_text(image, text):
    modify_image(image, text)
    cv2.imshow("Load image-text", image)
    cv2.waitKey(0)
    image_final = image.copy()
    cv2.imwrite("Load_text.png", image_final)


def get_chr(list_ord):
    message = ""
    for elem in list_ord:
        chr_elem = chr(elem)
        message = message + chr_elem
    return message


def extract_text(image):
    row, col = image.shape[:2]
    text_len = 0
    no = 0
    list_text = list()
    for i in range(row):
        for j in range(col):
            px = image[i, j]
            if i == 0 and j == 0:
                text_len = px[2]
            elif no <= text_len:
                list_text.append(px[2])
            no = no + 1
    text = get_chr(list_text)
    return text


def unload_text(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    txt = extract_text(image)
    return txt

#
# image1 = cv2.imread("images.jpg", cv2.IMREAD_COLOR)
# text1 = " en messages in an image file of concealing a hidden messagets in an image"
# if len(text1) > 255:
#     raise ValueError("Length of the text should be lower that 256 character")
# load_text(image1, text1)
# print(unload_text("Load_text.png"))
