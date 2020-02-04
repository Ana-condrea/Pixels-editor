import numpy as np
import cv2
from watermark_img_1 import create_mask, remove_background, create_invisible_image,compute_mask, remove_logo
from watermark_text_1 import create_txt_image, add_logo_text, compute_mask_text, remove_logo_text


def compute_logo_image(path_logo):
    create_mask(path_logo)
    remove_background(path_logo)
    create_invisible_image()


def compute_logo_text(text, color,save_mask):
    create_txt_image(text, color, save_mask, 0)
    create_mask("mask.png")
    remove_background("mask.png")
    create_invisible_image()


def add_logo_video_image(path_video, x_poz, y_poz, alpha):
    video = cv2.VideoCapture(path_video)
    video_w = int(video.get(3))
    video_h = int(video.get(4))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    frame_per_second = 20
    out = cv2.VideoWriter('output_logo_img.avi', fourcc, frame_per_second, (video_w, video_h))
    image_logo = cv2.imread("invisible_bkd.png")
    image_logo = cv2.resize(image_logo, (image_logo.shape[1]//5, image_logo.shape[0]//5))
    length_frames = int(cv2.VideoCapture.get(video, int(cv2.CAP_PROP_FRAME_COUNT)))
    count = 0
    while video.isOpened():
        ret, frame = video.read()
        mask_overlay = np.zeros((frame.shape[0], frame.shape[1], 3), dtype="uint8")
        mask_overlay[x_poz:x_poz+image_logo.shape[0], y_poz:y_poz+image_logo.shape[1]] = image_logo
        logo_image = frame
        logo_image = cv2.addWeighted(mask_overlay, alpha, logo_image, 1, 0, logo_image)
        cv2.imshow('Video with logo', logo_image)
        cv2.imwrite("logo_img.png", logo_image)
        out.write(logo_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        count = count + 1
        if count == length_frames:
            break
    video.release()
    out.release()
    cv2.destroyAllWindows()

def remove_logo_video_image(path_video, x_poz, y_poz):
    video = cv2.VideoCapture(path_video)
    video_w = int(video.get(3))
    video_h = int(video.get(4))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    frame_per_second = 20
    out = cv2.VideoWriter('output_rm_logo_img.avi', fourcc, frame_per_second,(video_w, video_h))
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            compute_mask(frame, x_poz, y_poz, 0)
            remove_logo_frame = remove_logo(frame, 0)
            cv2.imshow('Without logo', remove_logo_frame)
            out.write(remove_logo_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()

def add_logo_video_text(path_video, x_poz, y_poz, alpha):
    video = cv2.VideoCapture(path_video)
    video_w = int(video.get(3))
    video_h = int(video.get(4))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    frame_per_second = 20
    out = cv2.VideoWriter('output_logo_txt.avi', fourcc, frame_per_second, (video_w, video_h))
    length_frames = int(cv2.VideoCapture.get(video, int(cv2.CAP_PROP_FRAME_COUNT)))
    count = 0
    while video.isOpened():
        ret, frame = video.read()
        frame_txt = add_logo_text(frame,'invisible_bkd.png', alpha, x_poz, y_poz, 0)
        cv2.imshow('Video with logo', frame_txt)
        out.write(frame_txt)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        count = count + 1
        if count == length_frames:
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()


def remove_logo_video_text(path_video, x_poz, y_poz):
    video = cv2.VideoCapture(path_video)
    video_w = int(video.get(3))
    video_h = int(video.get(4))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    frame_per_second = 20
    out = cv2.VideoWriter('output_rm_logo_txt.avi', fourcc, frame_per_second, (video_w, video_h))
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            compute_mask_text(frame, x_poz, y_poz, 0)
            remove_text = remove_logo_text(frame, 0)
            cv2.imshow('Without logo', remove_text)
            out.write(remove_text)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()


def add_watermark_image_video(path_logo, path_video, poz_x, poz_y, alpha):
    compute_logo_image(path_logo)
    add_logo_video_image(path_video, poz_x, poz_y, alpha)


def remove_watermark_image_video(path_video, poz_x, poz_y):
    remove_logo_video_image(path_video, poz_x, poz_y)


def add_watermark_text_video(text, path_video, poz_x, poz_y, alpha, who_save, color):
    compute_logo_text(text, color, who_save)
    add_logo_video_text(path_video, poz_x, poz_y, alpha)


def remove_watermark_text_video(path_video, poz_x, poz_y):
    remove_logo_video_text(path_video, poz_x, poz_y)

#
# path_video = 'video3.mp4'
# var = 1
# if var:
# #     # compute_logo_image('5.png')
# #     # add_logo_video_image(path_video, 200, 200, 0.7)
#     # remove_logo_video_image('output_logo_img.avi', 200, 200)
#     add_watermark_image_video('1.png', path_video, 600, 5,1)
#     remove_watermark_image_video('output_logo_img.avi', 600,5)
# # # # # else:
# compute_logo_text('ana are mere', (255, 0, 252), 1)
# add_logo_video_text(path_video, 200, 200, 0.4)
# remove_logo_video_text('output_logo_txt.avi', 200, 200)
# #

# add_watermark_text_video('ana are mere la la la ',path_video, 5, 5, 1, 0, (255, 0, 252))
# remove_watermark_text_video('output_logo_txt.avi', 5, 5)
