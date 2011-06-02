from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Item,Fase,Atributo,CampoValor
from sgp.managers.ItemMan import ItemManager
from sgp.managers.FaseMan import FaseManager
from sgp.managers.TipoItemMan import TipoItemManager
from sgp.managers.CodigoMan import CodigoManager
from sgp.managers.CampoMan import CampoManager
from sgp.controllers.itemRevertir import ItemRevertirController
from tg import expose, flash, redirect
from tg.decorators import without_trailing_slash, with_trailing_slash

from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller
#from tw.forms.fields import FileField
from tw.forms.fields import InputField

from tg.decorators import paginate
import pylons
from pylons import tmpl_context 
from tg import session
from tg import session
import os
##############################################################################
class ItemTable(TableBase):
    __model__ = Item
    __omit_fields__ = ['id_item','observacion','complejidad','id_fase','id_linea_base','id_tipo_item','descripcion','adjuntos','atributos',]
   
item_table = ItemTable(DBSession)
##############################################################################
class ItemTableFiller(TableFiller):
    __model__ = Item
    
    buscado=""
    def init(self,id_fase):
        self.id_fase=id_fase
       
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = ItemManager()
        Campoes = pm.buscar_por_fase(self.id_fase)
        return len(Campoes), Campoes  

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        estado = obj.estado
        lista = []
        lista.append(str(obj.id_fase))
        lista.append(str(obj.id_item))
        if estado != 'finalizado':
            value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                  '</div><div>'\
                  '<form method="POST" action="'+pklist+'" class="button-to">'\
                '<input type="hidden" name="_method" value="DELETE" />'\
                '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
            '</form>'\
            '<div><a href="/item/impacto?id_item='+pklist+'" style="text-decoration:none">Impacto &nbsp;  </a>'\
            '</div>'
            if estado == "inicial":
                value += '<div><a href="/item/listo?id_item='+str(obj.id_item)+'" style="text-decoration:none">Listo &nbsp;  </a>'\
                        '</div>'
            if estado == 'listo':
                value += '<div><a href="/item/aprobar?id_item='+str(obj.id_item)+'" style="text-decoration:none">Aprobar &nbsp; </a>'\
                        '</div>'\
                        '<div><a href="/item/desaprobar?id_item='+str(obj.id_item)+'" style="text-decoration:none">Desaprobar &nbsp; </a>'\
                        '</div>'
               
            im = ItemManager()
            versiones = im.getByCodigo(obj.codigo)
            cantidad = 0
            for version in versiones:
                cantidad = cantidad +1
            print "cantidad", cantidad
            if cantidad > 1 and obj.estado != "finalizado":
                value += '<div><a href="/itemRevertir/obtener?id_item='+str(obj.id_item)+'" style="text-decoration:none">Revertir &nbsp;</a>'\
                        '</div>'

        else:
            value = '<div><div>'\
                  '</div><div>'\
                  '<form>'\
                  '</form>'
        value +='</div></div>'
        return value
item_table_filler = ItemTableFiller(DBSession)
##############################################################################
class ItemAddForm(AddRecordForm):
    __model__ = Item
    __omit_fields__ = ['id_item','id_fase','codigo','estado','tipo','id_linea_base','version','fase','linea_base','atributos']
  
    
item_add_form = ItemAddForm(DBSession)

##############################################################################
class BusquedaTableFiller(TableFiller):
    __model__ = Item
    buscado=""
    def init(self,buscado, id_fase):
        self.buscado=buscado
        self.id_fase = id_fase
    
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = ItemManager()
        Items = pm.buscar(self.buscado,self.id_fase)
        return len(Items), Items   
    
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        estado = obj.estado
        lista = []
        lista.append(str(obj.id_fase))
        lista.append(str(obj.id_item))
        if estado != 'finalizado':
            value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                  '</div><div>'\
                  '<form method="POST" action="'+pklist+'" class="button-to">'\
                '<input type="hidden" name="_method" value="DELETE" />'\
                '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
            '</form>'\
            '<div><a href="/item/impacto?id_item='+pklist+'" style="text-decoration:none">   Impacto &nbsp;</a>'\
            '</div>'
            if estado == "inicial":
                value += '<div><a href="/item/listo?id_item='+str(obj.id_item)+'" style="text-decoration:none">   Listo &nbsp;</a>'\
                        '</div>'
            if estado == 'listo':
                value += '<div><a href="/item/aprobar?id_item='+str(obj.id_item)+'" style="text-decoration:none">   Aprobar &nbsp;</a>'\
                        '</div>'\
                        '<div><a href="/item/desaprobar?id_item='+str(obj.id_item)+'" style="text-decoration:none">   Desaprobar &nbsp;</a>'\
                        '</div>'
               
            im = ItemManager()
            versiones = im.getByCodigo(obj.codigo)
            cantidad = 0
            for version in versiones:
                cantidad = cantidad +1
            print "cantidad", cantidad
            if cantidad > 1 and obj.estado != "finalizado":
                value += '<div><a href="/itemRevertir/obtener?id_item='+str(obj.id_item)+'" style="text-decoration:none">Revertir</a>'\
                        '</div>'

        else:
            value = '<div><div>'\
                  '</div><div>'\
                  '<form>'\
                  '</form>'
        value +='</div></div>'
        return value
        
