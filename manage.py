import sys
# from views import *
from resources import *
from models import *
from main import * 
from config import *

cmd = sys.argv

if cmd[1] == 'runserver':
    if len(cmd)>2:
        host = cmd[2].split(":")[0]
        port = cmd[2].split(":")[1]
        app.run(host=host,port=port,use_debugger=True,use_reloader=True)
    else:
        app.run(use_debugger=True,use_reloader=True)
elif cmd[1] == 'migrate':
    db.create_all()