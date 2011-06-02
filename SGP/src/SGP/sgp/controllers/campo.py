from repoze.what import predicates
from sgp.lib.auth import EvaluarPermiso
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

from tg import expose, flash, require, url, request, redirect
from tg.decorators import paginate
from tg.decorators import without_trailing_slash, with_trailing_slash
import pylons
from tg import session

#get_one
class CampoTable(TableBase):
    __model__ = Campo
#    __omit_fields__ = ['id_tipo_item','genre_id']
#    __omit_fields__ = ['id_campo','genre_id_fase']
    __limit_fields__=['nombre','tipo_dato']
#    __field_order__ = [ 'fase','nombre', 'campos']
    
Campo_table = CampoTable(DBSession)

class CampoTableFiller(TableFiller):
    __model__ = Campo
    tipo = ''
    fase = 0
    def init(self,fase,ti):
        self.tipo=ti
        self.fase=fase
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = CampoManager()
        tm = TipoItemManager()
        ti = tm.getByNombreFase(self.tipo, self.fase)
        if ti==None:
            return 0, []
        Campo = pm.getByTipoItem(ti.id_tipo_item)
        return len(Campo), Campo
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
    __limit_fields__= ['nombre', 'tipo_dato']
    __field_order__ = ['nombre','tipo_dato']   
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
    id_tipo_item = None
    tipoIt=None
# ################################################################################################
    def _before(self, *args, **kw):
        print request.url
        print request.url.split("/")
        self.id_tipo_item = unicode(request.url.split("/")[-3])
        print ("Before: "+str(self.id_tipo_item))
        try:
            self.tipoIt = TipoItemManager().getById(int(self.id_tipo_item))
        except:
            pass  
        super(CampoController, self)._before(*args, **kw)
        
        
    @with_trailing_slash
    @expose('sgp.templates.get_all_campo')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
#        fase    =   session['fase']
#        ti      =   session['tipoItem']        
        fase    =   TipoItemManager().getById(self.id_tipo_item).id_fase
        ti      =   TipoItemManager().getById(self.id_tipo_item).nombre
        
        filler  =    CampoTableFiller(DBSession)

        filler.init(fase,ti)
        tmpl_context.widget = self.table
        value = filler.get_value()
        return dict(value_list=value, fase=fase, tipoItem=ti, model="Campo")
# ################################################################################################                
    @with_trailing_slash
    @expose('sgp.templates.get_all_campo')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def camposTipo(self, **kw):
#        fase    =   session['fase']
#        ti      =   session['tipoItem']
        fase    =   self.tipoIt.id_fase
        ti      =   self.tipoIt.id_tipo_item


        filler  =    CampoTableFiller(DBSession)

        filler.init(fase,ti)
        tmpl_context.widget = self.table
        value = filler.get_value()
        return dict(value_list=value, fase=fase, tipoItem=ti, model="Campo")
    
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
    @without_trailing_slash
    @expose('sgp.templates.newCampo')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        nombre = TipoItemManager().getById(int(self.id_tipo_item)).nombre
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__, fase = session['id_fase'], tipoItem=nombre, action=('/tipoItem/' + str(self.id_tipo_item) +'/campos/post'), id_tipo_item = self.id_tipo_item)

# ****************************************************************************************************    
    @expose()
    def post(self, **kw):
        tm = TipoItemManager()
        cm= CampoManager()
        params = kw
        
#        fase = session['fase']
#        tipo = session['tipoItem']
        fase    =   self.tipoIt.id_fase
        tipo      =   self.tipoIt.nombre


        #devuelve query
        ti = tm.getByNombreFase(tipo,fase)
        creo = cm.addParams(params['nombre'], params['tipo_dato'], ti.id_tipo_item)
        if not(creo):
            flash(('Ya existe un campo con el nombre "' + params['nombre']+ '" en este tipo de item.'), 'error')
            raise redirect('/tipoItem/' + str(self.id_tipo_item)  + '/campos/new')
        else:        
            raise redirect('/tipoItem/' + str(self.id_tipo_item)  + '/campos')
# ################################################################################################
    def returnTipoItemList(self):
        session['fase']=''
        session.save()
        session['tipoItem']=''
        session.save()
        raise redirect('/tipoItem')
               


# ################################################################################################       
    @expose('sgp.templates.editCampo')
    def edit(self, *args, **kw):
        print "Dentro del EDIT"
        print kw
        print args
        c = CampoManager().getById(int(args[0]))
        cadena, numerico, date = (False, False, False)
        if c.tipo_dato=="numerico":
            numerico=True;
        if c.tipo_dato=="cadena":
            cadena = True;
        if c.tipo_dato=="date":
            date = True
        nombre = TipoItemManager().getById(c.id_tipo_item).nombre
        return dict(id_campo =c.id_campo,nombre=c.nombre,tipo = c.tipo_dato, cadena=cadena,numerico=numerico, date=date, tipoItem=nombre, id_tipo_item = c.id_tipo_item )
    @expose()
    def put(self, *args, **kw):
        print "Dentro del put"
        print args
        print kw
        rm = CampoManager()
        params = kw
        rm.actualizar(int(params['id_campo']), params['nombre'], params['tipo_dato'])
        raise redirect('/tipoItem/' + str(self.tipoIt.id_tipo_item) + '/campos')
# ################################################################################################       
    @expose()
    def post_delete(self, *args, **kw):
        pm = CampoManager()
        pm.deleteById(args)
        raise redirect('./')
# ################################################################################################
           
