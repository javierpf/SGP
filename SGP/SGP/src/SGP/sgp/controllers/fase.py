from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Fase
from sgp.managers.FaseMan import FaseManager
from sgp.managers.ProyectoMan import ProyectoManager
from sgp.managers.CodigoMan import CodigoManager


from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller
from tw.forms import TableForm
from pylons import tmpl_context 

from tg import expose, flash, redirect
from tg.decorators import paginate
from tg.decorators import without_trailing_slash, with_trailing_slash
import pylons
from tg import session
class faselist():
    nombre = None
    id = None
##############################################################################
class FaseTable(TableBase):
    __model__ = Fase
    __omit_fields__ = ['id_fase','id_proyecto','items','proyecto','codigo','tipo_items']    
fase_table = FaseTable(DBSession)
##############################################################################
class FaseTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    def init(self,buscado):
        self.buscado=buscado
        
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Fasees = pm.buscar_por_proyecto(self.buscado)
        return len(Fasees), Fasees   
    
fase_table_filler = FaseTableFiller(DBSession)

############################################################################## 
class FaseAddForm(AddRecordForm):
    __model__ = Fase
    __omit_fields__ = ['id_Fase','proyecto','items','estado','codigo','tipo_items']
fase_add_form = FaseAddForm(DBSession)
##############################################################################
class FaseEditForm(EditableForm):
    __model__ = Fase
    __omit_fields__ = ['id_Fase', 'proyecto','items','estado','codigo','tipo_items','nro_item']
#    __field_order__ = ['nombre','descripcion','permisos']   
#    __field_attrs__ = {'descripcion':{'rows':'2'}}

    
fase_edit_form = FaseEditForm(DBSession)
##############################################################################
class FaseEditFiller(EditFormFiller):
    __model__ = Fase
    __omit_fields__ = ['estado']
fase_edit_filler = FaseEditFiller(DBSession)
##############################################################################
class FasesProyectoTable(TableBase):
    __model__ = Fase
    __omit_fields__ = ['id_fase','id_proyecto','items','proyecto','__actions__']
    __xml_fields__ = ['nombre']
fase_proyecto_table = FasesProyectoTable(DBSession)
# ################################################################################################       
class FasePorProyectoTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    def init(self,buscado):
        self.buscado=buscado
        
    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/item/?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
#        nombre = ('<div>'+'<a href="/item/get_all?id_proyecto='+str(obj.id_proyecto)+'&id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Fasees = pm.buscar_por_proyecto(self.buscado)
        return len(Fasees), Fasees   
####################################################################################################    
class BusquedaTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    def init(self,buscado):
        self.buscado=buscado
        

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Campoes = pm.buscar(self.buscado, session['id_proyecto'])
        return len(Campoes), Campoes  
####################################################################################################    
class BusquedaProyectoTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    def init(self,buscado,id_proyecto):
        self.buscado=buscado
        self.id_proyecto = id_proyecto

    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/item'+'">'+obj.nombre+'</a>'+'</div>')
#        nombre = ('<div>'+'<a href="/item/get_all?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Campoes = pm.buscar(self.buscado, self.id_proyecto)
        return len(Campoes), Campoes  
##############################################################################
class FasesProyectoTableFiller(TableFiller):
    __model__ = Fase

    buscado=""
    def init(self,id_proyecto):
        self.id_proyecto= id_proyecto
    
    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/item/items?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
#        nombre = ('<div>'+'<a href="/item/get_all?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre
        
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        print self.id_proyecto
        pm = FaseManager()
        Fasees = pm.buscar_por_proyecto(self.id_proyecto)
        return len(Fasees), Fasees   

# ####################FASe############################################################################       

class FaseController(CrudRestController):
    model = Fase
    table = fase_table
    table_filler = fase_table_filler
    new_form = fase_add_form
    edit_form = fase_edit_form
    edit_filler = fase_edit_filler
    table_fases = fase_proyecto_table
    
    fase=0
