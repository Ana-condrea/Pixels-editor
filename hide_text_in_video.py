import cv2
import random
from second_alg_random_poz import load_text_random


def load_text_in_video(text, video_frame):
    dictionar_pozitii_text = load_text_random(video_frame, text)
    return video_frame, dictionar_pozitii_text


def change_frame_in_video(path_video, image, frame_number):
    count = 0
    video = cv2.VideoCapture(path_video)
    video_w = int(video.get(3))
    video_h = int(video.get(4))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    frame_per_second = 20
    out = cv2.VideoWriter('output_modified_video.avi', fourcc, frame_per_second, (video_w, video_h))
    length_frames = int(cv2.VideoCapture.get(video, int(cv2.CAP_PROP_FRAME_COUNT)))
    while video.isOpened():
        ret, frame = video.read()
        if count == frame_number:
            frame = image
            print("Here is the frame we change--->", count)
        cv2.imshow('Video with logo', frame)
        # cv2.imwrite("logo_img.png", frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count = count + 1
        if count == length_frames:
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()


def get_chr(list_ord):
    message = ""
    for elem in list_ord:
        chr_elem = chr(elem)
        message = message + chr_elem
    return message



def extract_text(video_image, dictionary_poz):
    list_text = list()
    for key, value in dictionary_poz.items():
        r = video_image[value[0], value[1]][0]
        g = video_image[value[0], value[1]][1]
        b = video_image[value[0], value[1]][2]
        list_text.append(r)
        list_text.append(g)
        list_text.append(b)
    text = get_chr(list_text)
    return text



def unload_text_from_video(path_video, img, dictionary_poz, frame_number):
    video = cv2.VideoCapture(path_video)
    count = 0
    while video.isOpened():
        ret, frame = video.read()
        if frame.all() == img.all() and frame_number == count:
            return extract_text(img, dictionary_poz)
            break
        count = count + 1



text1 = "Ana are mere.Length of the text should be lower that 256 character.!Ana are mere.Length of the text should " \
        "be lower that 256 character.!Ana are mere.Length of the text should be lower that 256 character.!Anahould " \
        "be lower that 256 characte"

# path_video = 'video1.mp4'
# video = cv2.VideoCapture(path_video)
# frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
# random_frame = random.randint(0, frame_count//2)
# print(random_frame)
# video.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
# _, image = video.read()
# img, pozitii_chr = load_text_in_video(text1, image)
# change_frame_in_video(path_video, img, random_frame)
#
#
# unload_text_from_video('output_text.avi', img,  pozitii_chr, random_frame)

