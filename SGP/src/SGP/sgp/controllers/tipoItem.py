from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Permiso, TipoItem, Campo
from sgp.managers.PermisoMan import PermisoManager
from sgp.managers.TipoItemMan import TipoItemManager
from sgp.managers.FaseMan import FaseManager
from sgp.managers.CampoMan import CampoManager


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


#get_one
class TipoItemTable(TableBase):
    __model__ = TipoItem
    __omit_fields__ = ['id_tipo_item','genre_id']
    __omit_fields__ = ['id_fase','genre_id_fase']
    __limit_fields__=['fase','nombre','campos']
    __field_order__ = [ 'fase','nombre', 'campos']
    
TipoItem_table = TipoItemTable(DBSession)

class TipoItemTableFiller(TableFiller):
    __model__ = TipoItem
TipoItem_table_filler = TipoItemTableFiller(DBSession)

  
class TipoItemAddForm(AddRecordForm):
    __model__ = TipoItem
    __omit_fields__ = ['id_TipoItem','TipoItem']
    __omit_fields__= ['campos', 'TipoItem']
    __field_order__ = ['nombre','campos','fase']
TipoItem_add_form = TipoItemAddForm(DBSession)

class TipoItemEditForm(EditableForm):
    __model__ = TipoItem
#    __omit_fields__ = ['id_TipoItem', 'TipoItem']
#    __field_order__ = ['nombre','descripcion','permisos']   
#    __field_attrs__ = {'descripcion':{'rows':'2'}}

    
TipoItem_edit_form = TipoItemEditForm(DBSession)

class TipoItemEditFiller(EditFormFiller):
    __model__ = TipoItem
TipoItem_edit_filler = TipoItemEditFiller(DBSession)
# ################################################################################################       
class BusquedaTableFiller(TableFiller):
    __model__ = TipoItem
    buscado=""
    def init(self,buscado):
        self.buscado=buscado

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = TipoItemManager()
        TipoItemes = pm.buscar(self.buscado)
        return len(TipoItemes), TipoItemes   

# ################################################################################################       

class TipoItemController(CrudRestController):
    model = TipoItem
    table = TipoItem_table
    table_filler = TipoItem_table_filler
    new_form = TipoItem_add_form
    edit_form = TipoItem_edit_form
    edit_filler = TipoItem_edit_filler
# ################################################################################################       
    @with_trailing_slash
    @expose('sgp.templates.get_all_tipoItem')
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
    @expose('sgp.templates.get_all_TipoItem')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw     
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="TipoItem")

# ################################################################################################       
    @expose()
    def post(self, **kw):
        rm = TipoItemManager()
        params = kw
        rm.addSinCampos(params['nombre'], params['fase'])
        session['fase'] = params['fase']
        session.save()
        session['tipoItem'] = params['nombre']
        session.save()
        raise redirect('/campo/new')

# ################################################################################################       
    @expose()
    def put(self, *args, **kw):
        rm = TipoItemManager()
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
        pm = TipoItemManager()
        pm.deleteById(args)
        raise redirect('./')