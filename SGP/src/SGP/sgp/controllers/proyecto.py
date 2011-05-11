from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Proyecto
from sgp.managers.ProyectoMan import ProyectoManager
from tg import expose, flash, redirect
from tg.decorators import without_trailing_slash, with_trailing_slash

from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller

from tg.decorators import paginate
import pylons
from pylons import tmpl_context 

class ProyectoTable(TableBase):
    __model__ = Proyecto
    __omit_fields__ = ['descripcion','id_proyecto','id_administrador','fecha_inicio','fecha_finalizacion','costo_estimado']
    #__dropdown_field_names__ = {'administrador':'nombre'}
    __field_order__        = ['nombre','estado','administrador','fases']
proyecto_table = ProyectoTable(DBSession)

class ProyectoTableFiller(TableFiller):
    __model__ = Proyecto
proyecto_table_filler = ProyectoTableFiller(DBSession)

class ProyectoAddForm(AddRecordForm):
    __model__ = Proyecto
    __omit_fields__ = ['id_Proyecto','estado','fecha_inicio','fecha_finalizacion','costo_estimado','fases', 'id_administrador']
    __dropdown_field_names__ = {'administrador':'nombre'}
    __field_order__ = ['nombre', 'descripcion', 'administrador']
    #__limit_fields__ = ['id_Proyecto','administrador','nombre','descripcion']
proyecto_add_form = ProyectoAddForm(DBSession)

class ProyectoEditForm(EditableForm):
    __model__ = Proyecto
    __omit_fields__ = ['id_Proyecto']
proyecto_edit_form = ProyectoEditForm(DBSession)

class ProyectoEditFiller(EditFormFiller):
    __model__ = Proyecto
proyecto_edit_filler = ProyectoEditFiller(DBSession)

class ProyectoController(CrudRestController):
    model = Proyecto
    table = proyecto_table
    table_filler = proyecto_table_filler
    new_form = proyecto_add_form
    edit_form = proyecto_edit_form
    edit_filler = proyecto_edit_filler
    
    
    @expose()
    def post(self, **kw):
        '''New'''
        p = Proyecto()
        pm = ProyectoManager()
        params = kw
       
        p.descripcion = params['descripcion']
        p.nombre = params['nombre']
        p.estado = 'creado'
        p.id_administrador = params['id_administrador']
        pm.add(p)
        raise redirect('./')
    
    @expose()
    def put(self, *args, **kw):
        '''update'''
        pm=ProyectoManager()
        p = pm.getById(args)
        params = kw
        p.nombre= params['nombre']
        p.descripcion = params ['descripcion']
        p.fecha_inicio = params['fecha_inicio']
        p.fecha_finalizacion = params['fecha_finalizacion']
        p.costo_estimado = params['costo_estimado']
        pm.update(p)
       
        raise redirect('../')    

    
    @expose()
    def post_delete(self, *args, **kw):
        '''delete'''
        pm = ProyectoManager()
        pm.deleteById(args)
        raise redirect('./')
        
    @expose()
    def buscar(self, **kw):
        params = kw
        p = params['parametro']
        return p
    
    @with_trailing_slash
    @expose('sgp.templates.get_all_proyecto')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        """Return all records.
           Pagination is done by offset/limit in the filler method.
           Returns an HTML page with the records if not json.
        """
        if pylons.request.response_type == 'application/json':
            return self.table_filler.get_value(**kw)

        if not getattr(self.table.__class__, '__retrieves_own_value__', False):
            values = self.table_filler.get_value(**kw)
        else:
            values = []
        tmpl_context.widget = self.table
        return dict(model=self.model.__name__, value_list=values)