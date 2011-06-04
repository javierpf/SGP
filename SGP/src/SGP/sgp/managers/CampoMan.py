from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Campo
from sgp import model
import transaction

class CampoManager():
        
    def getAll(self):
        user = DBSession.query(Campo).all()
        return user
    
    def getByName(self, name):
        print "Campo por nombre"
        user = DBSession.query(Campo).filter(Campo.nombre.like(name)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(Campo).filter(Campo.id_campo==(idUser)).one();
        return user
    
    def add(self, user):
        print ("Agregar el campo" + user.nombre)
        id = DBSession.add(user)
        transaction.commit()
        return id
    
    def addParams(self,name,type, id_tipo):
        print ("Agregar un Campo nuevo al tipo de Item" + str(id_tipo))
        u = Campo()
        u.nombre= name
        u.tipo_dato=type
        u.id_tipo_item=id_tipo
        b = self.verificaExistencia(id_tipo, name)
        if not(b)   :
            self.add(u)
            return True
        return False
    
    def verificaExistencia(self, id_tipo, name):
        c1 = DBSession.query(Campo).filter(Campo.id_tipo_item==id_tipo)
        c2 = DBSession.query(Campo).filter(Campo.nombre.like(name))
        c = c1.intersect(c2)
        if c.count()>0:
            return True
        return False
        
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
        
    def deleteByTipoItem(self,id_tipo):
        list = DBSession.query(Campo).filter(Campo.id_tipo_item==id_tipo).all()
        for i in list:
            self.delete(i)
    def buscar(self, buscado):
        lista = DBSession.query(Campo).filter(Campo.nombre.op('~*')(buscado)).all()
        return lista
    def getListaCampos(self, lista_id):
        listaCampos = []
        for i in lista_id:
            p = self.getById(i)
            listaCampos.append(p)
        return listaCampos
    def getByTipoItem(self, tipo):
        list = DBSession.query(Campo).filter(Campo.id_tipo_item==tipo).all()
        return list
    def actualizar(self, id_campo, nombre, tipo_dato):
        transaction.begin()
        p = self.getById(id_campo)
        p.nombre = nombre
        p.tipo_dato = tipo_dato
        DBSession.merge(p)
        transaction.commit()
        