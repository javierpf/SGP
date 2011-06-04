from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Item,Fase,Atributo
from sgp.managers.ItemMan import ItemManager
from sgp.managers.FaseMan import FaseManager
from sgp.managers.TipoItemMan import TipoItemManager
from sgp.managers.CodigoMan import CodigoManager
from tg import expose, flash, redirect
from tg.decorators import without_trailing_slash, with_trailing_slash
import transaction

from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller

from tg.decorators import paginate
import pylons
from pylons import tmpl_context 
from tg import session



class ItemTable(TableBase):
    __model__ = Item
    __omit_fields__ = ['id_item','observacion','complejidad','id_fase','id_linea_base','id_tipo_item','descripcion','adjuntos','atributos',]
    __xml_fields__ = ['nombre']
   
item_table = ItemTable(DBSession)
##############################################################################
class ItemTableFiller(TableFiller):
    __model__ = Item
    
    buscado=""
    def init(self,id_item):
        self.id_item=id_item


    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        im = ItemManager()
        item = im.getById(self.id_item)
        Campoes = im.getAnteriores(item.codigo)
        return len(Campoes), Campoes  

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        estado = obj.estado
        if estado != 'finalizado':
            #value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            #      '</div><div>'\
            value = '<div><a href="/itemRevertir/revertir?id_item='+str(obj.id_item)+'" style="text-decoration:none">Revertir</a>'\
            '</div>'



        else:
            value = '<div><div>'\
                  '</div><div>'\
                  '<form>'\
                  '</form>'\
                  '</div></div>'
        return value
        
item_table_filler = ItemTableFiller(DBSession)
class ItemRevertirController(CrudRestController):
    model = Item
    table = item_table
    table_filler = item_table_filler
#******************************************************************************************    
    @with_trailing_slash
    #@expose('sgp.templates.get_all_item')
    @expose('sgp.templates.item_revertir')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def obtener(self, *args, **kw):
        params = kw
        busqueda_filler = ItemTableFiller(DBSession)
        busqueda_filler.init(params["id_item"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="Item", id_item_revertir = params['id_item'])
    
#******************************************************************************************    
    @expose()
    def revertir(self,*args,**kw):
        id_item = kw["id_item"]
        id_item = int(id_item)
        im = ItemManager()
        transaction.begin()
        item_revertir = im.getById(id_item)
        item_nuevo = Item()
        item_nuevo.codigo = item_revertir.codigo
        item_nuevo.identificador = item_revertir.identificador
        item_nuevo.observacion = item_revertir.observacion
        item_nuevo.estado = "inicial"
        item_nuevo.complejidad = item_revertir.complejidad
        item_nuevo.id_fase = item_revertir.id_fase
        item_nuevo.id_tipo_item = item_revertir.id_tipo_item
        item_nuevo.descripcion = item_revertir.descripcion
        items_de_fase = im.buscar_por_fase(item_revertir.id_fase)
        id_fase = item_revertir.id_fase
        version = 0
        for item in items_de_fase:
            if item.version > version:
                version = item.version
            if item.codigo == item_revertir.codigo and item.actual == "true": 
                item.actual = "false"
        version = version + 1
        item_nuevo.version = version
        item_nuevo.actual = 'true'
        print "version",version
        im.add(item_nuevo)
        transaction.commit()
        
        item_viejo = im.getById(id_item)
        identificador = item_viejo.identificador
        
        tipo_item = item_viejo.id_tipo_item
        if tipo_item :
            for atributo in item_viejo.atributos:
                id_campo = atributo.id_campo
                valor = atributo.valor
                im.addAtributo(identificador,id_fase,version,id_campo,valor)  
        im.update(item_viejo)
        
        item_viejo = im.getById(id_item)
        item = im.getByIdentificadorFaseVersion(identificador,id_fase,version) #Item_nuevo
        
        '''Copiar los adjuntos'''
        if item_viejo.adjuntos :
            for adjunto in item_viejo.adjuntos:
                im.copiarAdjunto(item,adjunto)
        im.update(item)
        
        
        raise redirect('/item/items?id_fase='+ str(id_fase))
        
        