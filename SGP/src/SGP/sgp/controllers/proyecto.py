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
from tg import session
##############################################################################
class ProyectoTable(TableBase):
    __model__ = Proyecto
    __omit_fields__ = ['descripcion','id_proyecto','id_administrador','fecha_inicio','fecha_finalizacion','costo_estimado', 'administrador']
    __dropdown_field_names__ = {'administrador':'nombre'}
    __field_order__        = ['nombre','estado','fases']
    __xml_fields__ = ['nombre']
    
proyecto_table = ProyectoTable(DBSession)
##############################################################################
class ProyectoTableFiller(TableFiller):
    __model__ = Proyecto
    
    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/fase/fases_por_proyecto?id_proyecto='+str(obj.id_proyecto)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre

    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        estado = obj.estado
        if estado == "creado":
            value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                  '</div><div>'\
                  '<form method="POST" action="'+pklist+'" class="button-to">'\
                '<input type="hidden" name="_method" value="DELETE" />'\
                '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
            '</form>'\
            '</div></div>'
            return value
        else:
            value = '<div><div>'\
                  '</div><div>'\
                  '<form>'\
            '</form>'\
            '</div></div>'
            return value
proyecto_table_filler = ProyectoTableFiller(DBSession)
##############################################################################
class ProyectoAddForm(AddRecordForm):
    __model__ = Proyecto
    __omit_fields__ = ['id_Proyecto','estado','fecha_inicio','fecha_finalizacion','costo_estimado','fases', 'id_administrador']
    __dropdown_field_names__ = {'administrador':'nombre'}
    __field_order__ = ['nombre', 'descripcion', 'administrador']
    #__limit_fields__ = ['id_Proyecto','administrador','nombre','descripcion']
proyecto_add_form = ProyectoAddForm(DBSession)
##############################################################################
class ProyectoEditForm(EditableForm):
    __model__ = Proyecto
    __omit_fields__ = ['id_administrador','estado','fases']
proyecto_edit_form = ProyectoEditForm(DBSession)
##############################################################################
class ProyectoEditFiller(EditFormFiller):
    __model__ = Proyecto
proyecto_edit_filler = ProyectoEditFiller(DBSession)
##############################################################################
class BusquedaTableFiller(TableFiller):
    __model__ = Proyecto
    buscado=""
    def init(self,buscado):
        self.buscado=buscado
    
    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/fase/fases_por_proyecto?id_proyecto='+str(obj.id_proyecto)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre
    
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = ProyectoManager()
        proyectos = pm.buscar(self.buscado)
        return len(proyectos), proyectos   
    
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        estado = obj.estado
        if estado == "creado":
            value = '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                  '</div><div>'\
                  '<form method="POST" action="'+pklist+'" class="button-to">'\
                '<input type="hidden" name="_method" value="DELETE" />'\
                '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
            '</form>'\
            '</div></div>'
            return value
        else:
            value = '<div><div>'\
                  '</div><div>'\
                  '<form>'\
            '</form>'\
            '</div></div>'
            return value
        
##############################################################################

class ProyectoController(CrudRestController):
    model = Proyecto
    table = proyecto_table
    table_filler = proyecto_table_filler
    new_form = proyecto_add_form
    edit_form = proyecto_edit_form
    edit_filler = proyecto_edit_filler
    
#******************************************************************************************    
    @expose()
    def post(self, **kw):
        '''New'''
        p = Proyecto()
        pm = ProyectoManager()
        params = kw
       
        p.descripcion = params['descripcion']
        p.nombre = params['nombre']
        p.estado = 'creado'
        p.id_administrador = params['administrador']
        pm.add(p)
        raise redirect('./')
#******************************************************************************************    
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
        p.estado = 'iniciado'
        pm.update(p)
        
        session['id_proyecto'] = args
        session.save()
        
        raise redirect('/fase/')
   
#****************************************************************************************** 
    @expose()
    def post_delete(self, *args, **kw):
        '''delete'''
        pm = ProyectoManager()
        proyecto = pm.getById(args)
        if proyecto.estado == 'creado':
            pm.deleteById(args)
            raise redirect('./')
        else:
            raise redirect('/proyecto')
        
 #******************************************************************************************       
    @with_trailing_slash
    @expose('sgp.templates.get_all_proyecto')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="Proyecto")
    
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
    
    
    @expose('tgext.crud.templates.edit')
    def edit(self, *args, **kw):
        """Display a page to edit the record."""
        
        tmpl_context.widget = self.edit_form
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        value['_method'] = 'PUT'
        return dict(value=value, model=self.model.__name__, pk_count=len(pks))
        
        