import eel
from startup import eel_app
from models import request_in, form_request_in
import config

class Request():
    def __init__(self, request: request_in):
        print(f'routing: {request}')
        self.routes = config.routes
        self.request = request
        self.validate()
        # if this route requires authentication
        if self.routes[self.request['args']['target']]['auth_required']:
            self.auth_required = True
            self.authenticate()
        self.process()
        self.log()
        # consider wrapping a js function so the actual execution
        # is triggered from js after initialization
        # this allows the execution to be called from js or python
        # argument can specify these possibilities

    def process(self):
        # how can i wrap this in an await to be triggered by js function?
        # How would i then destroy that request? or do I maybe not want to...?
        # maybe allow people to visit speicifc links?'
        if self.validated:
            if self.auth_required:
                if self.authenticated:
                    self.routes[self.request['args']['target']]['route'](self.request)
            else:
                self.routes[self.request['args']['target']]['route'](self.request)

    def log(self):
        print('logging request in sql server')

    def authenticate(self):
        """
        """
        if 'session_token' in self.request['args']:
            session_token = self.request['args']['session_token']
        else:
            # log user failed a request due to no session token
            # prompt user to log in
            # return action data to client so it can be immediately ran again
            # on login, and also store new tokens
            self.authentication_fail_reason = 'No session token.'
            self.authenticated = False

        if 'user_id' in self.request['args']:
            user_id = self.request['args']['user_id']
        else:
            # log user failed a request due to no user id
            # prompt user to log in
            # return action data to client so it can be immediately ran again
            # on login, and also store new tokens
            self.authentication_fail_reason = 'No user id.'
            self.authenticated = False

        # need to actually hook this function up
        if authenticate(self.request['args']['target'], session_token, user_id):
            self.authenticated = True
        else:
            self.authentication_fail_reason = 'Authentication failed/Session Expired.'
            self.authenticated = False

    def validate(self):
        """
        Validates the request, the request must be defined in routes.py
        Checks that the request contains each arg in the required_args and each value in the required_values
        Required args/values should be strings, their type can be dynamic
        """
        # All request need link arg
        if 'target' in self.request['args']:
            route = self.request['args']['target']
        else:
            self.validation_fail_reason = 'No target.'
            self.validated = False

        # Check for the required arguments
        for req_arg in self.routes[route]['required_args']:
            if not req_arg in self.request['Missing required parameters.']:
                self.validated = False
        
        self.validated = True

def authenticate(target, session_token, user_id):
    permissions = ['/page-one/', '/page-two/', '/auth/login/successful/']
    if target in permissions:
        return True
    else:
        return False

def page_one(request):
    args = {
        'content': 'page one'
    }
    eel_app.write_new_page('index.html', args)

def page_two(request):
    args = {
        'content': 'page two'
    }
    eel_app.write_new_page('index.html', args)

def login_successful(request):
    print(request)
    eel.loginSuccessful('5678', '1')

@eel.expose
def process_request(request):
    Request(request)