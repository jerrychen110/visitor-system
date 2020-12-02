from main import db,api,basedir
from flask import g,request,jsonify,abort,session
from flask_restful import Resource

from models import *
from werkzeug.utils import secure_filename
import os,sys,time
from datetime import datetime
# from distutils.util import strtobool
# from utils import image_process, port_util, file_util

import importlib
import base64
import wave,audioop,time
from aip import AipSpeech
from utils.recorder import Recorder
from utils import gmm_vad
import threading 

UPLOAD_PATH = os.path.join(basedir, 'static/uploads/')
VOICES_PATH = os.path.join(UPLOAD_PATH,'voices/')
TEMP_PATH = os.path.join(UPLOAD_PATH,'temps/')
ALGORITHM_PATH = os.path.join(UPLOAD_PATH,'algorithms')
MODELS_PATH = os.path.join(UPLOAD_PATH,'models')
sys.path.append(ALGORITHM_PATH)
sys.path.append(MODELS_PATH)

started_list = []
rec = Recorder()

class TokenResource(Resource):
    # decorators = [auth.login_required]
    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({ 'token': token.decode('ascii') })

class LoginResource(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        result = {}
        if (self.verify_auth(username, password)):
            user = User.query.filter_by(username=username).first()
            last_login = datetime.utcnow()
            user.last_login = last_login
            user.merge()
            if user.is_superuser == True:
                result = {"msg": username+" login successful!", "code":200,"username":username,"id":user.id,"is_superuser":user.is_superuser}
            elif user.is_staff == True:
                result = {"msg": username+" login successful!", "code":200,"username":username,"id":user.id,"is_staff":user.is_staff}
            return jsonify(result) 
        result = {"msg": username+" login failure!", "code":201}
        return jsonify(result) 
    def verify_auth(self, username_or_token, password):
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password,user.password):
            return False
        session['username'] = user.username
        t = user.generate_auth_token()
        token = { 'token': t.decode('ascii') }
        session['token'] = token
        # g.username = user
        return True

class LogoutResource(Resource):
    def post(self):
        session.clear()
        return True


