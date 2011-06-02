from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Adjunto
from sgp import model
import transaction

class AdjuntoManager():
    def getByName(self, name):
        adjunto = DBSession.query(Adjunto).filter(Adjunto.nombre.like(name)).one()
        return adjunto
    
    def getById(self, id):
        adjunto = DBSession.query(Adjunto).filter(Adjunto.id_adjunto==id).one()
        return adjunto
    
    def add(self, adjunto):
        DBSession.add(adjunto)
        transaction.commit()
    
    def _add(self,idItem, byte, tipo_archivo, nombre):
        a = Adjunto()
        a.nombre = nombre
        a.idItem = idItem
        a.archivo = byte
        a.tipo_archivo=tipo_archivo
        DBSession.add(a)
        transaction.commit()
        
    def update(self,adjunto):
        DBSession.merge(adjunto)
        transaction.commit()
        
    def delete(self,adjunto):
        DBSession.delete(adjunto)
        transaction.commit()
    
    def deleteByid(self, id):
        u = self.getById(id)
        DBSession.delete(u)
        transaction.commit()
        
    def deleteByName(self,name):
        u = self.getByName(name)
        DBSession.delete(u)
        transaction.commit()   