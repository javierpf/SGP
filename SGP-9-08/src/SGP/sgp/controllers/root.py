# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from sgp.model import DBSession
from sgp.lib.base import BaseController

from sgp.controllers.error import ErrorController
from sgp.model.auth import *
from sgp.controllers.permiso import PermisoController
from sgp.managers.UsuarioMan import UsuarioManager
from sgp.managers.ItemMan import ItemManager
from sgp.managers.RolMan import RolManager
from sgp.managers.PermisoMan import PermisoManager

__all__ = ['RootController']


class RootController(BaseController):
    error = ErrorController()
    permiso = PermisoController(BaseController)
###############################################################################################################
#Relaciones
    @expose()
    def getHijos(self):
        im=ItemManager()
        hijos = im.getHijos(2)
        return hijos

###############################################################################################################
#ADJUNTO


###############################################################################################################
#PERMISO    
    @expose()
    def permisoById(self):
        pm = PermisoManager()
        p = pm.getById(1)
        return p.nombre
    @expose()
    def permisoByName(self):
        pm = PermisoManager()
        p = pm.getByName("permiso para Crear Proyecto")
        return p.descripcion
    @expose()
    def updatePermiso(self):
        pm = PermisoManager()
        p = pm.getById(12)
        p.descripcion = "Modificado1"
        pm.update(p)
        return "Verificar"
    @expose()
    def deletePermiso(self):
        pm = PermisoManager()
        p = pm.getById(14)
        pm.delete(p)
        return "Verificar no existe permiso con id=14"
    @expose()
    def deletePemisoById(self):
        pm = PermisoManager() 
        pm.deleteById(13)
        return "Verificar no existe permiso con id=13"
    @expose()
    def deletePermisoByName(self):
        pm = PermisoManager()
        p = pm.getById(12)
        pm.deleteByName(p.nombre)
        return "Verif. Crear proyecto no debe existir"
#############################################################################################################
# ROL    
    @expose()
    def updateRol(self):
        rm = RolManager()
        r = rm.getById(2)
        r.nombre = "Mod"
        rm.update(r)
        r = rm.getById(2)
        return r.nombre
    @expose()
    def deleteRol(self):
        rm = RolManager()
        r = rm.getByName("AddParams")
        rm.delete(r)
        return "No debe existir" + r.nombre
    @expose()
    def deleteByid(self):
        rm = RolManager()
        rm.deleteByid(3)
        return "Mirar en PGAdmin! -- No debe existir un rol con id=3"
    @expose()
    def deleteByName(self):
        rm=RolManager()
        rm.deleteByName("AddParams")
        return "Mirar en PGAdmin -- No debe existir un rol llamado AddParams"
    @expose()
    def addRol(self):
        rm = RolManager()
        id_permisos = [1,2,3]
        rm.addParams("AddParams", "Desde addRol", id_permisos)
        rr = rm.getByName("AddParams")
        return rr.nombre     
        
    @expose()
    def rolByName(self):
        rm = RolManager()
        r = rm.getByName("rol1")
        return r.nombre
    @expose()
    def rolById(self):
        rm = RolManager()
        r = rm.getById(2)
        return r.nombre
###############################################################################################################
#USUARIO
    @expose('sgp.templates.index')
    def index(self):
        """Handle the front-page"""
        return dict(page='index')
    @expose()
    def nuevoUsuario(self):
        u = Usuario()
        u.nombre = "Canhete"
        u.telefono="0981 631 303"
        u.usuario = "vanecan2"
        u.password = "12345"
        um = UsuarioManager()
        um.add(u)
        user = um.getUsuarioByLogin("vanecan2")
        return user.usuario
    @expose()
    def modificarUsuario(self):
        um = UsuarioManager()
        u = um.getUsuarioByLogin("vanecan2")
        u.nombre = "update"
        um.update(u)
        u=um.getUsuarioByLogin("vanecan2")
        return u.nombre
    @expose()
    def eByid(self):
        um = UsuarioManager()
        um.deleteByid(8)
    @expose()
    def eByLogin(self):
        um = UsuarioManager()
        um.deleteByLogin("vanecan")
    @expose()
    def delete(self):
        um = UsuarioManager()
        u = um.getByLogin("javier")
        um.delete(u)
        
        
        
    @expose()
    def prueba(self):
        query = DBSession.query(Usuario)
        it = query.filter(Usuario.id_usuario == 1 ).one()
        res = ""
        for r in it.roles :
           for p in r.permisos_recursos:
               res = res + p.permiso.nombre + "   "+str(p.recurso.id_recurso) + "         "
        return res
       # return dict(page='index')
    
    @expose()
    def listaUsuarios(self):
        um = UsuarioManager()
        u = um.getAll()
        res = ""
        for user in u:
            res = res + "\n" + str(user.id_usuario) + " " + user.nombre+" " + user.usuario+ " "+ user.password + "\n"
        return str(res) 
###############################################################################################################
#DEFAULT
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


