from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Campo
from sgp import model
import transaction

class CampoManager():
        
    def getAll(self):
        user = DBSession.query(Campo).all()
        return user
    
    def getByLogin(self, loginName):
        user = DBSession.query(Campo).filter(Campo.nombre.like(loginName)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(Campo).filter(Campo.id_campo==(idUser)).one();
        return user
    
    def add(self, user):
        id = DBSession.add(user)
        transaction.commit()
        return id
    
    def addParams(self,name,type, id_tipo):
        u = Campo()
        u.nombre= name
        u.tipo_dato=type
        u.id_tipo_item=id_tipo
        self.add(u)
                      
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
        lista = DBSession.query(Campo).filter(Campo.nombre.op('~*')(buscado)).all()
        return lista
    def getListaCampos(self, lista_id):
        listaCampos = []
        for i in lista_id:
            p = self.getById(i)
            listaCampos.append(p)
        return listaCampos
        