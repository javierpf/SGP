from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Relacion
from sgp import model
import transaction

class ItemManager():
    def getByName(self, name):
        item = DBSession.query(Item).filter(Item.nombre.like(name)).one()
        return item
    def getById(self, id):
        item = DBSession.query(Item).filter(Item.id_item==id).one()
        return item
    def getHijos(self, id_item):
        hijos = DBSession.query(Item).filter(Relacion.id_item1 == id_item and Relacion.tipo_relacion==1).all()
        return hijos
