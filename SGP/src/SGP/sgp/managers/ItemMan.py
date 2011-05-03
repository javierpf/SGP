from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso
from sgp import model

class ItemManager():
    def getItemByName(self, name):
        item = DBSession.query(Item).filter(Item.nombre.like(name)).one()
        return item
    def getItemById(self, id):
        item = DBSession.query(Item).filter(Item.id_item==id).one()
        return item
