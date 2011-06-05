from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Relacion, Atributo, Adjunto,Fase, TipoItem
from sgp import model
import transaction

class RelacionManager():
    def getById(self, id):
        Relacion = DBSession.query(Relacion).filter(Relacion.id_Relacion==id).one()
        return Relacion
    
    def getItemsByFase(self, id_fase):
        lista = DBSession.query(Relacion).filter((Relacion.id_fase1 == id_fase) & (Relacion.actual == 'true') & (Relacion.estado != 'eliminado')).all()
        return lista
    
    def buscar(self,buscado,id_fase):
        lista = DBSession.query(Relacion).filter(Relacion.identificador.op('~*')(buscado) 
                                             & (Relacion.id_fase ==id_fase)
                                             & (Relacion.actual == 'true')
                                             & (Relacion.estado != 'eliminado')).all()
        return lista
    
    def add(self, Relacion):
        DBSession.add(Relacion)
        transaction.commit()
        
    def update(self,user):
        DBSession.merge(user)
        transaction.commit()