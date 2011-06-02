# -*- coding: utf-8 -*-
"""Main Controller"""
from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates
from sgp.lib.auth import EvaluarPermiso

from sgp.lib.base import BaseController
from sgp.model import DBSession, metadata
from sgp import model
from sgp.model.auth import menu_class
from sgp.managers.UsuarioMan import UsuarioManager
from sgp.managers.RolMan import RolManager
from sgp.controllers.secure import SecureController
from sgp.controllers.error import ErrorController
from sgp.controllers.permiso import PermisoController
from sgp.controllers.permiso import PermisoController
from sgp.controllers.usuario import UsuarioController
from sgp.controllers.proyecto import ProyectoController
from sgp.controllers.rol import RolController
from sgp.controllers.tipoItem import TipoItemController
from sgp.controllers.campo import CampoController
from sgp.controllers.item import ItemController
from sgp.controllers.fase import FaseController
from sgp.controllers.itemRevertir import ItemRevertirController
from tg import session
__all__ = ['RootController']

class ProyectList():
    id_proyecto = None
    nombre = None

class RootController(BaseController):
    error = ErrorController()
    permiso = PermisoController(BaseController)
    usuario = UsuarioController(DBSession)
    proyecto = ProyectoController(DBSession)
    rol = RolController(DBSession)
    tipoItem=TipoItemController(DBSession)
    fase=FaseController(DBSession)
    item=ItemController(DBSession)
    itemRevertir = ItemRevertirController(DBSession)
    m=None
    def menu (self,id_user):
        if request.identity:
            m =(UsuarioManager().getMenu(id_user))
            session['menu'] = m
            session.save()
        return m

    @expose('sgp.templates.index')
    def index(self):
        try:
            if session['menu'] != []:
                pass
        except:
            session['menu']=[]
            session.save()
        return dict(page='index')
    @expose('sgp.templates.pagina_principal')
    def principal(self):
        session['admin_sistema']=False
        um = UsuarioManager()
        usuario= um.getByLogin(request.identity['repoze.who.userid'])
        roles = RolManager().getRoles(usuario)
        proyectos, sistema = um.getProyecto(usuario.id_usuario)
        l = []
        for i in proyectos:
            p = ProyectList()
            p.nombre = i.nombre
            p.id_proyecto = i.id_proyecto
            l.append(p)
        print l
        session['admin_tipo']="ambos"; session.save()
        session['sistema']=True; session.save()
        return dict(id_usuario = usuario.id_usuario, usuario = usuario.nombre, proyectos = l, roles = roles, hola=True)
    @expose('sgp.templates.Sistema')
    def sistema(self):
        session['admin_sistema']=True; session.save()
        session['id_proyecto']=-1; session.save()
        return dict(page="sistema")
    @expose('sgp.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('sgp.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('sgp.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('sgp.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('sgp.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('sgp.templates.index')
    #@require(predicates.is_user('editor', msg=l_('Only for the editor')))
    @require(EvaluarPermiso(1 ,id_fase = 2))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('sgp.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, menu=None)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        self.menu(UsuarioManager().getByLogin(userid).id_usuario)
        redirect('/principal')

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        session.delete()
        flash(_('We hope to see you soon!'))
        redirect('/index')