class RegisterResource(Resource):
    def post(self):
        username = request.json['username']
        firstname = request.json['first_name']
        password = request.json['password']
        email = ""
        description = None
        created = datetime.utcnow()
        last_login = None
        result = {}
        if (self.verify_username(username)):
            user = User(username=username,firstname=firstname,password=password,email=email,description=description,is_staff=1,is_active=1,is_superuser=0,created=created,last_login=last_login)
            user.save()
            result = {"msg": username+" register successful!", "code":200}
            return jsonify(result) 
        else:
            result = {"msg": username+" has already registered", "code":300}
            return jsonify(result) 

    def verify_username(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return True
        return False

class UserListResource(Resource):
    # decorators = [auth.login_required]
    def get(self):
        users = User.query.all()
        user_list = []
        for i in users:
            user_serialize = i.user_schema()
            user_list.append(user_serialize)
        return jsonify(user_list)

    def post(self):
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        password = request.form.get('password')
        email = request.form.get('email')
        description = request.form.get('description')
        is_staff = request.form.get('is_staff')
        is_active = request.form.get('is_active')
        is_superuser = request.form.get('is_superuser')
        created = datetime.utcnow()
        last_login = None
        msg = {}
        if username is None or password is None:
            msg = {"msg": "username or password are None!", "code":500}
            return jsonify(msg)
        if User.query.filter_by(username = username).first() is not None:
            msg = {"msg": username+" is exist!", "code":400}
            return jsonify(msg)
        is_staff = True if(is_staff == "true") else False
        is_active = True if(is_active == "true") else False
        is_superuser = True if(is_superuser == "true") else False

        user = User(username=username,firstname=firstname,password=password,email=email,description=description,is_staff=is_staff,is_active=is_active,is_superuser=is_superuser,created=created,last_login=last_login)
        user.save()
        msg = {"msg": "create "+username+" successful!", "code":200}
        return jsonify(msg)

class UserResource(Resource):
    # decorators = [auth.login_required]
    def get(self,user_id):
        user = User.query.get_or_404(user_id)
        user_serialize = user.user_schema()
        return jsonify(user_serialize)

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        firstname = request.form.get('firstname')
        password = request.form.get('password')
        email = request.form.get('email')
        description = request.form.get('description')
        is_staff = request.form.get('is_staff')
        is_active = request.form.get('is_active')
        is_superuser = request.form.get('is_superuser')

        if (password is not None and password != ""):
            user.password = password
        if(firstname is not None and firstname != ""):
            user.firstname = firstname
        if(email is not None and email != ""):
            user.email = email
        if(description is not None and description != ""):
            user.description = description
        user.is_staff = True if(is_staff == "true") else False
        user.is_active = True if(is_active == "true") else False
        user.is_superuser = True if(is_superuser == "true") else False
        user.merge()
        user_serialize = user.user_schema()
        return jsonify(user_serialize)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        user.delete()
        return 'delete successful',204

class PatientListResource(Resource):
    def get(self):
        patients = Patient.query.all()
        patient_list = []
        for i in patients:
            patient_serialize = i.patient_schema()
            patient_list.append(patient_serialize)
        return jsonify(patient_list)

    def post(self):
        patient_name = request.form.get('patient_name')
        patient_sex = request.form.get('patient_sex')
        patient_age = int(request.form.get('patient_age'))
        patient_address = request.form.get('patient_address')
        user_id = request.form.get('user_id')
        created = datetime.utcnow()
        result = {}
        if patient_name is None:
            result = {"msg": "patient name is None!", "code":500}
            return jsonify(result)
        patient_sex = True if(patient_sex == "true") else False
        patient = Patient(patient_name=patient_name,patient_sex=patient_sex,patient_age=patient_age,patient_address=patient_address,user_id=user_id,created=created)
        patient.save()
        result = {"msg": "create "+patient_name+" successful!", "code":200}
        return jsonify(result)

class PatientResource(Resource):
    def get(self,patient_id):
        patient = Patient.query.get_or_404(patient_id)
        patient_serialize = patient.patient_schema()
        return jsonify(patient_serialize)

    def put(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        patient_name = request.form.get('patient_name')
        patient_sex = request.form.get('patient_sex')

        patient_age = int(request.form.get('patient_age'))
        patient_address = request.form.get('patient_address')
        if (patient_name is not None and patient_name != ""):
            patient.patient_name = patient_name
        if (patient_age is not None and patient_age != 0):
            patient.patient_age = patient_age
        if (patient_address is not None and patient_address != ""):
            patient.patient_address = patient_address
        patient.patient_sex = True if(patient_sex == "true") else False
        patient.merge()
        patient_serialize = patient.patient_schema()
        return jsonify(patient_serialize)

    def delete(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        patient.delete()
        return 'delete successful',204

class VoiceListResource(Resource):

    def get(self):
        voices = Voice.query.all()
        voice_list = []
        for i in voices:
            voice_serialize = i.voice_schema()
            voice_list.append(voice_serialize)
        return jsonify(voice_list)
    
    def post(self):
        voice_file = request.files.get('voice_file')
        voice_ext = voice_file.filename.split(".")
        voice_name = str(int(time.time()))+"."+str(voice_ext[1])
        voice_text = request.form.get('voice_text')
        user_id = int(request.form.get("user_id"))
        patient_id = request.form.get("patient_id")
        print(patient_id)
        voice_path = "static/uploads/"+voice_name

        upload_path=os.path.join(VOICES_PATH,secure_filename(voice_name))
        created = datetime.utcnow()
        voice = Voice(voice_name=voice_name,voice_file=voice_path,voice_text=voice_text,user_id=user_id,patient_id=patient_id,created=created)
        voice_file.save(upload_path)
        voice.save()
        voice_serialize = voice.voice_schema()
        return jsonify(voice_serialize)

class VoiceResource(Resource):

    def get(self,voice_id):
        voice = Voice.query.get_or_404(voice_id)
        voice_serialize = voice.voice_schema()
        return jsonify(voice_serialize)

    def put(self, voice_id):

        voice = Voice.query.get_or_404(voice_id)
        voice_file = request.files.get('voice_file')
        
        voice_text = request.form.get("voice_text")
        user_id = request.form.get("user_id")
        patient_id = request.form.get("patient_id")

        if(voice_file is not None and voice_file != ""):
            voice_ext = voice_file.filename.split(".")
            voice_name = str(int(time.time()))+"."+str(voice_ext[1])
            upload_path=os.path.join(VOICES_PATH,secure_filename(voice_name))
            voice_file.save(upload_path)
            voice.voice_file = "static/uploads/"+voice_name
        if(user_id is not None):
            voice.user_id = int(user_id)
        if(patient_id is not None):
            voice.patient_id = int(patient_id)
        if(voice_text is not None and voice_text != ""):
            voice.voice_text = voice_text
        voice.merge()
        voice_serialize = voice.voice_schema()
        return jsonify(voice_serialize)

    def delete(self, voice_id):
        voice = Voice.query.get_or_404(voice_id)
        voice.delete()
        return 'delete successful',204

class SysParametersListResource(Resource):
    def get(self):
        sys_parameters = SysParameters.query.all()
        sys_parameters_list = []
        for i in sys_parameters:
            sys_parameters_serialize = i.sys_parameters_schema()
            sys_parameters_list.append(sys_parameters_serialize)
        return jsonify(sys_parameters_list)

    def post(self):
        baidu_app_id = request.form.get('baidu_app_id')
        baidu_app_key = request.form.get('baidu_app_key')
        baidu_secret_key = request.form.get('baidu_secret_key')
        baidu_service_id = request.form.get('baidu_service_id')
        user_id = int(request.form.get('user_id'))

        result = {}
        sys_parameters = SysParameters(baidu_app_id=baidu_app_id,baidu_app_key=baidu_app_key,baidu_secret_key=baidu_secret_key,baidu_service_id=baidu_service_id,user_id=user_id)
        sys_parameters.save()
        result = {"msg": "create successful!", "code":200}
        return jsonify(result)

class SysParametersResource(Resource):
    def get(self,sys_parameter_id):
        sys_parameters = SysParameters.query.get_or_404(sys_parameter_id)
        sys_parameters_serialize = sys_parameters.sys_parameters_schema()
        return jsonify(sys_parameters_serialize)

    def put(self, sys_parameter_id):
        sys_parameters = SysParameters.query.get_or_404(sys_parameter_id)
        baidu_app_id = request.form.get('baidu_app_id')
        baidu_app_key = request.form.get('baidu_app_key')
        baidu_secret_key = request.form.get('baidu_secret_key')
        baidu_service_id = request.form.get('baidu_service_id')

        if (baidu_app_id is not None and baidu_app_id != ""):
            sys_parameters.baidu_app_id = baidu_app_id
        if (baidu_app_key is not None and baidu_app_key != ""):
            sys_parameters.baidu_app_key = baidu_app_key
        if (baidu_secret_key is not None and baidu_secret_key != ""):
            sys_parameters.baidu_secret_key = baidu_secret_key
        if (baidu_service_id is not None and baidu_service_id != ""):
            sys_parameters.baidu_service_id = baidu_service_id
        sys_parameters.merge()
        sys_parameters_serialize = sys_parameters.sys_parameters_schema()
        return jsonify(sys_parameters_serialize)

    def delete(self, sys_parameter_id):
        sys_parameters = SysParameters.query.get_or_404(sys_parameter_id)
        sys_parameters.delete()
        return 'delete successful',204

class QueryUserResource(Resource):
    def get(self):
        page = int(request.args.get("page"))
        page_size = request.args.get("page-size")
        username = request.args.get("username", None)
        if username is not None:
            page_size = page_size if page_size is not None else 8
            pagination = User.query.filter(User.username.like("%" + username + "%")).paginate(page=page, per_page=page_size)
            total = pagination.total
            list_view = pagination.items
            user_list = []
            results = {}
            for i in list_view:
                user_serialize = i.user_schema()
                user_list.append(user_serialize)
            results = {"results":user_list,"total":total}
            return jsonify(results)
        else:
            page_size = page_size if page_size is not None else 8
            pagination = User.query.paginate(page=page, per_page=page_size)
            total = pagination.total
            list_view = pagination.items
            user_list = []
            results = {}
            for i in list_view:
                user_serialize = i.user_schema()
                user_list.append(user_serialize)
            results = {"results":user_list,"total":total}
            return jsonify(results)

class QueryPatienResource(Resource):
    def get(self):
        page = int(request.args.get("page"))
        page_size = request.args.get("page-size")
        patient_name = request.args.get("patient_name", None)
        if patient_name is not None:
            page_size = page_size if page_size is not None else 8
            user_id = request.args.get("user_id")
            pagination = Patient.query.filter(Patient.patient_name.like("%" + patient_name + "%")).paginate(page=page, per_page=page_size)
            total = pagination.total
            list_view = pagination.items
            patient_list = []
            results = {}
            for i in list_view:
                patient_serialize = i.patient_schema()
                patient_list.append(patient_serialize)
            results = {"results":patient_list,"total":total}
            return jsonify(results)
        else:
            page_size = page_size if page_size is not None else 8
            user_id = request.args.get("user_id")
            pagination = Patient.query.filter_by(user_id=user_id).paginate(page=page, per_page=page_size)
            total = pagination.total
            list_view = pagination.items
            patient_list = []
            results = {}
            for i in list_view:
                patient_serialize = i.patient_schema()
                patient_list.append(patient_serialize)
            results = {"results":patient_list,"total":total}
            return jsonify(results)

class QueryVoiceResource(Resource):
    def get(self):
        page = int(request.args.get("page"))
        page_size = request.args.get("page-size")
        voice_text = request.args.get("voice_text", None)
        voices = Voice.query.all()
        results = {}
        if len(voices) > 0:
            if voice_text is not None:
                page_size = page_size if page_size is not None else 8
                user_id = request.args.get("user_id")
                pagination = Voice.query.filter(Voice.voice_text.like("%" + voice_text + "%")).paginate(page=page, per_page=page_size)
                total = pagination.total
                list_view = pagination.items
                voice_list = []
                
                for i in list_view:
                    voice_serialize = i.voice_schema()
                    patient_id = voice_serialize.get("patient_id")
                    patient = Patient.query.get_or_404(patient_id)
                    patient_serialize = patient.patient_schema()
                    patient_name = patient_serialize.get("patient_name")

                    user_id = voice_serialize.get("user_id")
                    user = User.query.get_or_404(user_id)
                    user_serialize = user.user_schema()
                    username = user_serialize.get("username")
                    voice_serialize["patient_name"] = patient_name
                    voice_serialize["username"] = username

                    voice_list.append(voice_serialize)
                results = {"results":voice_list,"total":total}
                return jsonify(results)
            else:
                page_size = page_size if page_size is not None else 8
                user_id = request.args.get("user_id")
                pagination = Voice.query.filter_by(user_id=user_id).paginate(page=page, per_page=page_size)
                total = pagination.total
                list_view = pagination.items
                voice_list = []
                for i in list_view:
                    voice_serialize = i.voice_schema()
                    patient_id = voice_serialize.get("patient_id")
                    patient = Patient.query.get_or_404(patient_id)
                    patient_serialize = patient.patient_schema()
                    patient_name = patient_serialize.get("patient_name")

                    user_id = voice_serialize.get("user_id")
                    user = User.query.get_or_404(user_id)
                    user_serialize = user.user_schema()
                    username = user_serialize.get("username")
                    voice_serialize["patient_name"] = patient_name
                    voice_serialize["username"] = username

                    voice_list.append(voice_serialize)
                results = {"results":voice_list,"total":total}
                return jsonify(results)
        else:
            results = {"msg": "empty voice", "code":404}
        
        return jsonify(results)

class QueryPatientRecordResource(Resource):
    def get(self):
        page = int(request.args.get("page"))
        page_size = int(request.args.get("page-size"))
        user_id = request.args.get("user_id")
        patient_id = request.args.get("patient_id")
        now_time=str(datetime.utcnow())
        now_dat = datetime.strptime(now_time.split(' ')[0],'%Y-%m-%d')
        print(now_dat)
        voices = Voice.query.filter_by(user_id=user_id).all()
        results = {}

        if len(voices) > 0:
            page_size = page_size if page_size is not None else 8
            user_id = request.args.get("user_id")
            pagination = Voice.query.filter_by(patient_id=patient_id).paginate(page=page, per_page=page_size)
            # pagination=Voice.query.filter(Voice.created < now_dat_time).all()
            print(pagination)
            total = pagination.total
            list_view = pagination.items
            voice_name_list = []
            tmp_list = []
            voice_files = []
            
            for i in list_view:
                voice_serialize = i.voice_schema()

                voice_name = voice_serialize.get("voice_name").split("-")
                tmp_list.append(voice_name[0])
            
            for j in tmp_list:
                if j not in voice_name_list:
                    voice_name_list.append(j)

            total_voice = []
            total_result = {}
            for k in voice_name_list: 
                voice_file_list = []
                voice_files = Voice.query.filter(Voice.voice_name.like('%'+k+'%')).all()
                for l in voice_files:
                    voice_file_dict = {}
                    voice_files_serialize = l.voice_schema()
                    voice_name = voice_files_serialize.get("voice_name")
                    voice_file = voice_files_serialize.get("voice_file")
                    voice_text = voice_files_serialize.get("voice_text")
                    created = voice_files_serialize.get("created")
                    voice_file_dict["voice_name"] = voice_name
                    voice_file_dict["voice_file"] = voice_file
                    voice_file_dict["voice_text"] = voice_text
                    voice_file_dict["created"] = created

                    voice_file_list.append(voice_file_dict)
                total_voice.append(voice_file_list)

            patient = Patient.query.get_or_404(patient_id)
            patient_serialize = patient.patient_schema()
            patient_name = patient_serialize.get("patient_name")
            user = User.query.get_or_404(user_id)
            user_serialize = user.user_schema()
            username = user_serialize.get("username")
            total_result['patient_name'] = patient_name
            total_result['username'] = username
            total_result['voices'] = total_voice

            # print("Str:"+str(total_voice))

            results = {"results":total_result,"total":total,"visit_count":len(total_voice)}
            return jsonify(results)
        else:
            results = {"msg": "empty voice", "code":404}
        
        return jsonify(results)
class ApiPatientListResource(Resource):
    def get(self,user_id):
        patients = Patient.query.filter_by(user_id=user_id).all()
        patient_list = []
        for i in patients:
            patient_serialize = i.patient_schema()
            patient_list.append(patient_serialize)
        results = {"results":patient_list}
        return jsonify(results)


class ApiSysParametersListResource(Resource):
    def get(self):
        user_id = int(request.args.get("userId"))
        sys_parameters = SysParameters.query.filter_by(user_id=user_id).first()
        if sys_parameters is not None:
            sys_parameters_serialize = sys_parameters.sys_parameters_schema()
            return jsonify({"result_data":sys_parameters_serialize})
        else:
            return jsonify({"result_data":{}})

    def post(self):
        user_id = request.json.get('user_id')
        baidu_app_id = request.json.get('baidu_app_id')
        baidu_app_key = request.json.get('baidu_app_key')
        baidu_secret_key = request.json.get('baidu_secret_key')
        baidu_service_id = request.json.get('baidu_service_id')
        result = {}
        sys_parameters = SysParameters.query.filter_by(user_id=user_id).first()
        if sys_parameters is None:
            sys_parameters = SysParameters(baidu_app_id=baidu_app_id,baidu_app_key=baidu_app_key,baidu_secret_key=baidu_secret_key,baidu_service_id=baidu_service_id,user_id=user_id)
            sys_parameters.save()
            result = {"msg": "create successful!", "code":200}
        else:
            if (baidu_app_id is not None and baidu_app_id != ""):
                sys_parameters.baidu_app_id = baidu_app_id
            else:
                sys_parameters.baidu_app_id = ""
            if (baidu_app_key is not None and baidu_app_key != ""):
                sys_parameters.baidu_app_key = baidu_app_key
            else:
                sys_parameters.baidu_app_key = ""
            if (baidu_secret_key is not None and baidu_secret_key != ""):
                sys_parameters.baidu_secret_key = baidu_secret_key
            else:
                sys_parameters.baidu_secret_key = ""
            if (baidu_service_id is not None and baidu_service_id != ""):
                sys_parameters.baidu_service_id = baidu_service_id
            else:
                sys_parameters.baidu_service_id = ""
            sys_parameters.merge()
            result = {"msg": "update successful!", "code":201}
        return jsonify(result)

class BaiduSpeechRecognition(Resource):
    def post(self):
        result = {'code': 200, 'msg': None}
        
        user_id = request.form.get('user_id')
        patient_id = request.form.get('patient_id')
        created = datetime.utcnow()

        sys_parameters = SysParameters.query.filter_by(user_id=user_id).first()
        sys_parameters_serialize = sys_parameters.sys_parameters_schema()

        voice_file = request.files.get('file1_name')
        voice_ext = voice_file.filename.split(".")
        voice_name = str(int(time.time()))+"."+str(voice_ext[1])
        temp_path=os.path.join(TEMP_PATH,secure_filename(voice_name))
        upload_path=os.path.join(VOICES_PATH,secure_filename(voice_name))
        voice_file.save(temp_path)
        self.trans_wave_file(temp_path,upload_path)
        client = AipSpeech(sys_parameters_serialize.get('baidu_app_id'), sys_parameters_serialize.get('baidu_app_key'), sys_parameters_serialize.get('baidu_secret_key'))
        voice_text = client.asr(self.get_file_content(upload_path), 'wav', 16000, {'lan': 'zh'})
        print("结果:", voice_text)

        voice = Voice(voice_name=voice_name,voice_file=upload_path,voice_text=voice_text['result'][0],user_id=user_id,patient_id=patient_id,created=created)
        voice.save()

        if voice_text['err_no'] == 0:
            result['msg'] = voice_text['result'][0]
        elif voice_text['err_no'] == 2000:
            result['code'] = 300
            result['msg'] = 'data empty'
        elif voice_text['err_no'] == 3301:
            result['code'] = 400
            result['msg'] = '音频质量过差'
        elif voice_text['err_no'] == 3308:
            result['code'] = 500
            result['msg'] = '音频过长,不超过60s'
        elif voice_text['err_no'] == 3311:
            result['code'] = 600
            result['msg'] = '采样率不是16000'
        else:
            result['code'] = 700
            result['msg'] = '识别错误'
        return result
    def trans_wave_file(self, src, dst, outrate=16000, outchannels=1):
        try:
            s_read = wave.open(src, 'rb')
            params = s_read.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            print(nchannels,sampwidth, framerate,nframes)
            s_write = wave.open(dst, 'wb')

            n_frames = s_read.getnframes()
            data = s_read.readframes(n_frames)
            converted = audioop.ratecv(data, 2, nchannels, framerate, outrate, None)
            if outchannels == 1:
                converted = audioop.tomono(converted[0], 2, 1, 0)
            s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
            s_write.writeframes(converted)
        except Exception as e:
            print ('Failed to write wav')
            s_read.close()
            s_write.close()

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

class SpeechRecorder(Resource):
    def post(self):
        results = {'code': 200, 'msg': None}
        
        self.user_id = request.form.get('user_id')
        patient_id = request.form.get('patient_id')
        created = datetime.utcnow()
        status = request.form.get('status')
        voice_name = str(int(time.time()))
        # upload_path=os.path.join(VOICES_PATH,voice_name)
        print("status:"+status)
        voice_path = VOICES_PATH+patient_id
        valid_path = os.path.exists(voice_path)
        if valid_path == True:
            upload_path=voice_path+"/"+voice_name
        else:
            os.makedirs(voice_path)
        
        
        if status == "1":
            rec.start()
            print("start recording...")
            results['code'] = 301
            results['msg'] = '开始录音'
        else:
            rec.stop()
            rec.save(upload_path)
            print("stop recording!")
            print("saved:"+upload_path)
            threading._start_new_thread(self.process_voice,(upload_path,patient_id,created,))
            results['code'] = 302
            results['msg'] = '停止录音'
        return results
    
    def process_voice(self, upload_path,patient_id,created):
        sys_parameters = SysParameters.query.filter_by(user_id=self.user_id).first()
        sys_parameters_serialize = sys_parameters.sys_parameters_schema()

        is_start_api = False

        if sys_parameters_serialize.get('baidu_app_id') !="":
            is_start_api = True

        wave_file = upload_path+".wav"
        wave_file_list = gmm_vad.vad(3, wave_file)
        if is_start_api == True:
            for i in wave_file_list:
                voice_text = self.voice_recognise(i)
                new_voice_name = i[i.rindex("/")+1:]
                new_voice_path = "static/uploads/voices/"+patient_id+"/"+new_voice_name
                voice = Voice(voice_name=new_voice_name,voice_file=new_voice_path,voice_text=voice_text,user_id=self.user_id,patient_id=patient_id,created=created)
                voice.save()
        else:
            for i in wave_file_list:
                voice_text = ""
                new_voice_name = i[i.rindex("/")+1:]
                new_voice_path = "static/uploads/voices/"+patient_id+"/"+new_voice_name
                voice = Voice(voice_name=new_voice_name,voice_file=new_voice_path,voice_text=voice_text,user_id=self.user_id,patient_id=patient_id,created=created)
                voice.save()

    def voice_recognise(self, wave_file_path):
        sys_parameters = SysParameters.query.filter_by(user_id=self.user_id).first()
        sys_parameters_serialize = sys_parameters.sys_parameters_schema()

        client = AipSpeech(sys_parameters_serialize.get('baidu_app_id'), sys_parameters_serialize.get('baidu_app_key'), sys_parameters_serialize.get('baidu_secret_key'))
        voice_text = client.asr(self.get_file_content(wave_file_path), 'wav', 16000, {'lan': 'zh'})
        print("结果:", voice_text)
        return voice_text['result'][0]
    
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    
api.add_resource(TokenResource,'/API/token/')
api.add_resource(LoginResource,'/API/normal-login/')
api.add_resource(RegisterResource,'/API/register/')
api.add_resource(LogoutResource,'/API/logout/')

api.add_resource(UserListResource,'/API/base-api/user-profile/')
api.add_resource(UserResource,'/API/base-api/user-profile/<int:user_id>/')

api.add_resource(PatientListResource,'/API/base-api/patient/')
api.add_resource(PatientResource,'/API/base-api/patient/<int:patient_id>/')

api.add_resource(VoiceListResource,'/API/base-api/voice/')
api.add_resource(VoiceResource,'/API/base-api/voice/<int:voice_id>/')

api.add_resource(QueryUserResource,'/API/base-api/query-user-profile/')
api.add_resource(QueryPatienResource,'/API/base-api/query-patient/')
api.add_resource(QueryVoiceResource,'/API/base-api/query-voice/')
api.add_resource(QueryPatientRecordResource,'/API/base-api/query-patient-record/')

api.add_resource(ApiPatientListResource,'/API/base-api/api-patient/<int:user_id>/')
api.add_resource(ApiSysParametersListResource,'/API/sys-parameters-manage/')

api.add_resource(BaiduSpeechRecognition,'/API/voice-recognition/')
api.add_resource(SpeechRecorder,'/API/voice-recorder/')