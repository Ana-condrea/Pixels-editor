import cv2
import numpy as np


def create_mask(path):
    img = cv2.imread(path, 1)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("mask", th_img)
    cv2.waitKey(0)
    cv2.imwrite('log_mask.png', th_img)


def remove_background(path_logo):
    original_image = cv2.imread(path_logo)
    im = original_image.copy()
    image = cv2.imread('log_mask.png')
    row, col = image.shape[:2]
    for i in range(row):
        for j in range(col):
            if list(image[i, j]) == [0, 0, 0]:
                im[i, j] = [0, 0, 0]

    # cv2.imshow('fg', im)
    # cv2.waitKey(0)
    cv2.imwrite('rm_bkd.png', im)


def create_invisible_image():
    img = cv2.imread('rm_bkd.png', 1)
    gary_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th_img = cv2.threshold(gary_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    b, g, r = cv2.split(img)
    rgba = [b, g, r, th_img]
    img_result = cv2.merge(rgba, 4)
    # cv2.imshow("masksesgf", img_result)
    # cv2.waitKey(0)
    cv2.imwrite("invisible_bkd.png", img_result)


def compute_mask(path_image, y_poz, x_poz, how_arg):
    if how_arg:
        img = cv2.imread(path_image)
    else:
        img = path_image
    mask_img = cv2.imread('log_mask.png')
    mask_img = cv2.resize(mask_img, (mask_img.shape[1]//5, mask_img.shape[0]//5))
    y1, y2 = y_poz, y_poz + mask_img.shape[0]
    x1, x2 = x_poz, x_poz + mask_img.shape[1]
    total_list = []
    rows, cols = mask_img.shape[:2]
    for i in range(rows):
        for j in range(cols):
            total_list.append(list(mask_img[i, j]))

    mask = np.zeros(img.shape[:])
    elem = 0
    rows, cols = mask.shape[:2]
    for i in range(rows):
        for j in range(cols):
            if x1 <= j < x2 and i >= y1 and i < y2:
                mask[i, j] = total_list[elem]
                elem = elem + 1

    cv2.imwrite('rm_mask.png', mask)


def add_logo(path_image, path_logo, alpha, x_poz, y_poz):
    img = cv2.imread(path_image)
    logo = cv2.imread(path_logo)
    logo = cv2.resize(logo, (logo.shape[1]//5, logo.shape[0]//5))
    mask_overlay = np.zeros((img.shape[0], img.shape[1], 3), dtype="uint8")
    mask_overlay[x_poz:x_poz+logo.shape[0], y_poz:y_poz+logo.shape[1]] = logo
    logo_image = img.copy()
    logo_image = cv2.addWeighted(mask_overlay, alpha, logo_image, 1, 0, logo_image)
    cv2.imshow('Image with logo', logo_image)
    cv2.waitKey(0)
    cv2.imwrite("image_with_logo.png", logo_image)


def remove_logo(path_image, arg):
    if arg:
        img = cv2.imread(path_image)
    else:
        img = path_image
    mask = cv2.imread('rm_mask.png', 0)
    image_result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    if arg:
        cv2.imshow("Result", image_result)
        cv2.waitKey(0)
        cv2.imwrite("rl_image.png", image_result)
    else:
        return image_result

def add_watermark_img(path_img, path_logo, alpha, poz_x, poz_y):
    create_mask(path_logo)
    remove_background(path_logo)
    create_invisible_image()
    add_logo(path_img, 'invisible_bkd.png', alpha, poz_x, poz_y)


def remove_watermark_img(path_image, poz_x, poz_y):
    compute_mask(path_image, poz_x, poz_y, 1)
    remove_logo(path_image, 1)

# create_mask('5.png')
# remove_background('5.png')
# create_invisible_image()
# add_logo("d.jpg", 'invisible_bkd.png', 0.8, 50, 50)
# compute_mask("logo_img.png", 600, 800, 1)
# remove_logo('logo_img.png', 1)


