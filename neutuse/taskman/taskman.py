from flask import Flask
from . import webclient 
from .api import apiv1
from .storage import Sqlite
from .task import Task
from .man import Man


class TaskMan():
    
    def __init__(self, host, port, debug):
        self.host = host
        self.port = port
        self.addr = host if host.startswith('http') else 'http://' + host
        self.addr += ':' + str(port)
        self.debug = debug
        self._initApp()
        
    def _initApp(self):
        self.app = Flask(__name__)
        
        self.app.config['addr'] = self.addr
        self.app.config['model'] = Task
        db = Sqlite('test.db', Task)
        self.app.config['db'] = db
        self.app.config['man'] = Man(db, check_interval=10, waiting_time=5, enable_retry=False)
        
        self.app.register_blueprint(webclient.bp, url_prefix='/client')
        self.app.register_blueprint(apiv1.bp, url_prefix='/api/v1/tasks')
        
        
    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)