##############################################################################

class ItemController(CrudRestController):
    model = Item
    table = item_table
    table_filler = item_table_filler
    new_form = item_add_form
    itemRevertir = ItemRevertirController(DBSession)
#******************************************************************************************    
    @expose()
    def post(self,*args, **kw):
        '''New'''
        p = Item()
        pm = ItemManager()
        cm = CodigoManager()
        params = kw
        
        p.identificador = params['identificador']
        p.observacion = params['observacion']
        p.estado = 'inicial'
        p.complejidad = params['complejidad']
        p.descripcion = params['descripcion']
        p.id_fase = int(session['id_fase'])
        p.codigo = cm.generar_codigo()
        p.version = 1
        p.actual = 'true'
        
        
        if params['tipo_items'] != '-1':
            ti = TipoItemManager()
            tipo= ti.getById(params['tipo_items'])
            p.tipo = tipo
            
        pm.add(p)

        if params['tipo_items'] != '-1':
            ti = TipoItemManager()
            tipo= ti.getById(params['tipo_items'])
            campos = tipo.campos
            for campo in campos:   
                nombre_campo = campo.nombre
                valor = params[nombre_campo]   
                pm.addAtributo(params['identificador'],params['id_fase'],1,campo.id_campo,valor)  
                
                  
        item = pm.getByIdentificadorFaseVersion(params['identificador'],params['id_fase'],1)        
        '''Adjuntar nuevos Archivos'''
        if params['submit'] == 'Adjuntar':
            '''Hay que adjuntar archivos''' 
            id_item = item.id_item
            raise redirect('/item/adjuntar?id_item='+ str(id_item))            
      
        raise redirect('/item/items?id_fase='+ params['id_fase'])
#******************************************************************************************    
    @expose()
    def put(self, *args, **kw):
        '''update'''
        
        params = kw
#        print params['submit']
        pm=ItemManager()
        item_viejo = pm.getById(int(args[0]))
        item_nuevo = Item()
        
        identificador = params['identificador']
        item_nuevo.identificador = identificador
        item_nuevo.observacion = params['observacion']
        item_nuevo.estado = item_viejo.estado
        item_nuevo.complejidad = params['complejidad']
        item_nuevo.descripcion = params['descripcion']
        item_nuevo.id_fase = item_viejo.id_fase
        
        id_fase = item_viejo.id_fase
        item_nuevo.codigo = item_viejo.codigo
        item_nuevo.version = item_viejo.version + 1
        item_nuevo.actual = 'true'
        item_viejo.actual = 'false'
        item_nuevo.tipo = item_viejo.tipo
        tipo_item = item_viejo.id_tipo_item
        
        version = item_nuevo.version
        pm.add(item_nuevo)
        pm.update(item_viejo)
        
        '''Copiar los campos'''
        if tipo_item :
            ti = TipoItemManager()
            tipo= ti.getById(tipo_item)
            campos = tipo.campos
            for campo in campos:
                nombre_campo = campo.nombre
                valor = params[nombre_campo]   
                pm.addAtributo(identificador,id_fase,version,campo.id_campo,valor)  
                
        item = pm.getByIdentificadorFaseVersion(identificador,id_fase,version) #Item_nuevo
        
        item_viejo = pm.getById(int(args[0]))
        '''Copiar los adjuntos'''
        if item_viejo.adjuntos :
            for adjunto in item_viejo.adjuntos:
                pm.copiarAdjunto(item,adjunto)
                
        pm.update(item)
        pm.update(item_viejo)    
        
        item = pm.getByIdentificadorFaseVersion(identificador,id_fase,version) #Item_nuevo
        '''Adjuntar nuevos Archivos'''
        if params['submit'] == 'Adjuntar':
            '''Hay que adjuntar archivos''' 
            id_item = item.id_item
            raise redirect('/item/adjuntar?id_item='+ str(id_item))
        
        raise redirect('/item/items?id_fase='+ str(id_fase))
   
