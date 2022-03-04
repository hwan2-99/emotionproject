# all emotions on RAVDESS dataset
import glob
import os

import numpy as np
from pydub import AudioSegment
from sklearn.model_selection import train_test_split

from voiceEmotion.utils import extract_feature

int2emotion = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fear",
    "07": "disgust",
    "08": "surprised"
}

# 학습시킬 감정들의 목록 작성
AVAILABLE_EMOTIONS = {
    # "angry",
    # "sad",
    "happy",
    "neutral",
    "fear",
}

def load_data(test_size=0.2):
    x, y = [], []
    for file in glob.glob("data/Actor_*/*.wav"):
        # 오디오 파일의 기본 이름 가져오기
        basename = os.path.basename(file)
        # sound = AudioSegment.from_wav(file)

        # 감정표현 받기
        emotion = int2emotion[basename.split("-")[2]]

        print(emotion)

        # 감정중 설정한 감정만 허용하기
        if emotion not in AVAILABLE_EMOTIONS:
            continue
        # 음성 특징 추출

        # sound = sound.set_channels(1)
        # sound.export("data/02-01-06-1.wav", format="wav")

        features = extract_feature(file, mfcc=True, chroma=True, mel=True)
        # print(features)
        # 데이터 추가
        x.append(features)
        y.append(emotion)

    # 데이터를 훈련과 테스트를 분할하여 반환한다. split the data to training and testing and return it
    return train_test_split(np.array(x), y, test_size=test_size, random_state=7)