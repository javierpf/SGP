from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso
from sgp import model
import transaction

class PermisoManager():
    def getAll(self):
        all = DBSession.query(Permiso).all()
        return all
    def getById(self,id):
        permiso = DBSession.query(Permiso).filter(Permiso.id_permiso==(id)).one();
        return permiso
    def getByName(self,name):
        permiso = DBSession.query(Permiso).filter(Permiso.nombre.like(name)).one();
        return permiso
    def getListaPermisos(self, lista_id):
        listaPermisos = []
        for i in lista_id:
            p = self.getById(i)
            listaPermisos.append(p)
        return listaPermisos
    def add(self, permiso):
        DBSession.add(permiso)
        transaction.commit()
        
    def addParams(self, params):
        p = Permiso()
        descripcion = params['descripcion']
        nombre = params['nombre']
        tipo = params['tipo']
        p.nombre = nombre
        p.descripcion = descripcion
        p.tipo = tipo
        self.add(p)
    def update(self,per):
        DBSession.merge(per)
        transaction.commit()
    
    def updateParams(self, id, nombre, tipo, descripcion):
        p = Permiso()
        p.id_permiso=id
        p.nombre=nombre
        p.tipo=tipo
        p.descripcion=descripcion
        self.update(p)
        
    def delete(self,per):
        DBSession.delete(per)
        transaction.commit()
    
    def deleteById(self, id):
        u = self.getById(id)
        DBSession.delete(u)
        transaction.commit()
        
    def deleteByName(self,name):
        u = self.getByName(name)
        DBSession.delete(u)
        transaction.commit()    
    def get_primary_fields(self):
        lista = DBSession.query(Permiso).all()
        l=[]
        for i in lista:
            l.append(i.id_permiso)
        return l 
    def buscar(self, buscado):
        lista = DBSession.query(Permiso).filter(Permiso.nombre.op('~*')(buscado)).all()
        return lista
        