#****************************************************************************************** 
    @expose('sgp.templates.adjuntar')
    def adjuntar(self,*args,**kw):
        im = ItemManager()
        item = im.getById(kw['id_item'])
        return dict(page='index', id_item = kw['id_item'], id_fase= item.id_fase)
#****************************************************************************************** 
    @expose()
    def adjuntar_archivo(self,*args,**kw):
        fileitem = kw['datafile']
        if fileitem.filename:
            os.path.basename(fileitem.filename.replace("\\", "/" ))
            f = fileitem.file.read()
            im = ItemManager()
            item = im.getById(kw['id_item'])
            im.adjuntarArchivo(item,f,fileitem.filename)
        else:
            print 'No file was uploaded'
        raise redirect('/item/adjuntar?id_item='+ kw['id_item'])

#******************************************************************************************        
    @expose()
    def post_delete(self, *args, **kw):
        '''delete'''
        pm = ItemManager()
        item = pm.getById(args)
        if item.estado != 'finalizado':
            item.estado = 'eliminado'
            item.actual = 'false'
            
        id_fase = item.id_fase
        pm.update(item)
        raise redirect('/item/items?id_fase='+ str(id_fase))
#****************************************************************************************** 
    @without_trailing_slash
    @expose('sgp.templates.newitem')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        params = kw
        
        id_tipoItem = params['tipo_items']
        if str(id_tipoItem) == '-1':
            
            return dict(value=kw, model=self.model.__name__, campos=[],id_fase=params['id_fase'],tipo_items=id_tipoItem)
        else:
            fm = TipoItemManager()
            tipo = fm.getById(id_tipoItem)
            campos = tipo.campos
            return dict(value=kw, model=self.model.__name__,campos = campos,id_fase=params['id_fase'],tipo_items=id_tipoItem)
#****************************************************************************************** 
    @with_trailing_slash
    @expose('sgp.templates.get_all_item')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"],kw['id_fase'])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        fm = FaseManager()
        fase = fm.getById(params['id_fase'])
        return dict(value_list=value, model="Item", tipo_items=fase.tipo_items, id_fase=kw['id_fase'])
    
#******************************************************************************************   
    @with_trailing_slash
    @expose('sgp.templates.get_all_item')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def items(self, *args, **kw):
        params = kw
        busqueda_filler = ItemTableFiller(DBSession)
        busqueda_filler.init(params["id_fase"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        
        #obtener tipos de items de la fase
        fm = FaseManager()
        fase = fm.getById(params['id_fase'])
        session['id_fase']=fase.id_fase; session.save()
        session['fase']=fase.nombre; session.save()
        return dict(value_list=value, model="Item",tipo_items=fase.tipo_items,id_fase=params['id_fase'])
#******************************************************************************************   
#******************************************************************************************   
    
    @expose('sgp.templates.edit_item')
    def edit(self, *args, **kw):
        """Display a page to edit the record."""
        
        im = ItemManager()
        cm = CampoManager()       
        item = im.getById(args)
        atributos = item.atributos
        lista = []
        if str(item.id_tipo_item) != '':
            for atributo in atributos:
                campo = cm.getById(atributo.id_campo)
                campoValor = CampoValor()
                campoValor.valor = atributo.valor
                campoValor.campo = campo.nombre
                campoValor.tipo = campo.tipo_dato
                lista.append(campoValor)
        return dict(item=item, campos = lista, id_fase= item.id_fase)
#        return dict(value=value, model=self.model.__name__, pk_count=len(pks),item=item)
#******************************************************************************************       
    @expose()
    def aprobar(self,*args,**kw):
        id_item = kw["id_item"]
        id_item = int(id_item)
        im = ItemManager()
        item_aprobar = im.getById(int(id_item))
        fase_retorno = item_aprobar.id_fase
        item_aprobar.estado = 'aprobado'
        im.update(item_aprobar)
        raise redirect('/item/items?id_fase='+ str(fase_retorno))
#******************************************************************************************   
    @expose()
    def desaprobar(self,**kw):
        id_item = kw["id_item"]
        id_item = int(id_item)
        im = ItemManager()
        item_aprobar = im.getById(int(id_item))
        fase_retorno = item_aprobar.id_fase
        item_aprobar.estado = 'desaprobado'
        im.update(item_aprobar)
        raise redirect('/item/items?id_fase='+ str(fase_retorno))    

#******************************************************************************************   
    @expose()
    def listo(self,**kw):
        id_item = kw["id_item"]
        id_item = int(id_item)
        im = ItemManager()
        item_listo = im.getById(int(id_item))
        fase_retorno = item_listo.id_fase
        item_listo.estado = 'listo'
        im.update(item_listo)
        raise redirect('/item/items?id_fase='+ str(fase_retorno))   