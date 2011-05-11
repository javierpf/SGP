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
class CampoTable(TableBase):
    __model__ = Campo
#    __omit_fields__ = ['id_tipo_item','genre_id']
#    __omit_fields__ = ['id_campo','genre_id_fase']
    __limit_fields__=['nombre','tipo_dato','tipo_item']
#    __field_order__ = [ 'fase','nombre', 'campos']
    
Campo_table = CampoTable(DBSession)

class CampoTableFiller(TableFiller):
    __model__ = Campo
Campo_table_filler = CampoTableFiller(DBSession)

  
class CampoAddForm(AddRecordForm):
    __model__ = Campo
#    __omit_fields__ = ['id_Campo','Campo']
    __limit_fields__=['nombre','tipo_dato']
#    __field_order__ = ['fase','nombre']
    fase=0
    def init(self,fase):
        self.fase=fase
Campo_add_form = CampoAddForm(DBSession)

class CampoEditForm(EditableForm):
    __model__ = Campo
#    __omit_fields__ = ['id_Campo', 'Campo']
#    __field_order__ = ['nombre','descripcion','permisos']   
#    __field_attrs__ = {'descripcion':{'rows':'2'}}

    
Campo_edit_form = CampoEditForm(DBSession)

class CampoEditFiller(EditFormFiller):
    __model__ = Campo
Campo_edit_filler = CampoEditFiller(DBSession)
# ################################################################################################       
class BusquedaTableFiller(TableFiller):
    __model__ = Campo
    buscado=""
    def init(self,buscado):
        self.buscado=buscado

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = CampoManager()
        Campoes = pm.buscar(self.buscado)
        return len(Campoes), Campoes   

# ################################################################################################       

class CampoController(CrudRestController):
    model = Campo
    table = Campo_table
    table_filler = Campo_table_filler
    new_form = Campo_add_form
    edit_form = Campo_edit_form
    edit_filler = Campo_edit_filler
    fase=0
# ################################################################################################
    def init(self,fase):
        self.fase=fase
         
    @with_trailing_slash
    @expose('sgp.templates.get_all_campo')
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
    @expose('sgp.templates.get_all_Campo')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw     
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="Campo")

# ################################################################################################       
    @expose()
    def post(self, **kw):
        rm = CampoManager()
        tm = TipoItemManager()
        params = kw

        fase = session['newCampo']
        tipo = session['tipoItem']

        ti=tm.getByName(tipo)
        rm.addParams(params['nombre'], params['tipo_dato'], ti.id_tipo_item)
       
        raise redirect('/campo/new')
# ################################################################################################
    def returnTipoItemList(self):
        session['newCampo']=''
        session['tipoItem']=''
        raise redirect('/tipoItem')
               
    @without_trailing_slash
    @expose('sgp.templates.newCampo')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        fase = session['newCampo']
        tipo = session['tipoItem']
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__, fase = fase, tipoItem=tipo)


# ################################################################################################       
    @expose()
    def put(self, *args, **kw):
        rm = CampoManager()
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
        pm = CampoManager()
        pm.deleteById(args)
        raise redirect('./')
# ################################################################################################
           
