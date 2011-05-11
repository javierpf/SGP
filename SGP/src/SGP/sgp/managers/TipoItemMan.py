from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, TipoItem
from sgp import model
from sgp.managers.CampoMan import CampoManager
from sgp.managers.FaseMan import FaseManager

import transaction

class TipoItemManager():
        
    def getAll(self):
        user = DBSession.query(TipoItem).all()
        return user
    
    def getByName(self, loginName):
        user = DBSession.query(TipoItem).filter(TipoItem.nombre.like(loginName)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(TipoItem).filter(TipoItem.id_tipo_item==(idUser)).one();
        return user
    
    def add(self, user):
        DBSession.add(user)
        transaction.commit()
    
    def _add(self,name,tel,login, passw):
        u = TipoItem()
        u.nombre= name
        u.telefono=tel
        u.TipoItem = login
        u.password=passw
        DBSession.add(u)
        transaction.commit()
    def addParams(self,nombre, id_fase, id_campos):
        r = TipoItem()
        r.nombre = nombre
        r.id_fase = id_fase
        r.fase = FaseManager().getById(id_fase)
        r.campos = self.getListaCampos(id_campos)
        self.add(r)
    def addSinCampos(self,nombre, id_fase):
        r = TipoItem()
        r.nombre = nombre
        r.id_fase = id_fase
        r.fase = FaseManager().getById(id_fase)
        self.add(r)
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
        lista = DBSession.query(TipoItem).filter(TipoItem.nombre.op('~*')(buscado)).all()
        return lista
    def getListaCampos(self, lista_id):
        listaCampos = []
        pm = CampoManager()
        for i in lista_id:
            p = pm.getById(i)
            listaCampos.append(p)
        return listaCampos
        