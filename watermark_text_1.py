import cv2
import numpy as np
from watermark_img_1 import create_mask, remove_background, create_invisible_image


def create_txt_image(text, color_text, save_mask, font_size):
    font_scale = 1
    thickness = 2
    font_text = cv2.FONT_HERSHEY_SIMPLEX
    rows_txt, cols_txt = 0, 0
    if len(text) > 0:
        rows_txt = cv2.getTextSize(text, font_text, 1, 2)[0][1] + 5
        cols_txt = cv2.getTextSize(text, font_text, 1, 2)[0][0] + 5
    if font_size == 0:
        rows_txt = rows_txt + 3*len(text)
        cols_txt = cols_txt + 8*len(text)
    elif font_size == 1 and ("q" in list(text) or "y" in list(text) or "g" in list(text) or "j" in list(text)):
        rows_txt = rows_txt + 10

    mask_img = np.zeros((rows_txt, cols_txt, 3), dtype='uint8')
    textsize = cv2.getTextSize(text, font_text, 1, 2)[0]
    pozX = (mask_img.shape[1] - textsize[0]) // 2
    pozY = (mask_img.shape[0] + textsize[1]) // 2
    cv2.putText(mask_img, text, (pozX, pozY), font_text, font_scale, color_text, thickness, cv2.LINE_AA)
    cv2.imwrite("mask.png", mask_img)

    if save_mask == 1:
        cv2.putText(mask_img, text, (pozX, pozY), font_text, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        cv2.imwrite("mask_text.png", mask_img)
    else:
        mask_img.fill(255)
        cv2.imwrite("mask_text.png", mask_img)



def add_logo_text(path_image, path_logo, alpha, x_poz, y_poz, who_save):
    if who_save:
        img = cv2.imread(path_image)
    else:
        img = path_image
    logo = cv2.imread(path_logo)
    mask_overlay = np.zeros((img.shape[0], img.shape[1], 3), dtype="uint8")
    mask_overlay[x_poz:x_poz + logo.shape[0], y_poz:y_poz + logo.shape[1]] = logo
    logo_image = img.copy()
    logo_image = cv2.addWeighted(mask_overlay, alpha, logo_image, 1, 0, logo_image)
    if who_save:
        cv2.imshow('image with logo', logo_image)
        cv2.waitKey(0)
        cv2.imwrite("logo_img.png", logo_image)
    else:
        return logo_image


def compute_mask_text(path_image, x_poz, y_poz, how_arg):
    if how_arg:
        img = cv2.imread(path_image)
    else:
        img = path_image
    mask_img = cv2.imread('mask_text.png')
    y1, y2 = y_poz, y_poz + mask_img.shape[1]
    x1, x2 = x_poz, x_poz + mask_img.shape[0]
    # print("mash shape", mask_img.shape[:2])
    # print("x1-y1", x1, y1,"x2-y2", x2, y2)
    total_list = []
    rows, cols = mask_img.shape[:2]
    for i in range(rows):
        for j in range(cols):
            total_list.append(list(mask_img[i, j]))

    mask = np.zeros(img.shape[:])
    elem = 0
    # rows, cols = mask.shape[:2]
    # print(len(total_list))
    for i in range(x1, x2-1):
        for j in range(y1-1, y2-1):
            # print(i, j, total_list[elem], elem)
            mask[i, j] = total_list[elem]
            elem = elem + 1
    # cv2.imshow("maskaaaa", mask)
    # cv2.waitKey(0)
    cv2.imwrite('rm_mask.png', mask)



def remove_logo_text(path_image, arg):
    if arg:
        img = cv2.imread(path_image)
    else:
        img = path_image
    mask = cv2.imread('rm_mask.png', 0)
    image_result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    if arg:
        cv2.imshow("result", image_result)
        cv2.waitKey(0)
        cv2.imwrite("rl_image.png", image_result)
    else:
        return image_result

def add_watermark_text(path_image, text, color, save, alpha, poz_x, poz_y):
    create_txt_image(text, color, save, 1)
    create_mask("mask.png")
    remove_background("mask.png")
    create_invisible_image()
    add_logo_text(path_image, 'invisible_bkd.png', alpha, poz_x, poz_y, 1)

def remove_watermark_text(path_image, poz_x, poz_y):
    compute_mask_text(path_image, poz_x, poz_y, 1)
    remove_logo_text(path_image, 1)

# create_txt_image('ana are mere', (255,0,255), 0, 1)
#
# create_mask("mask.png")
# remove_background("mask.png")
# create_invisible_image()
# add_logo_text("d.jpg", 'invisible_bkd.png', 0.5, 50, 50, 1)


# print("lalalallaaaa")


# add_watermark_text("d.jpg", "ana are mere",(255,0,255), 0,0.5, 50, 50)
# compute_mask_text("logo_img.png", 5, 50, 1)
# remove_logo_text('logo_img.png', 1)

