from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Fase
from sgp import model
import transaction

class FaseManager():
        
    def getAll(self):
        user = DBSession.query(Fase).all()
        return user
    
    def getByLogin(self, loginName):
        user = DBSession.query(Fase).filter(Fase.id_fase.like(loginName)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(Fase).filter(Fase.id_fase==(idUser)).one();
        return user
    
    def add(self, user):
        DBSession.add(user)
        transaction.commit()
    
    def _add(self,name,tel,login, passw):
        u = Fase()
        u.nombre= name
        u.telefono=tel
        u.Fase = login
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
    def buscar(self, buscado):
        lista = DBSession.query(Fase).filter(Fase.nombre.op('~*')(buscado)).all()
        return lista
    def getListaFases(self, lista_id):
        listaFases = []
        for i in lista_id:
            p = self.getById(i)
            listaFases.append(p)
        return listaFases
        