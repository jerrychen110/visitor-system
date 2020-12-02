from flask import render_template,request,jsonify,redirect,url_for,session
from main import app,basedir
from models import *
# from flask_login import logout_user

@app.route('/')
def home():
    msg = None
    print(session.get('username'))
    if(session.get('username') is not None):
        return render_template('index.html', username=session.get('username'))
    return render_template('login.html')

@app.route('/login',methods=('GET', 'POST'))
def login():
    # msg = None
    # if request.method == "POST":
    #     if verify_password(request.form['username'], request.form['password']):
    #         msg = "登录成功"
    #         return redirect(url_for('home'))
    #     else:
    #         msg = "账号或密码错误！"
    #         return render_template('login.html', error=msg)
    return render_template('login.html')

@app.route('/logout')
def logout():
    # msg = None
    # if(session.get('username') is not None):
    #     session.pop("username")
    #     msg = "退出成功"
    #     return render_template('login.html', info=msg)
    return render_template('login.html')

@app.route('/register')
def register():
    # if request.method == "POST":
    #     username = request.form.get('username')
    #     fullname = request.form.get('fullname')
    #     password1 = request.form.get('password1')
    #     password2 = request.form.get('password2')
    #     created = datetime.now()
    #     msg = None
    #     if password1 != password2:
    #         msg = "两次密码不相同"
    #     elif verify_username(request.form['username']) == False:
    #         msg = "用户已注册"
    #     else:
    #         user = User(username=username,fullname=fullname,password=password1,is_staff=1,is_active=1,is_superuser=0,created=created)
    #         user.save()
    #         msg = "用户注册成功"
    #         session['username'] = user.username
    #         return render_template('index.html', info=msg)
    return render_template('register.html')

# def verify_username(username):
#     user = User.query.filter_by(username=username).first()
#     if not user:
#         return True
#     return False


# def verify_password(username_or_token, password):
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         user = User.query.filter_by(username=username_or_token).first()
#         if not user or not user.verify_password(password,user.password):
#             return False
#     session['username'] = user.username
#     return True

# @app.route('/user/new', methods=['GET','POST'])
# def new_user():
#     if request.method == "POST":
#         username = request.form.get('username')
#         fullname = request.form.get('fullname')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         created = datetime.now()
#         msg = None
#         if password1 != password2:
#             msg = "两次密码不相同"
#         elif verify_username(request.form['username']) == False:
#             msg = "用户已注册"
#         else:
#             user = User(username=username,fullname=fullname,password=password1,is_staff=1,is_active=1,is_superuser=0,created=created)
#             user.save()
#             msg = "用户注册成功！"
#         return render_template('index.html', info=msg)

# @app.route('/user/edit/<int:user_id>', methods=['GET','POST'])
# def edit_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     users = User.query.all()
#     msg = None
#     if request.method == "POST":
#         fullname = request.form.get('fullname')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         if password1 !="" and password2 !="" and password1 == password2:
#             user.password = user.hash_password(password1)
#         if fullname != "":
#             user.fullname = fullname
#         user.merge()
#         return render_template('user_management.html', users=users)
#     return render_template('edit_user.html', user=user)
        
# @app.route('/user/delete/<int:user_id>', methods=['GET'])
# def delete_user(user_id):
#     user = User.query.get_or_404(user_id)
#     user.delete()
#     users = User.query.all()
#     return render_template('user_management.html', users=users)

# @app.route('/user/list', methods=['GET'])
# def list_user():
#     users = User.query.all()
#     return render_template('user_management.html',users=users)



# @app.route('/patient/new', methods=['GET','POST'])
# def new_patient():
#     if request.method == "POST":
#         patient_name = request.form.get('patient_name')
#         patient_sex = request.form.get('patient_sex')
#         patient_age = request.form.get('patient_age')
#         patient_address = request.form.get('patient_address')
#         created = datetime.now()
#         msg = None
#         if patient_name == "":
#             msg = "请输入用户名"
#         patient = Patient(patient_name=patient_name,patient_sex=patient_sex,patient_age=patient_age,patient_address=patient_address,created=created)
#         patient.save()
#         msg = "信息录入成功！"
#         return render_template('index.html', info=msg)
#     return render_template('new_patient.html')

    