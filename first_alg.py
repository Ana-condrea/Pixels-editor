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


def hide_image(list_img_1: list, list_img_2: list, no_byte: int) -> list:
    list_bites = list()
    for i in range(len(list_img_1)):
        # modify_bits = list_img_1[i][:no_byte] + list_img_2[i][-no_byte:]
        modify_bits = list_img_1[i][:(8 - no_byte)] + list_img_2[i][:no_byte]
        list_bites.append(modify_bits)
    return list_bites


def convet_byte_to_int(list_bytes: list) -> list:
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
            l2 = get_binary(px2)
            lista = hide_image(l1, l2, no_bytes)
            new_px = convet_byte_to_int(lista)
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


def load(img1, img2, no_bytes: int):
    modify_image(img1, img2, no_bytes)
    cv2.imshow("Load image", img1)
    cv2.waitKey(0)
    cv2.imwrite("Load.png", img1)


def add_zero(list_binary: list, no_bytes: int):
    new_list = list()
    for elem in list_binary:
        no_zero = "0" * (8 - no_bytes)
        new_elem = elem[8 - no_bytes:] + no_zero
        new_list.append(new_elem)

    return new_list


def unload_image(img, img_original, no_bytes: int):
    original_size = img_original.shape[:2]
    rows, cols = img_original.shape[:2]
    total_list = []
    for i in range(rows):
        for j in range(cols):
            px = get_binary(img[i, j])
            new_px = add_zero(px, no_bytes)
            conv_px = convet_byte_to_int(new_px)
            total_list.append(conv_px)

            if list(img[i, j]) != [0, 0, 0]:
                original_size = (i+1, j+1)

    return total_list, original_size


def unload_show(path_image, size, no_bytes: int, who_save):
    elem = 0
    if who_save:
        img1 = cv2.imread(path_image, cv2.IMREAD_COLOR)
    else:
        img1 = path_image
    img2 = img1.copy()
    lista_px, size_img = unload_image(img1, img2, no_bytes)
    rows, cols = img2.shape[:2]
    for i in range(rows):
        for j in range(cols):
            img1[i, j] = lista_px[elem]
            elem = elem + 1
    img = img1[0:size[0], 0:size[1]]
    cv2.imshow("Unload image", img)
    cv2.waitKey(0)
    cv2.imwrite("Unload.png", img)

#
# def unload(img1, img2, no_bytes: int):
#     modify_image(img1, img2, no_bytes)
#     unload_show(img1, img2, no_bytes)


# ----------------->MAIN <--------------------
# image = cv2.imread("d.jpg", cv2.IMREAD_COLOR)
# image2 = cv2.imread("d2.jpg", cv2.IMREAD_COLOR)
# height, width = image.shape[:2]
# height2, width2 = image2.shape[:2]
# print(height, width)
# print(height2, width2)
# no_b = 7
# if height2 > height or width2 > width:
#     raise ValueError('Image 2 should not be larger than Image 1!')
# if no_b > 7 or no_b < 0:
#     raise ValueError('Number of bytes should not be greater than 7 and lower than 0')
#
#
# load(image, image2, no_b)
# unload(image, image2, no_b)
