from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso
from sgp import model
import transaction


class RolManager():
    def getByName(self,name):
        rol = DBSession.query(Rol).filter(Rol.nombre.like(name)).one()
        return rol

    def getById(self, id):
        query = DBSession.query(Rol)
        rol = query.filter(Rol.id_rol == id).one()
        return rol
    
    def add(self, rol):
        DBSession.add(rol)
        transaction.commit()