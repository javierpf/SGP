from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso
from sgp.managers.PermisoMan import PermisoManager
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
        