from repoze.what import predicates
from sgp.lib.auth import EvaluarPermiso
from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Permiso, TipoItem, Campo
from sgp.managers.PermisoMan import PermisoManager
from sgp.managers.TipoItemMan import TipoItemManager
from sgp.managers.FaseMan import FaseManager
from sgp.managers.CampoMan import CampoManager
from tg import expose, flash, require, url, request, redirect

from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller
from tw.forms import TableForm
from pylons import tmpl_context 

from tg import expose, flash, require, url, request, redirect
from tg.decorators import paginate
from tg.decorators import without_trailing_slash, with_trailing_slash
import pylons
from tg import session
from sgp.controllers.campo import CampoController


#get_one
class TipoItemTable(TableBase):
    __model__ = TipoItem
    __omit_fields__ = ['id_tipo_item','genre_id']
    __omit_fields__ = ['id_fase','genre_id_fase']
    __omit_fields__ = ['campos', 'muchos']
    __limit_fields__=['fase','nombre']
    __field_order__ = ['nombre', 'fase']
    __xml_fields__ = ['nombre']
TipoItem_table = TipoItemTable(DBSession)

class TipoItemTableFiller(TableFiller):
    __model__ = TipoItem
    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/tipoItem/'+str(obj.id_tipo_item)+'/campos">'+obj.nombre+'</a>'+'</div>')
        return nombre    
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = TipoItemManager()
        TipoItemes = pm.getByFase(int(session['id_fase']))
        return len(TipoItemes), TipoItemes

TipoItem_table_filler = TipoItemTableFiller(DBSession)

  
class TipoItemAddForm(AddRecordForm):
    __model__ = TipoItem
    __omit_fields__ = ['id_TipoItem','TipoItem']
    __omit_fields__= ['campos', 'TipoItem']
    __omit_fields__= ['fase', 'fase']
    __limit_fields__=['nombre']
    __field_order__ = ['nombre']
TipoItem_add_form = TipoItemAddForm(DBSession)

class TipoItemEditForm(EditableForm):
    __model__ = TipoItem
    __omit_fields__ = ['id_tipo_item', 'TipoItem']
    __omit_fields__ = ['campos', 'camposTI']
    __omit_fields__ = ['fase', 'fases']  
    __field_order__ = ['nombre','fase']     
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
        usuarios = pm.buscar(self.buscado)
        return len(usuarios), usuarios   

# ################################################################################################       

class TipoItemController(CrudRestController):
    model = TipoItem
    table = TipoItem_table
    table_filler = TipoItem_table_filler
    new_form = TipoItem_add_form
    edit_form = TipoItem_edit_form
    edit_filler = TipoItem_edit_filler
    campos = CampoController(DBSession)

# ################################################################################################ 
    @with_trailing_slash
    @expose('sgp.templates.get_all_tipoItem')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
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
    @expose('sgp.templates.get_all_tipoItem')
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
        creo = rm.addSinCampos(params['nombre'], int(session['id_fase']))
        if not(creo):
            flash(('Error: Ya existe un tipo de item con el nombre' + params['nombre'] + 'en esta fase.'), 'Error')
            raise redirect('/tipoItem')
        else:      
            id = rm.getByNombreFase(params['nombre'], int(session['id_fase'])).id_tipo_item
            raise redirect('/tipoItem/' + str(id) + '/campos')
#        raise redirect('/campo')

# ################################################################################################       
    @expose('sgp.templates.editTipoItem')
    def edit(self, *args, **kw):
        """Display a page to edit the record."""
        tmpl_context.widget = self.edit_form
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        value['_method'] = 'PUT'
        id = '/tipoItem/' + args[0] + '/campos'
        print args[0]
        return dict(value=value, model=self.model.__name__, pk_count=len(pks), id=id)
#    
    @expose()
    def put(self, *args, **kw):
        rm = TipoItemManager()
        params = kw
        existe = rm.verificaExistencia(params['fase'], params['nombre'])
        if existe:
            flash(('Error: Ya existe un tipo de item con el nombre "' + params['nombre'] + '" en esta fase.'), 'Error')
            dir = '/tipoItem/' + args[0] + '/edit'
            raise redirect(dir)
        p = rm.getById(args)
        p.nombre = params['nombre']
        p.id_fase = params['fase']
        rm.actualizar(params['nombre'], params['fase'], args[0])
        raise redirect('/campo')
# ################################################################################################       
    @expose()
    def post_delete(self, *args, **kw):
        pm = TipoItemManager()
        cm = CampoManager()
        cm.deleteByTipoItem(args)
        pm.deleteById(args)
        raise redirect('./')

    def returnTipoItemList(self):
        session['fase']=''
        session['tipoItem']=''
        raise redirect('/tipoItem')
# ################################################################################################       
    @expose('sgp.templates.importar')
    def importar(self, *args, **kw):
        tipos = TipoItemManager().getNotThisFase(session['id_fase'])
        return dict(tipos=tipos)
    @expose()
    def s_importar(self, *args, **kw):
        importados = kw['selected_tipos']
        for i in importados:
            TipoItemManager().importar(int(i), int(session['id_fase']))
        raise redirect ('/tipoItem')