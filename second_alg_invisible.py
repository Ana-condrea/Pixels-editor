import cv2


def find_div(elem: int) -> int:
    length = len("{0:b}".format(elem))
    if length % 4 != 0:
        div_length = length // 4
        length = (div_length + 1) * 4
    return length


def get_binary(list_pixel: list) -> list:
    list_binary = list()
    m = max(list_pixel)
    length = find_div(m)
    for elem in list_pixel:
        list_binary.append(format(elem, 'b').zfill(length))
    return list_binary


def get_ord(message):
    list_ord = list()
    list_ord.append(len(message))
    for elem in message:
        ord_elem = ord(elem)
        list_ord.append(ord_elem)
    return list_ord


def make_list_binary(lista: list) -> list:
    list_elem = list()
    for elem in lista:
        for e in elem:
            list_elem.append(e)
    return list_elem


def convet_byte_to_int(list_bytes: list) -> list:
    final_list = list()

    for byte_elem in list_bytes:
        final_int = 0
        for b in byte_elem:
            final_int = final_int * 2 + int(b)
        final_list.append(final_int)
    return final_list


def hide_text(list_pixel: list, list_text: list) -> list:
    list_final = list()
    for i in range(len(list_text)):
        modify_bits = list_pixel[i][:7] + list_text[i]
        list_final.append(modify_bits)
    return list_final


def modify_image(image, text):
    total_list = list()
    ordin = get_ord(text)
    binary = get_binary(ordin)
    binary_list = make_list_binary(binary)
    row, col = image.shape[:2]
    for i in range(row):
        for j in range(col):
            if binary_list != []:
                px = image[i, j]
                list_pixel_bin = get_binary(px)
                list_modif = hide_text(list_pixel_bin, binary_list[0:3])
                binary_list = binary_list[3:]
                new_px = convet_byte_to_int(list_modif)
                total_list.append(new_px)
            else:
                total_list.append(image[i, j])
    return total_list


def modify_image_f(image, text):
    elem = 0
    rows2, cols2 = image.shape[:2]
    total_list = modify_image(image, text)
    for i in range(rows2):
        for j in range(cols2):
            image[i, j] = total_list[elem]
            elem = elem + 1


def load_text_invisible(image, text):
    modify_image_f(image, text)
    cv2.imshow("Load image-text", image)
    cv2.waitKey(0)
    image_final = image.copy()
    cv2.imwrite("Load_text_invisible.png", image_final)


def get_chr(list_ord):
    message = ""
    for elem in list_ord:
        chr_elem = chr(elem)
        message = message + chr_elem
    return message


def create_number(list_bin):
    p = 0
    number = 0
    length = ""
    no_el = 0
    for elem in list_bin:
        if no_el < 8:
            length = length + elem[7]
            no_el = no_el + 1

    lista_bin_new = reversed(list(length))
    for elem in lista_bin_new:
        number = number + pow(2, p) * int(elem)
        p = p + 1
    return number


def get_length(image):
    row, col = image.shape[:2]
    no = 0
    list_len = list()
    for i in range(row):
        for j in range(col):
            if no < 8:
                px = image[i, j]
                px_bin = get_binary(px)
                list_len.extend(px_bin)
                no = no + 3

    length_number = create_number(list_len)
    return length_number


def extract_text(image):
    list_text, new_list, list_ord_elem = list(), list(), list()
    start, no = 0, 0
    row, col = image.shape[:2]
    text_len = get_length(image)
    count = (2 * text_len) * 8

    for i in range(row):
        for j in range(col):
            if no <= count:
                px = image[i, j]
                px_bin = get_binary(px)
                list_text.extend(px_bin)
                no = no + 3

    list_text = list_text[8:count]
    for elem in range(len(list_text)):
        if elem % 8 == 0 and elem != 0:
            new_list.append(list_text[start:start+8])
            start = start + 8

    for elem in range(text_len):
        list_ord_elem.append(create_number(new_list[elem]))

    return get_chr(list_ord_elem)


def unload_text_invisible(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    txt = extract_text(image)
    return txt


# image1 = cv2.imread("images.jpg", cv2.IMREAD_COLOR)
# load_text_invisible(image1, 'ab, a')
#
# image_u = cv2.imread("Load_text_invisible.png", cv2.IMREAD_COLOR)
# print(unload_text_invisible("Load_text_invisible.png"))
