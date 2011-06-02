# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in SGP.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""

from tg.configuration import AppConfig

import sgp
from sgp import model
from sgp.lib import app_globals, helpers 

base_config = AppConfig()
base_config.renderers = []

base_config.package = sgp

#Enable json in expose
base_config.renderers.append('json')
#Set the default renderer
base_config.default_renderer = 'genshi'
base_config.renderers.append('genshi')
# if you want raw speed and have installed chameleon.genshi
# you should try to use this renderer instead.
# warning: for the moment chameleon does not handle i18n translations
#base_config.renderers.append('chameleon_genshi')

#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = sgp.model
base_config.DBSession = sgp.model.DBSession

# Configure the authentication backend

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP 
base_config.sa_auth.cookie_secret = "ChangeME" 

base_config.auth_backend = 'sqlalchemy'
base_config.sa_auth.dbsession = model.DBSession
# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class = model.Usuario
# what is the class you want to use to search for groups in the database
base_config.sa_auth.group_class = model.Rol
# what is the class you want to use to search for permissions in the database
base_config.sa_auth.permission_class = model.Permiso


base_config.sa_auth.translations.user_name = 'usuario'
base_config.sa_auth.translations.users = 'usuarios'
base_config.sa_auth.translations.group_name = 'nombre'
base_config.sa_auth.translations.groups = 'roles'
base_config.sa_auth.translations.permission_name = 'nombre'
# override this if you would like to provide a different who plugin for
# managing login and logout of your application
base_config.sa_auth.form_plugin = None

# override this if you are using a different charset for the login form
base_config.sa_auth.charset = 'utf-8'

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url = '/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url = '/post_logout'
