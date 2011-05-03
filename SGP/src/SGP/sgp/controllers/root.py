# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from sgp.model import DBSession
from sgp.lib.base import BaseController

from sgp.controllers.error import ErrorController
from sgp.model.auth import *
from sgp.controllers.permiso import PermisoController


__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the SGP application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    error = ErrorController()
    permiso = PermisoController(DBSession)

    @expose('sgp.templates.index')
    def index(self):
#        query = DBSession.query(Usuario)
#        it = query.filter(Usuario.id_usuario == 1 ).one()
#        res = ""
#        for r in it.roles :
#           for p in r.permisos_recursos:
#               res = res + p.permiso.nombre + "   "+str(p.recurso.id_recurso) + "         "
#        return res
       # return dict(page='index')
       return dict(page='index')
    
    
    @expose('sgp.templates.about')
    def about(self):
        """Handle the 'about' page."""
        query = DBSession.query(Usuario)
        rol = query.filter(Usuario.id_usuario == 2).one()
        res = ""
        for r in rol.permisos:
            res = res + r.nombre + "\n"
        #return dict(page='index')
        return res
        #return dict(page='about')

    @expose('sgp.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('sgp.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)


