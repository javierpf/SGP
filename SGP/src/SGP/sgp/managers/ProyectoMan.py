from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Proyecto
from sgp.model.auth import Recurso
from sgp import model
import transaction

class ProyectoManager():
        
    def getAll(self):
        user = DBSession.query(Proyecto).all()
        return user
    
    def getByNombre(self, nombre):
        user = DBSession.query(Proyecto).filter(Proyecto.nombre.like(nombre)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(Proyecto).filter(Proyecto.id_proyecto==(idUser)).one();
        return user
    
    def add(self, user):
        DBSession.add(user)
        transaction.commit()
        
        recurso = Recurso()
        recurso.proyecto = user
        recurso.tipo = 1
        id = DBSession.add(recurso)
        transaction.commit()
        return id
        
    def update(self,user):
        DBSession.merge(user)
        transaction.commit()
        
    def delete_recurso(self,user):
        recurso = DBSession.query(Recurso).filter(user.id_proyecto == Recurso.id_proyecto)
        DBSession.delete(recurso)
        transaction.commit()
        
    def delete(self,user):
        DBSession.delete(user)
        transaction.commit()
           
    
    def deleteById(self, id):
        recurso = DBSession.query(Recurso).filter(id == Recurso.id_proyecto).one()
        DBSession.delete(recurso)
        transaction.commit()
        
        u = self.getById(id)
        DBSession.delete(u)
        transaction.commit()
        
    def deleteByLogin(self,name):
        u = self.getByLogin(name)
        DBSession.delete(u)
        transaction.commit()   
        
    def buscar(self, buscado):
        lista = DBSession.query(Proyecto).filter(Proyecto.nombre.op('~*')(buscado)).all()
        return lista