import wave
from pyaudio import PyAudio, paInt16
import time
import os
from aip import AipSpeech




framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = '/home/kevin/project/dobot-project/vioce_distinguish/speech.wav'



def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()

#录音
def my_record(t_l=4):
    pa = PyAudio()
    #打开一个新的音频stream
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = [] #存放录音数据

    os.system('clear')
    # input('press any key to start recording....')
    print('正在录音...')
    t = time.time()
 
    while time.time() < t + t_l:  # 设置录音时间（秒）
    	#循环read，每次read 2000frames
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束...')
    save_wave_file(FILEPATH, my_buf)
    stream.close()


def get_file_content(filePath):
     with open(filePath, 'rb') as fp:
        return fp.read()


def baidu_voice():
    APP_ID = '25309910'
    API_KEY = 'VenLQqKh0onHWvZ2B5BLddPj'
    SECRET_KEY = 'rwUU1iOFO0nSFnfClvy01wNHoGEvHyio'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    my_record(t_l=2)
    try:
        re = client.asr(get_file_content(FILEPATH), 'pcm', 16000, {'dev_pid': 1536, })
    except:
        re = {'err_no':0, 'err_msg':'connect to baidu-aip error,please check your web connection and code!'}

    return re












