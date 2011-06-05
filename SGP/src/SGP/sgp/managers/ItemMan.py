from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, Relacion, Atributo, Adjunto,Fase, TipoItem
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
    
    def getByCodigo(self,codigo):
        lista = DBSession.query(Item).filter(Item.codigo == codigo).all()
        return lista
    
    def getAnteriores(self,codigo):
        lista = DBSession.query(Item).filter((Item.codigo == codigo) & (Item.actual== 'false')).all()
        return lista
    
    def buscar_por_fase(self, id_fase):
        lista = DBSession.query(Item).filter((Item.id_fase == id_fase) & (Item.actual == 'true') & (Item.estado != 'eliminado')).all()
        return lista
    
    def buscar(self,buscado,id_fase):
        lista = DBSession.query(Item).filter(Item.identificador.op('~*')(buscado) 
                                             & (Item.id_fase ==id_fase)
                                             & (Item.actual == 'true')
                                             & (Item.estado != 'eliminado')).all()
        return lista
    
    def add(self, item):
        DBSession.add(item)
        transaction.commit()
        
    def update(self,user):
        DBSession.merge(user)
        transaction.commit()
        
    def addAtributo(self,identificador,id_fase,version,id_campo, valor):
        transaction.begin()
        item = self.getByIdentificadorFaseVersion(identificador,id_fase,version)
        atributo = Atributo()
        atributo.id_campo = id_campo
        atributo.valor =valor
        atributo.id_item = item.id_item
        DBSession.add(atributo)
        transaction.commit()
        
    def copiarAdjunto(self, item, adjunto):
        transaction.begin()
        adjunto_copia = Adjunto()
        adjunto_copia.archivo = adjunto.archivo
        adjunto_copia.id_item = item.id_item
        adjunto_copia.nombre = adjunto.nombre
        
        DBSession.add(adjunto_copia)
        transaction.commit
        
    def getByIdentificadorFaseVersion(self,identificador,id_fase,version):
        item = DBSession.query(Item).filter((Item.identificador == identificador) 
                                            & (Item.id_fase == int(id_fase)) 
                                            & (Item.version == version)).one()
        return item
    
    def adjuntarArchivo(self,item,archivo,nombre):
        transaction.begin()
        adjunto = Adjunto()
        adjunto.archivo = archivo
        adjunto.id_item = item.id_item
        adjunto.nombre = nombre
        
        DBSession.add(adjunto)
        transaction.commit()
    def generar_codigo(self, idfase, tipo_item):
        transaction.begin()
        fase = DBSession.query(Fase).filter(Fase.id_fase == idfase).one()
        nro = fase.nro_item + 1
        fase.nro_item = fase.nro_item +1
        DBSession.merge(fase)
        transaction.commit()
        if tipo_item ==-1:
            codigo = "Gen - " + str(nro)
        else:
            tipo = DBSession.query(TipoItem).filter(TipoItem.id_tipo_item == tipo_item).one()   
            codigo = tipo.prefijo + " - " + str(nro) 
        return codigo