# ################################################################################################
    @with_trailing_slash
    @expose('sgp.templates.get_all_fase')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        """Return all records.
           Pagination is done by offset/limit in the filler method.
           Returns an HTML page with the records if not json.
        """   
        busqueda_filler = FaseTableFiller(DBSession)
        id_proyecto = session['id_proyecto']
        busqueda_filler.init(id_proyecto)
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="Fase", id_proyecto =id_proyecto)
# ################################################################################################            
    @with_trailing_slash
    @expose('sgp.templates.get_all_fase')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw     
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        
        return dict(value_list=value, model="Fase")

# ################################################################################################   
    @with_trailing_slash
    @expose('sgp.templates.proyecto_fases')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar_proyecto_fases(self,*args,**kw):
        params = kw     
        busqueda_filler = BusquedaProyectoTableFiller(DBSession)
        print params['id_proyecto']
        busqueda_filler.init(params['parametro'],params['id_proyecto'])
        
        tmpl_context.widget = self.table_fases
        value = busqueda_filler.get_value()
        
        return dict(value_list=value, model="Fase",id_proyecto = params['id_proyecto'])
    
    @expose()
    def post(self, **kw):
        '''Nuevo'''
        rm = FaseManager()
        cm = CodigoManager()
        params = kw
        '''crear la nueva fase'''
        fase = Fase()
        fase.nombre = params['nombre']
        fase.descripcion = params['descripcion']
        fase.id_proyecto = session['id_proyecto']
        fase.estado = 'inicial'
        fase.nro_item=0
        fase.orden=0
        
        codigo= rm.generarCodigo(session['id_proyecto'])
        print codigo
        
        fase.codigo = codigo
        rm.add(fase)
        raise redirect('./')

# ################################################################################################       
    @expose()
    def put(self, *args, **kw):
        '''editar'''
        rm = FaseManager()
        p = rm.getById(args)
        params = kw
        
        p.descripcion = params['descripcion']
        p.nombre = params['nombre']
        rm.update(p)
        raise redirect('../')
# ################################################################################################       
    @expose()
    def post_delete(self, *args, **kw):
        pm = FaseManager()
        pm.deleteById(args)
        raise redirect('./')
# ################################################################################################
    @with_trailing_slash
    @expose('sgp.templates.proyecto_fases')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def fases_por_proyecto(self, *args, **kw):
        params = kw
        fase_filler = FasesProyectoTableFiller(DBSession)
        id_proyecto = params['id_proyecto']
        session['id_proyecto']=id_proyecto;
        session.save()
        
        session['proyecto']=ProyectoManager().getById(int(id_proyecto)).nombre
        session.save()
        session['conn_tipo'] = 0; session.save()
        proyecto = ProyectoManager().getById(int(id_proyecto))
        if proyecto.estado=="creado":
            raise redirect ('/proyecto/'+params['id_proyecto']+'/edit')
        fase_filler.init(id_proyecto)
        
        tmpl_context.widget = self.table_fases
        value = fase_filler.get_value()
        return dict(value_list=value, model="Fase")
    @expose()
    def terminar(self):
        print"terminar"
        print ("id_proyecto:" + session['id_proyecto'])
        pm=ProyectoManager()
        p = pm.getById(int(session['id_proyecto']))
        p.estado = 'iniciado'
        pm.update(p)
        raise redirect('/fase/fases_por_proyecto?id_proyecto='+session['id_proyecto'])
    
    @expose("sgp.templates.ordenar_fases")
    def ordenar(self):
        proyecto = ProyectoManager().getById(int(session['id_proyecto']))
        cantidad = len(proyecto.fases)
        orden = []
        for i in range(cantidad):
            x = i+1
            orden.append(x)
        fases = []
        for f in proyecto.fases:
            fa = faselist(); fa.nombre =f.nombre; fa.id = f.id_fase 
            fases.append(fa)
        print fases
        print orden
        return dict(orden = orden, fases=fases)
    @expose()
    def s_ordenar(self,*args, **kw):
        params  = kw
        for i in params['posicion']:
            orden, fase = i.split('#')
            FaseManager().ordenarFase(int(orden), int(fase))
        self.terminar()