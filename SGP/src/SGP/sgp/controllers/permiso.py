from repoze.what import predicates
from sgp.lib.auth import EvaluarPermiso
from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Permiso
from sgp.managers.PermisoMan import PermisoManager

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
#get_one
class PermisoTable(TableBase):
    __model__ = Permiso
    __omit_fields__ = ['id_permiso','permiso_recurso']
    
permiso_table = PermisoTable(DBSession)

class PermisoTableFiller(TableFiller):
    __model__ = Permiso
permiso_table_filler = PermisoTableFiller(DBSession)

class PermisoAddForm(AddRecordForm):
    __model__ = Permiso
    __omit_fields__ = ['genre_id','id_permiso']
    __omit_fields__ = ['permiso_recurso']
    __field_order__        = ['nombre','descripcion','tipo']
permiso_add_form = PermisoAddForm(DBSession)

class PermisoEditForm(EditableForm):
    __model__ = Permiso
    __omit_fields__ = ['id_permiso', 'permiso_recurso']
    
permiso_edit_form = PermisoEditForm(DBSession)

class PermisoEditFiller(EditFormFiller):
    __model__ = Permiso
permiso_edit_filler = PermisoEditFiller(DBSession)
# ################################################################################################       
class BusquedaTableFiller(TableFiller):
    __model__ = Permiso
    buscado=""
    def init(self,buscado):
        self.buscado=buscado

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = PermisoManager()
        permisos = pm.buscar(self.buscado)
        return len(permisos), permisos   

# ################################################################################################       

class PermisoController(CrudRestController):
    model = Permiso
    table = permiso_table
    table_filler = permiso_table_filler
    new_form = permiso_add_form
    edit_form = permiso_edit_form
    edit_filler = permiso_edit_filler
# ################################################################################################       
    @with_trailing_slash
    @expose('sgp.templates.get_all_permiso')
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
# ################################################################################################            
    @with_trailing_slash
    @expose('sgp.templates.get_all_permiso')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw     
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="permiso")

# ################################################################################################       
    @expose()
    def post(self, **kw):
        p = Permiso()
        pm = PermisoManager()
        params = kw
        descripcion = params['descripcion']
        nombre = params['nombre']
        tipo = params['tipo']
        p.nombre = nombre
        p.descripcion = descripcion
        p.tipo = tipo
        pm.add(p)
        raise redirect('./')
# ################################################################################################       
    @expose()
    def put(self, *args, **kw):
        pm=PermisoManager()
        p = pm.getById(args)
        params = kw
        p.nombre = params["nombre"]
        p.descripcion = params["descripcion"]
        p.tipo = params["tipo"]
        pm.update(p)
        raise redirect('../')
# ################################################################################################       
    @expose()
    def post_delete(self, *args, **kw):
        pm = PermisoManager()
        pm.deleteById(args)
        raise redirect('./')