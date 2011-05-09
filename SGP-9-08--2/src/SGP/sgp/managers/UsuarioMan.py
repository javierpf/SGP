from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso
from sgp import model
import transaction

class UsuarioManager():
        
    def getAll(self):
        user = DBSession.query(Usuario).all()
        return user
    
    def getByLogin(self, loginName):
        user = DBSession.query(Usuario).filter(Usuario.usuario.like(loginName)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(Usuario).filter(Usuario.id_usuario==(idUser)).one();
        return user
    
    def add(self, user):
        DBSession.add(user)
        transaction.commit()
    
    def _add(self,name,tel,login, passw):
        u = Usuario()
        u.nombre= name
        u.telefono=tel
        u.usuario = login
        u.password=passw
        DBSession.add(u)
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