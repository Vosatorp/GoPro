import cv2
import matplotlib.pyplot as plt
import numpy as np

from pytube import YouTube
import os

from collections import deque
from arguments import get_args

import cv2
import hashlib

def hash_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_hashes = {}
    timestamp = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Преобразование кадра в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Вычисление хеша кадра
        frame_hash = hashlib.sha256(gray).hexdigest()

        # Присвоение хешу значения времени
        frame_hashes[frame_hash] = timestamp

        # Обновление временного штампа
        timestamp += 1 / cap.get(cv2.CAP_PROP_FPS)

    cap.release()

    return frame_hashes


def find_transition(frame_hashes, threshold=0.9):
    cap = cv2.VideoCapture(video_path)
    # Читаем первый кадр
    ret, prev_frame = cap.read()
    print('ret:', ret)
    # Преобразуем кадр в градации серого
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    diffs = []
    fps = cap.get(cv2.CAP_PROP_FPS)  # получение количества кадров в секунду
    print('fps', fps)
    transitions = []
    last_time = -1
    MAXLEN = 7
    MIN_EPISODE = 2.0
    stack_frames = deque([prev_gray] * MAXLEN, maxlen=MAXLEN)
    while cap.isOpened():
        # Читаем следующий кадр
        ret, curr_frame = cap.read()
        if not ret:
            break
        # Преобразуем текущий кадр в градации серого
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        # Вычисляем разницу между текущим и предыдущим кадром
        frame_diffs = [cv2.absdiff(curr_gray, prev_gray) for prev_gray in stack_frames]
        diff = sum(np.linalg.norm(frame_diff) for frame_diff in frame_diffs)
        diffs.append(diff)
        if diff > 32_000 * MAXLEN:
            transition_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # получение времени перехода в секундах
            if transition_time - last_time > MIN_EPISODE:
                transitions.append(transition_time)
                last_time = transition_time
                print('diff:', diff, ' time:', transition_time)
                # plt.imshow(curr_frame)
                # plt.title(transition_time)
                # plt.show()

        stack_frames.append(curr_gray)
    return transitions


def main(video_path, folder_path):
    # timestamps = get_timestamps(video_path)
    return

if __name__ == "__main__":
    args = get_args()
    main(args.video_path, args.folder_path
