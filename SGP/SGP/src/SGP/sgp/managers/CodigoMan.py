from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Codigo
from sgp import model
import transaction

class CodigoManager():
    def generar_codigo(self):
        codigo = DBSession.query(Codigo).filter(Codigo.codigo==0).one()
        valor = codigo.valor
        codigo.valor +=1
        DBSession.merge(codigo)
        transaction.commit()
        return valor
    