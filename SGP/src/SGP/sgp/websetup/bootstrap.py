# -*- coding: utf-8 -*-
"""Setup the SGP application"""

import logging
from tg import config
from sgp import model

import transaction


def bootstrap(command, conf, vars):
    """Place any commands to setup sgp here"""

    # <websetup.bootstrap.before.auth

    # <websetup.bootstrap.after.auth>
