from api.utils import file_util
import wave
import os
from aip import AipSpeech
from pydub import AudioSegment


class BaiduSpeechRecognition(object):
    def __init__(self):
        pass

    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def save_wave_file(self, filename, data):
        '''save the date to the wavfile'''
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes(b"".join(data))
        wf.close()

    def transfor_audio(file_path, out_file_path):
        try:
            cmd = "ffmpeg -i {0} -ac 1 {1}".format(file_path, out_file_path)
            print("命令:", cmd)
            os.system(cmd)
            song = AudioSegment.from_wav(out_file_path).set_frame_rate(16000)
            song.export(out_file_path, format='wav')
        except:
            print("转换出错")
            result = {'code': 800, 'msg': 'transfor faild'}
            return result

    def _algorithm(self, param_dict, file_path):
        result = {'code': 200, 'msg': None}
        wave_file = wave.open(file_path, 'r')
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        print("帧率：", frame_rate)
        print("通道：", channels)
        wave_file.close()
        out_file_path = file_path
        if frame_rate != 16000 or channels != 1:
            out_file_path = file_path[:-4]+'_out.wav'
            BaiduSpeechRecognition.transfor_audio(file_path, out_file_path)
        
        client = AipSpeech(param_dict['baidu_app_id'], param_dict['baidu_app_key'], param_dict['baidu_secret_key'])
        reg = client.asr(BaiduSpeechRecognition.get_file_content(out_file_path), 'wav', 16000, {'lan': 'zh'})
        print("结果:", reg)
        if os.path.exists(file_path):
            os.remove(file_path)

        if os.path.exists(out_file_path):
            os.remove(out_file_path)

        if reg['err_no'] == 0:
            result['msg'] = reg['result'][0]
        elif reg['err_no'] == 2000:
            result['code'] = 300
            result['msg'] = 'data empty'
        elif reg['err_no'] == 3301:
            result['code'] = 400
            result['msg'] = '音频质量过差'
        elif reg['err_no'] == 3308:
            result['code'] = 500
            result['msg'] = '音频过长,不超过60s'
        elif reg['err_no'] == 3311:
            result['code'] = 600
            result['msg'] = '采样率不是16000'
        else:
            result['code'] = 700
            result['msg'] = '识别错误'
        return result