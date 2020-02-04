import cv2
import random
from hide_text_in_video import change_frame_in_video
from first_alg import load, unload_show


def hide_image_in_frame(frame_image, image, no_bite):
    load(frame_image, image, no_bite)
    return frame_image


def unload_image_from_video(path_video, img, frame_number, no_bite, size):
    video = cv2.VideoCapture(path_video)
    count = 0
    while video.isOpened():
        ret, frame = video.read()
        if frame.all() == img.all() and frame_number == count:
            unload_show(frame, size, no_bite, 0)
            break
        count = count + 1

#
# image_to_hide = cv2.imread("3.png", cv2.IMREAD_COLOR)
# size_img = image_to_hide.shape[:2]
# path = 'video2.mp4'
# videoo = cv2.VideoCapture(path)
# frame_count = int(videoo.get(cv2.CAP_PROP_FRAME_COUNT))
# random_frame = random.randint(0, frame_count//2)
# print(random_frame)
# videoo.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
# _, imagee = videoo.read()
# no_bites = 4
# return_image = hide_image_in_frame(imagee, image_to_hide, no_bites)
# cv2.imshow('loaded image', return_image)
# change_frame_in_video(path, return_image, random_frame)
#
#
# unload_image_from_video("output_text.avi", return_image, random_frame, no_bites, size_img)
