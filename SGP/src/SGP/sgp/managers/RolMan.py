from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, RolUsuario, PermisoRecurso, rec
from sgp.managers.PermisoMan import PermisoManager
from sgp.managers.ProyectoMan import ProyectoManager
from sgp.managers.UsuarioMan import UsuarioManager

from sgp import model
import transaction


class RolManager():
    def getByName(self,name):
        rol = DBSession.query(Rol).filter(Rol.nombre.like(name)).one()
        return rol

    def getById(self, id):
        query = DBSession.query(Rol)
        rol = query.filter(Rol.id_rol == id).one()
        return rol
    
    def add(self, rol):
        DBSession.add(rol)
        transaction.commit()
    def addParams(self,nombre, descripcion, id_permisos):
        r = Rol()
        r.nombre = nombre
        r.descripcion = descripcion
        pm = PermisoManager()
        permisos = pm.getListaPermisos(id_permisos)
        for p in permisos:
            r.permisos.append(p)
        self.add(r)
    def update(self,rol):
        DBSession.merge(rol)
        transaction.commit()
        
    def delete(self,rol):
        DBSession.delete(rol)
        transaction.commit()
    
    def deleteById(self, id):
        u = self.getById(id)
        DBSession.delete(u)
        transaction.commit()
        
    def deleteByName(self,name):
        u = self.getByName(name)
        DBSession.delete(u)
        transaction.commit()
    def buscar(self, buscado):
        lista = DBSession.query(Rol).filter(Rol.nombre.op('~*')(buscado)).all()
        return lista
    def getListaPermisos(self, lista_id):
        listaPermisos = []
        pm = PermisoManager()
        for i in lista_id:
            p = pm.getById(i)
            listaPermisos.append(p)
        return listaPermisos
   
    #-------------------------------------------------------------------------------------------------------
    #                                ASIGNACION DE ROL de PROYECTO
    #-------------------------------------------------------------------------------------------------------
    def getPermisosByTipo(self, tipo):
        if tipo==0:
            lista = DBSession.query(Permiso).filter(Permiso.tipo == tipo).all()
        else:
            lista = DBSession.query(Permiso).filter(Permiso.tipo >= tipo).all()
        return lista
    def getRolUsuarioId(self, id_rol, id_user):
        id = DBSession.query(RolUsuario).filter((RolUsuario.id_rol == id_rol) & (RolUsuario.id_usuario==id_user)).one()
        return id.id_rol_usuario
    def addRolUsuario(self, id_user, id_rol, id_proyecto):
        transaction.begin()
        ru = RolUsuario()
        id = ru.insert(id_rol, id_user, id_proyecto)
        transaction.commit()       
    def getByRolUsuarioProyecto(self, id_rol, id_usuario, id_proyecto):
        ru = DBSession.query(RolUsuario).filter((RolUsuario.id_rol == id_rol)&(RolUsuario.id_usuario==id_usuario) & (RolUsuario.id_proyecto==id_proyecto)).one()
        print ("Encontrado: "+str(ru.id_proyecto))
        return ru
    def addPermisoRecursoRolUsuario(self, permisos_recursos, usuarios, id_rol, id_proyecto):
        for user in usuarios:
            self.addRolUsuario(int(user), int(id_rol), int(id_proyecto))
            for pr in permisos_recursos:
                p = pr.split("#")
                id_permiso = int(p[0])
                id_recurso = int(p[1])
                self.addPR(id_permiso, id_recurso,id_rol, int(user), int(id_proyecto))
    def addPR (self, id_per, id_rec,id_rol, id_user, id_proyecto):
        transaction.begin()
        ru = self.getByRolUsuarioProyecto(id_rol, id_user, id_proyecto)

        print (str(ru.id_rol_usuario) + "   " + str(id_per) + "    "+ str(id_rec))
        pr = PermisoRecurso()
        pr.id_permiso = id_per
        pr.id_recurso = id_rec
        ru.permisos_recursos.append(pr)
        DBSession.merge(ru)
        transaction.commit()
    #-------------------------------------------------------------------------------------------------------
    #                                ASIGNACION DE ROL SISTEMA
    #-------------------------------------------------------------------------------------------------------
    def addRolSistemaUsuario(self, rol, usuarios):
        for user in usuarios:
            u = int(user)
            r = int(rol)
            transaction.begin()
            ru =RolUsuario()
            ru.insert(r,u,-1)
            transaction.commit()
    #-------------------------------------------------------------------------------------------------------
    #                                DESASIGNACOIN
    #-------------------------------------------------------------------------------------------------------
    def desasignar(self, id_rol, usuarios, id_proyecto):
        for u in usuarios:
            self.quitarRol(int(id_rol), int(u), int(id_proyecto))
    def quitarRol (self, id_rol, id_user, id_proyecto):
        print ("Quitar Rol -> id_rol: " + str(id_rol) + "id_usuario: " + str(id_user) + " id_proyecto: "+str(id_proyecto))
        r = self.getByRolUsuarioProyecto(id_rol, id_user, id_proyecto)
        for i in r.permisos_recursos:
            transaction.begin()
            DBSession.delete(i)
            transaction.commit()
        transaction.begin()
        DBSession.delete(r)
        transaction.commit()
    def getRoles(self, u):
        l = []
        for i in u.roles:
            r = RolManager().getById(i.id_rol)
            rol = rec()
            rol.nombre = r.nombre
            rol.id = r.id_rol
            l.append(rol)
        return l
    def rolesByTipo(self,tipo):
        roles = DBSession.query(Rol).filter(Rol.tipo==tipo).all()
        return roles