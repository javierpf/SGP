from repoze.what import predicates
from sgp.lib.auth import EvaluarPermiso
from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Usuario
from sgp.managers.UsuarioMan import UsuarioManager
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
#import tw.dojo 

class UsuarioTable(TableBase):
    __model__ = Usuario
    __omit_fields__ = ['id_usuario','password','telefono','roles']
    
usuario_table = UsuarioTable(DBSession)

class UsuarioTableFiller(TableFiller):
    __model__ = Usuario
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        value = '<div><div><a class="edit_link" href="/usuario/'+pklist+'/edit" style="text-decoration:none">edit</a>'\
              '</div><div>'\
              '<form method="POST" action="/usuario/'+pklist+'/post_delete" class="button-to">'\
            '<input type="hidden" name="_method" value="DELETE" />'\
            '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
            'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
        '</form>'\
        '</div></div>'
        return value    
usuario_table_filler = UsuarioTableFiller(DBSession)

class UsuarioAddForm(AddRecordForm):
    __model__ = Usuario
    __omit_fields__ = ['id_usuario','roles']
    __limit_fields__= ['nombre', 'usuario', 'telefono', '_password']
    __order_fields__= ['nombre', 'usuario', 'telefono', '_password']

usuario_add_form = UsuarioAddForm(DBSession)

class UsuarioEditForm(EditableForm):
    __model__ = Usuario
    __omit_fields__ = ['id_usuario','roles']
usuario_edit_form = UsuarioEditForm(DBSession)

class UsuarioEditFiller(EditFormFiller):
    __model__ = Usuario
usuario_edit_filler = UsuarioEditFiller(DBSession)
# ################################################################################################       
class BusquedaTableFiller(TableFiller):
    __model__ = Usuario
    buscado=""
    def init(self,buscado):
        self.buscado=buscado

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = UsuarioManager()
        usuarios = pm.buscar(self.buscado)
        return len(usuarios), usuarios   

# ################################################################################################       

# ************************************************************************************************************
class UsuarioController(CrudRestController):
    model = Usuario
    table = usuario_table
    table_filler = usuario_table_filler
    new_form = usuario_add_form
    edit_form = usuario_edit_form
    edit_filler = usuario_edit_filler
    @without_trailing_slash
    @expose('sgp.templates.get_all_usuario')
    @expose('json')
    @paginate('value_list', items_per_page=10)
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
#---------------------------------------------------------------------------------------------    
    @without_trailing_slash
    @expose('tgext.crud.templates.new')
    def new(self, *args, **kw):
        print"En el new"
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__)
#---------------------------------------------------------------------------------------------    
    @expose()
    def post(self, **kw):
        #New
        p = Usuario()
        pm = UsuarioManager()
        params = kw
        password = params['_password']
        nombre = params['nombre']
        telefono = params['telefono']
        usuario = params['usuario']
        p.nombre = nombre
        p.telefono = telefono
        p.password = password
        p.usuario = usuario
        pm.add(p)
        raise redirect('/usuario')
    
    @expose()
    def put(self, *args, **kw):
        '''update'''
        pm=UsuarioManager()
        p = pm.getById(args)
        params = kw
        password = params['_password']
        nombre = params['nombre']
        telefono = params['telefono']
        usuario = params['usuario']
        
        p.nombre = nombre
        p.telefono = telefono
        p.password = password
        p.usuario = usuario
        pm.update(p)
       
        raise redirect('/usuario')    

    
    @expose()
    def post_delete(self, *args, **kw):
        '''delete'''
        pm = UsuarioManager()
        pm.deleteById(int(args[0]))
        raise redirect('/usuario')
# ************************************************************************************************************
    @with_trailing_slash
    @expose('sgp.templates.get_all_usuario')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="Usuario")
