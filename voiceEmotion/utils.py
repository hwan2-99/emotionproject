import soundfile
import librosa
import numpy as np
import matplotlib.pyplot as plt


def extract_feature(file_name, **kwargs):
    """
    오디오 파일 "file_name"에서 기능 추출
        지원되는 기능:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g:
        `features = extract_feature(path, mel=True, mfcc=True)`
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")

    #print("오디오 파일이 여기로 옴")
    #print(file_name)
    with soundfile.SoundFile(file_name) as sound_file:
        x = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
           # print("chroma or contrast")
            stft = np.abs(librosa.stft(x))
            result = np.array([])

            # print(result)
        if mfcc:
            #print("mfcc")
            mfccs = np.mean(librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=40).T, axis=0)
            # 배열을 왼쪽에서 오른쪽으로 붙이기
            result = np.hstack((result, mfccs))
            plt.title("mfcc")
            plt.plot(mfccs)
            # plt.show()

            #print(result)
        if chroma:
            #print("chroma")
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
            # plt.title("chroma")
            # plt.plot(chroma)
            # plt.show()

            #print(result)
        if mel:
            #print("mel")
            mel = np.mean(librosa.feature.melspectrogram(x, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))

            # plt.title("mel")
            # plt.plot(mel)
            # plt.show()
            #print(result)
        if contrast:
            #print("contrast")
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            #print("tonnetz")
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(x), sr=sample_rate).T, axis=0)
            result = np.hstack((result, tonnetz))
    return result
