from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso
from sgp import model
import transaction

class PermisoManager():
    def getById(self,id):
        permiso = DBSession.query(Permiso).filter(Permiso.id_permiso==(id)).one();
        return permiso
    def getByName(self,name):
        permiso = DBSession.query(Permiso).filter(Permiso.nombre.like(name)).one();
        return permiso
    def getListaPermisos(self, lista_id):
        listaPermisos = []
        for i in lista_id:
            p = getById(i)
            listaPermisos.append(p)
        return listaPermisos
    def add(self, permiso):
        DBSession.add(permiso)
        transaction.commit()
    