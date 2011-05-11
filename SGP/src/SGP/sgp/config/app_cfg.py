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


base_config.use_sqlalchemy=False
base_config.use_transaction_manager=False
base_config.auth_backend=None
base_config.use_toscawidgets=False
base_config.use_toscawidgets = True