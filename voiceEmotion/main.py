import pyaudio
import os
import wave
import pickle
from sys import byteorder
from array import array
from struct import pack
# from sklearn.neural_network import MLPClassifier

from voiceEmotion.utils import extract_feature
from voiceEmotion.modelTrain import modelTrain

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 16000

SILENCE = 30


def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i * times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"

    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds * RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds * RATE))])
    return r


def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.
    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=True,
                    frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > SILENCE:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    print("record")
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def record_to_user_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


# if __name__ == "__main__":
#     # load the saved model (after training)
#     model = pickle.load(open("result/mlp_classifier.model", "rb"))
#     print("Please talk")
#     # filename = "test.wav"
#     # # record the file (start talking)
#     # record_to_file(filename)
#     # extract features and reshape it
#     features = extract_feature("test.wav", mfcc=True, chroma=True, mel=True).reshape(1, -1)
#
#     # predict
#     proba = model.predict_proba(features)[0]
#
#     result = {}
#     voice_key = 'null'
#     temp_value = 0
#     for emotion, prob in zip(model.classes_, proba):
#
#         result[emotion] = prob
#
#         if(result[emotion] >  temp_value):
#             temp_value = result[emotion]
#             voice_key = emotion
#     # show the result !
#
#     # result 결과가 높을 경우에 재 학습을 백그라운드에서 시킨다.
#     # 현재 결과 값이 높을 경우는 처리 되지 않았고 결과값이 오류를 발생시켰을 경우 예외처리를 추가해야 한다.
#     print(voice_key)
#     # if(result[voice_key] > 0.8):
#     file_list = os.listdir('data/Actor_2')
#     count = 0
#
#     if(voice_key == 'neutral'):
#         for file_name in file_list:
#             if ('01' == file_name.split("-")[1]):
#                 if('01' == file_name.split("-")[2]):
#                     if(count < (int((file_name.split("-")[3]).split(".")[0]))):
#                         count = (int((file_name.split("-")[3]).split(".")[0]))
#
#         record_to_user_file('data/Actor_2/02-01-01-' + str(count + 1) + '.wav')
#
#     if (voice_key == 'fear'):
#         for file_name in file_list:
#             if ('01' == file_name.split("-")[1]):
#                 if ('06' == file_name.split("-")[2]):
#                     if (count < (int((file_name.split("-")[3]).split(".")[0]))):
#                         count = (int((file_name.split("-")[3]).split(".")[0]))
#
#         record_to_user_file('data/Actor_2/02-01-06-' + str(count + 1) + '.wav')
#
#     print("result:", result)

# 모델 재 학습
# modelTrain()

def emotionCheck():
    # load the saved model (after training)
    model = pickle.load(open("voiceEmotion/result/mlp_classifier.model", "rb"))
    #print("Please talk")
    # filename = "voiceEmotion/test.wav"
    # # record the file (start talking)
    # record_to_file(filename)
    # extract features and reshape it
    features = extract_feature("voiceEmotion/test.wav", mfcc=True, chroma=True, mel=True).reshape(1, -1)

    # predict
    proba = model.predict_proba(features)[0]

    result = {}
    voice_key = 'null'
    temp_value = 0
    for emotion, prob in zip(model.classes_, proba):

        result[emotion] = prob

        if (result[emotion] > temp_value):
            temp_value = result[emotion]
            voice_key = emotion
    # show the result !

    # result 결과가 높을 경우에 재 학습을 백그라운드에서 시킨다.
    # 현재 결과 값이 높을 경우는 처리 되지 않았고 결과값이 오류를 발생시켰을 경우 예외처리를 추가해야 한다.
    # print(voice_key)
    # if(result[voice_key] > 0.8):
    # file_list = os.listdir('voiceEmotion/data/Actor_2')
    # count = 0
    #
    # if (voice_key == 'neutral'):
    #     for file_name in file_list:
    #         if ('01' == file_name.split("-")[1]):
    #             if ('01' == file_name.split("-")[2]):
    #                 if (count < (int((file_name.split("-")[3]).split(".")[0]))):
    #                     count = (int((file_name.split("-")[3]).split(".")[0]))
    #
    #     record_to_user_file('voiceEmotion/data/Actor_2/02-01-01-' + str(count + 1) + '.wav')
    #
    # if (voice_key == 'fear'):
    #     for file_name in file_list:
    #         if ('01' == file_name.split("-")[1]):
    #             if ('06' == file_name.split("-")[2]):
    #                 if (count < (int((file_name.split("-")[3]).split(".")[0]))):
    #                     count = (int((file_name.split("-")[3]).split(".")[0]))
    #
    #     record_to_user_file('voiceEmotion/data/Actor_2/02-01-06-' + str(count + 1) + '.wav')

    # print("result:", result)

    return result


####

# """
# # 전체 파이프 라인 설명
# 1. 데이터 세트 준비
# 2. 데이터 세트 로드
# 3. 모델 학습
# 4. 모델 테스트
# """
#
# # 오디오 파일 읽기
# import soundfile
# import numpy as np
# # 음성 특징 추출
# import librosa
# import glob
# import os
# # 모델 훈련결과 담기
# import pickle
# # 훈련, 시험 분리
# from sklearn.model_selection import train_test_split
# # Multi-layer 퍼셉트론 모델
# from sklearn.neural_network import MLPClassifier
# # 모델 측정결과 확인
# from sklearn.metrics import accuracy_score
#
# # load RAVDESS dataset, 75% training 25% testing
# from data_load import load_data
#
# x_train, x_test, y_train, y_test = load_data(test_size=0.25)
#
# # print some details
# # number of samples in training data
# print("[+] Number of training samples:", x_train.shape[0])
# # number of samples in testing data
# print("[+] Number of testing samples:", x_test.shape[0])
# # number of features used
# # this is a vector of features extracted
# # using extract_features() function
# print("[+] Number of features:", x_train.shape[1])
#
# # best model, determined by a grid search
# model_params = {
#     'alpha': 0.01,
#     'batch_size': 1,
#     'epsilon': 1e-08,
#     'hidden_layer_sizes': (300,),
#     'learning_rate': 'adaptive',
#     'max_iter': 500,
# }
#
# # initialize Multi Layer Perceptron classifier
# # with best parameters ( so far )
# model = MLPClassifier(**model_params)
#
# # train the model
# print("[*] Training the model...")
# model.fit(x_train, y_train)
#
# # predict 25% of data to measure how good we are
# y_pred = model.predict(x_test)
#
# # calculate the accuracy
# accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
#
# print("Accuracy: {:.2f}%".format(accuracy*100))
#
# # now we save the model
# # make result directory if doesn't exist yet
# if not os.path.isdir("result"):
#     os.mkdir("result")
#
# pickle.dump(model, open("result/mlp_classifier.model", "wb"))
def voiceEmotion():
    return None
