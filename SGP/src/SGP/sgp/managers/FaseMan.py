from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Fase, Recurso, Proyecto
from sgp import model
from sgp.managers.ProyectoMan import ProyectoManager
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
        
        recurso = Recurso()
        recurso.fase = user
        recurso.tipo = 2
        DBSession.add(recurso)
        transaction.commit()
        
    def update(self,user):
        DBSession.merge(user)
        transaction.commit()
        
    def delete(self,user):
        recurso = DBSession.query(Recurso).filter(user.id_fase == Recurso.id_fase)
        DBSession.delete(recurso)
        transaction.commit()
        
        DBSession.delete(user)
        transaction.commit()
        
    
    def deleteById(self, id):
        recurso = DBSession.query(Recurso).filter(id == Recurso.id_fase).one()
        DBSession.delete(recurso)
        transaction.commit()
        
        u = self.getById(id)
        DBSession.delete(u)
        transaction.commit()
        
    def deleteByLogin(self,name):
        u = self.getByLogin(name)
        DBSession.delete(u)
        transaction.commit()
    def buscar(self, buscado, id_proyecto):        
        lista = DBSession.query(Fase).filter(Fase.nombre.op('~*')(buscado) & (Fase.id_proyecto ==id_proyecto )).all()
        return lista
    def cantidad(self, id_proyecto):
        if len(ProyectoManager().getById(id_proyecto).fases)>2:
            return True;
        else:
            return False;
    def getListaFases(self, lista_id):
        listaFases = []
        for i in lista_id:
            p = self.getById(i)
            listaFases.append(p)
        return listaFases
    
    def buscar_por_proyecto(self, buscado):
        lista = DBSession.query(Fase).filter(Fase.id_proyecto == buscado).all()
        return lista
    def generarCodigo(self, id_proyecto):
        transaction.begin()
        idp=int(id_proyecto)
        p = DBSession.query(Proyecto).filter(Proyecto.id_proyecto==idp).one()
        nro = p.nro_fase+1
        p.nro_fase = nro
        DBSession.merge(p)
        transaction.commit()
        return nro
    def ordenarFase(self, orden, fase):
        transaction.begin()
        f = self.getById(fase)
        f.orden = orden
        DBSession.merge(f)
        transaction.commit()