from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Proyecto
from sgp import model
import transaction

class ProyectoManager():
        
    def getAll(self):
        user = DBSession.query(Proyecto).all()
        return user
    
    def getByLogin(self, loginName):
        user = DBSession.query(Proyecto).filter(proyecto.proyecto.like(loginName)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(proyecto).filter(proyecto.id_proyecto==(idUser)).one();
        return user
    
    def add(self, user):
        DBSession.add(user)
        transaction.commit()
        
    def update(self,user):
        DBSession.merge(user)
        transaction.commit()
        
    def delete(self,user):
        DBSession.delete(user)
        transaction.commit()
    
    def deleteById(self, id):
        u = self.getById(id)
        DBSession.delete(u)
        transaction.commit()
        
    def deleteByLogin(self,name):
        u = self.getByLogin(name)
        DBSession.delete(u)
        transaction.commit()   