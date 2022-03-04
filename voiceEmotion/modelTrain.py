"""
# 전체 파이프 라인 설명
1. 데이터 세트 준비
2. 데이터 세트 로드
3. 모델 학습
4. 모델 테스트
"""

# 오디오 파일 읽기
import soundfile
import numpy as np
# 음성 특징 추출
import librosa
import glob
import os
# 모델 훈련결과 담기
import pickle
# 훈련, 시험 분리
from sklearn.model_selection import train_test_split
# Multi-layer 퍼셉트론 모델
from sklearn.neural_network import MLPClassifier
# 모델 측정결과 확인
from sklearn.metrics import accuracy_score

# load RAVDESS dataset, 75% training 25% testing
from voiceEmotion.data_load import load_data


def modelTrain():
    x_train, x_test, y_train, y_test = load_data(test_size=0.25)

    # print some details
    # number of samples in training data
    print("[+] Number of training samples:", x_train.shape[0])
    # number of samples in testing data
    print("[+] Number of testing samples:", x_test.shape[0])
    # number of features used
    # this is a vector of features extracted
    # using extract_features() function
    print("[+] Number of features:", x_train.shape[1])

    # best model, determined by a grid search
    model_params = {
        'alpha': 0.01,
        'batch_size': 245,
        'epsilon': 1e-08,
        'hidden_layer_sizes': (300,),
        'learning_rate': 'adaptive',
        'max_iter': 500,
    }

    # initialize Multi Layer Perceptron classifier
    # with best parameters ( so far )
    model = MLPClassifier(**model_params)

    # train the model
    print("[*] Training the model...")
    model.fit(x_train, y_train)

    # predict 25% of data to measure how good we are
    y_pred = model.predict(x_test)

    # calculate the accuracy
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)

    print("Accuracy: {:.2f}%".format(accuracy * 100))

    # now we save the model
    # make result directory if doesn't exist yet
    if not os.path.isdir("result"):
        os.mkdir("result")

    pickle.dump(model, open("result/mlp_custom_classifier.model", "wb"))

