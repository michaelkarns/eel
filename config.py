
import os
from controllers import BuildController
from views import page_one, page_two, login_successful

# need to set dst_dir
# also need to setup spec file
app_args = {
    'dst_dir': os.path.normpath('C:/Users/mikek/Desktop/Life/Projects/Eel/static'),
    'src_dir': os.path.normpath(BuildController.resource_path('web'))
}

connection_string = ''

routes = {
    '/page-one/': {
        'route': page_one,
        'required_args': [],
        'auth_required': True,
    },
    '/page-two/': {
        'route': page_two,
        'required_args': [],
        'auth_required': True,
    },
    '/auth/login/successful/': {
        'route': login_successful,
        'required_args': [],
        'auth_required': True,
    }
}