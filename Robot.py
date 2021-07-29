  
# coding=utf-8
import json
import os
import requests
from aip import AipSpeech


BaiDu_APP_ID = '24222217'
API_KEY = 'y57KljcgS4TY3hsWi7xGAY4X'
SECRET_KEY = 'LX5Ap1Vrs0yjK3EHLe3GerrM57YlFMBi'
client = AipSpeech(BaiDu_APP_ID, API_KEY, SECRET_KEY)

turing_api_key = '67d5386150e248fea4af3db80f4ca1ae'
api_url = 'http://openapi.tuling123.com/openapi/api/v2'
headers = {'Content-Type': 'application/json;charset=UTF-8'}
host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=6KLdtAifYT46PtyzULAGpIzu&client_secret=tCEEz7LC4XfD2RA4ojgdOUvBBd7i3T4Y'
access_token = requests.get(host).json()["access_token"]
running = True
resultText, path = "", "output.wav"


def SoundRecording(path):
    import pyaudio
    import wave
    import os
    import sys
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = path
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("done")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def SpeechRecognition(path):
        with open(path, 'rb') as fp:
            voices = fp.read()
            # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
            result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537, })

            result_text = result["result"][0]
            print("you said: " + result_text)
            return result_text

def TuLing(text_words=""):
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": text_words
            },
            "selfInfo": {
                "location": {
                    "city": "天津",
                    "province": "天津",
                    "street": "天津科技大学"
                }
            }
        },
        "userInfo": {
            "apiKey": turing_api_key,
            "userId": "Leosaf"
        }
    }

    req["perception"]["inputText"]["text"] = text_words
    response = requests.request("post", api_url, json=req, headers=headers)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI Robot said: " + result)

    return result


def SpeechSynthesis(text_words=""):
    result = client.synthesis(text_words, 'zh', 1, {'per': 4, 'vol': 10, 'pit': 9, 'spd': 5})
    if not isinstance(result, dict):
        with open('app.mp3', 'wb') as f:
            f.write(result)
    os.system('mpg321 app.mp3')


if __name__ == '__main__':
    while running:
        SoundRecording(path)
        resultText = SpeechRecognition(path)
        response = TuLing(resultText)
        if '退出' in response or '再见' in response or '拜拜' in response:
            SpeechSynthesis(response)
            running = False
        SpeechSynthesis(response)
