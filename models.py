from datetime import datetime
from main import db,secret_key
# from flask_admin.contrib.sqla import ModelView
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    def save(self):
        db.session.add(self)
        db.session.commit()
    def merge(self):
        db.session.merge(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(BaseModel):
    __tablename__ = 'user'
    username = db.Column(db.String(128), unique=True)
    firstname = db.Column(db.String(128), default=None)
    password = db.Column(db.String(128), default=None)
    email = db.Column(db.String(254), default=None)
    description = db.Column(db.String(512), default=None)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    created = db.Column(db.DATETIME,index=True,default=datetime.now)
    last_login = db.Column(db.DATETIME)

    def __init__(self, username, firstname, password, email, description, is_staff, is_active, is_superuser, created, last_login):
        self.username = username
        self.firstname = firstname
        self.password = self.hash_password(password)
        self.email = email
        self.description = description
        self.is_staff = is_staff
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.created = created
        self.last_login = last_login

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        return self.password_hash

    def verify_password(self, password, h_password):
        return pwd_context.verify(password, h_password)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({ 'id': self.id })
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
    
    def user_schema(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "password": self.password,
            "email": self.email,
            "description": self.description,
            "is_staff": self.is_staff,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created": self.created,
            "last_login": self.last_login
        }
    # def __repr__(self):
    #     return '%r,%r,%r' %(self.username, self.password, self.is_staff)
class Patient(BaseModel):
    __tablename__ = 'patient'
    patient_name = db.Column(db.String(128), unique=True)
    patient_sex = db.Column(db.Boolean, default=False)
    patient_age = db.Column(db.Integer, default=0)
    patient_address = db.Column(db.String(250), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DATETIME,index=True,default=datetime.now)

    def __init__(self, patient_name, patient_sex, patient_age, patient_address, user_id, created):
        self.patient_name = patient_name
        self.patient_sex = patient_sex
        self.patient_age = patient_age
        self.patient_address = patient_address
        self.created = created
        self.user_id = user_id

    def patient_schema(self):
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "patient_sex": self.patient_sex,
            "patient_age": self.patient_age,
            "patient_address": self.patient_address,
            "user_id": self.user_id,
            "created": self.created
        }


class Voice(BaseModel):
    __tablename__ = 'voice'
    voice_name = db.Column(db.String(128), unique=True)
    voice_file = db.Column(db.String(250), default=None)
    voice_text = db.Column(db.Text, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    created = db.Column(db.DATETIME,index=True,default=datetime.now)

    def __init__(self, voice_name, voice_file, voice_text, user_id, patient_id, created):
        self.voice_name = voice_name
        self.voice_file = voice_file
        self.voice_text = voice_text
        self.user_id = user_id
        self.patient_id = patient_id
        self.created = created
    
    def voice_schema(self):
        return {
            "id": self.id,
            "voice_name": self.voice_name,
            "voice_file": self.voice_file,
            "voice_text": self.voice_text,
            "user_id": self.user_id,
            "patient_id": self.patient_id,
            "created": self.created
        }

class SysParameters(BaseModel):
    __tablename__ = 'sys_parameters'
    baidu_app_id = db.Column(db.String(100), default=None)
    baidu_app_key = db.Column(db.String(100), default=None)
    baidu_secret_key = db.Column(db.String(100), default=None)
    baidu_service_id = db.Column(db.String(100), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, baidu_app_id, baidu_app_key, baidu_secret_key, baidu_service_id,user_id):
        self.baidu_app_id = baidu_app_id
        self.baidu_app_key = baidu_app_key
        self.baidu_secret_key = baidu_secret_key
        self.baidu_service_id = baidu_service_id
        self.user_id = user_id

    def sys_parameters_schema(self):
        return {
            "id": self.id,
            "baidu_app_id": self.baidu_app_id,
            "baidu_app_key": self.baidu_app_key,
            "baidu_secret_key": self.baidu_secret_key,
            "baidu_service_id": self.baidu_service_id,
            "user_id": self.user_id
        }

# class VoiceText(BaseModel):
#     __tablename__ = 'voice_text'
#     voice_text = db.Column(db.String(1024), default=None)
#     voice_id = db.Column(db.Integer, db.ForeignKey('voice.id'))
#     created = db.Column(db.DATETIME,index=True,default=datetime.now)

#     def __init__(self, voice_text, voice_id, created):
#         self.voice_text = voice_text
#         self.voice_id = voice_id
#         self.created = created
    
#     def voice_text_schema(self):
#         return {
#             "id": self.id,
#             "voice_text": self.voice_text,
#             "voice_id": self.voice_id,
#             "created": self.created
#         }

