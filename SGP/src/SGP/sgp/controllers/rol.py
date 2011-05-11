from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Permiso, Rol
from sgp.managers.PermisoMan import PermisoManager
from sgp.managers.RolMan import RolManager


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
class RolTable(TableBase):
    __model__ = Rol
    __omit_fields__ = ['id_rol','rol']
    __field_order__ = ['nombre', 'descripcion', 'permisos']
    
rol_table = RolTable(DBSession)

class RolTableFiller(TableFiller):
    __model__ = Rol
rol_table_filler = RolTableFiller(DBSession)

class RolAddForm(AddRecordForm):
    __model__ = Rol
    __omit_fields__ = ['id_rol','rol']
    __field_order__ = ['nombre','descripcion','permisos']
    __field_attrs__ = {'descripcion':{'rows':'2'}}
 

rol_add_form = RolAddForm(DBSession)

class RolEditForm(EditableForm):
    __model__ = Rol
    __omit_fields__ = ['id_rol', 'rol']
    __field_order__ = ['nombre','descripcion','permisos']   
    __field_attrs__ = {'descripcion':{'rows':'2'}}

    
rol_edit_form = RolEditForm(DBSession)

class RolEditFiller(EditFormFiller):
    __model__ = Rol
rol_edit_filler = RolEditFiller(DBSession)
# ################################################################################################       
class BusquedaTableFiller(TableFiller):
    __model__ = Rol
    buscado=""
    def init(self,buscado):
        self.buscado=buscado

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = RolManager()
        roles = pm.buscar(self.buscado)
        return len(roles), roles   

# ################################################################################################       

class RolController(CrudRestController):
    model = Rol
    table = rol_table
    table_filler = rol_table_filler
    new_form = rol_add_form
    edit_form = rol_edit_form
    edit_filler = rol_edit_filler
# ################################################################################################       
    @with_trailing_slash
    @expose('sgp.templates.get_all_rol')
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
    @expose('sgp.templates.get_all_rol')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw     
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="Rol")

# ################################################################################################       
    @expose()
    def post(self, **kw):
        p = Rol()
        rm = RolManager()
        params = kw
        descripcion = params['descripcion']
        nombre = params['nombre']
        per = params['permisos']
        permisos = rm.getListaPermisos(per)
        p.nombre = nombre
        p.descripcion = descripcion
        p.permisos = permisos
        rm.add(p)
        raise redirect('./')
# ################################################################################################       
    @expose()
    def put(self, *args, **kw):
        rm = RolManager()
        p = rm.getById(args)
        params = kw
        descripcion = params['descripcion']
        nombre = params['nombre']
        per = params['permisos']
        permisos = rm.getListaPermisos(per)
        p.nombre = nombre
        p.descripcion = descripcion
        p.permisos = permisos
        rm.update(p)
        raise redirect('../')
# ################################################################################################       
    @expose()
    def post_delete(self, *args, **kw):
        pm = RolManager()
        pm.deleteById(args)
        raise redirect('./')