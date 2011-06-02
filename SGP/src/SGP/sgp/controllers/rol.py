from repoze.what import predicates
from sgp.lib.auth import EvaluarPermiso
from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Permiso, Rol, Recurso
from sgp.managers.PermisoMan import PermisoManager
from sgp.managers.RolMan import RolManager
from sgp.managers.UsuarioMan import UsuarioManager
from sgp.managers.ProyectoMan import ProyectoManager


from sgp.controllers.asignarRol import AsignacionRolController


from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller
from sprox.widgetselector import SAWidgetSelector
from tw.forms import TableForm
from pylons import tmpl_context 

from tg import expose, flash, redirect, request
from tg.decorators import paginate
from tg.decorators import without_trailing_slash, with_trailing_slash
import pylons
from tg import session
#---------------------------------------------------------------------------------------------------------
class RolTable(TableBase):
    __model__ = Rol
    __omit_fields__ = ['id_rol','rol']
    __omit_fields__ = ['permisos','rol']
    __limit_fields__= ['nombre', 'descripcion', 'tipo']
    __field_order__ = ['nombre', 'descripcion', 'tipo']
    
rol_table = RolTable(DBSession)
#---------------------------------------------------------------------------------------------------------
class RolTableFiller(TableFiller):
    __model__ = Rol
    proyecto = None
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = RolManager()
        if (session['admin_sistema']):
            roles = pm.rolesByTipo(0)
        else:
            roles = pm.rolesByTipo(1)
        return len(roles), roles 
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
#        if estado == "creado":
        value = '<div>'\
                    '<table>'\
                        '<tr>'\
                            '<td>'\
                                '<a class="edit_link" href="/rol/'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                            '</td>'\
                            '<td>'\
                                '<form method="POST" action="/rol/'+pklist+'/post_delete" class="button-to">'\
                                    '<input type="hidden" name="_method" value="DELETE" />'\
                                    '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
                                    'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
                                '</form>'\
                            '</td>'\
                            '<td>'\
                                '<a class="assign_link" href="/rol/asignar?id='+pklist+'">Asignar</a>'\
                            '</td>'\
                            '<td>'\
                                '<a class="assign_link" href="/rol/desasignar?id='+pklist+'">Desasignar</a>'\
                            '</td>'\
                        '</tr>'\
                    '</table>'\
                '</div>'
        return value
rol_table_filler = RolTableFiller(DBSession)
#---------------------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------------------
#class PermisosField(SAWidgetSelector):
#    def select(self,d):
#        permisos = DBSession.query(Permiso).filter(Permiso.tipo == 1).all()
#        options = [(permiso.nombre) for permiso in permisos]
#        d['options']= options
#        return d
#
##---------------------------------------------------------------------------------------------------------

class RolAddForm(AddRecordForm):
    __model__ = Rol
    __omit_fields__ = ['id_rol','rol']
    __field_order__ = ['nombre','descripcion','permisos']
    __field_attrs__ = {'descripcion':{'rows':'2'}}
    __dropdown_field_names__ = {'permisos':'nombre'}
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
class Permi():
    id=None
    nombre=None
    activo=None
class RolController(CrudRestController):
    model = Rol
    table = rol_table
    table_filler = rol_table_filler
    new_form = rol_add_form
    edit_form = rol_edit_form
    edit_filler = rol_edit_filler
    assign = AsignacionRolController(DBSession)
    tipo_rol=None

# ################################################################################################
#                                                LISTAR TODO
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
        return dict(model=self.model.__name__, value_list=values, tipo=0)
# ################################################################################################            
#                                        BUSCAR POR NOMBRE
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
#                                        CREAR
# ################################################################################################

    @without_trailing_slash
    @expose('sgp.templates.newRol')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        params=kw
        try:
            self.tipo_rol = int(params['tipo_rol'])
        except:
            pass
        permisos = RolManager().getPermisosByTipo(self.tipo_rol)
        return dict(value=kw, permisos = permisos, tipo = self.tipo_rol, accion=True)

# ------------------------------------------------------------------------------------------------
    @expose()
    def post(self, **kw):
        print "Estoy en el POST"
        p = Rol()
        rm = RolManager()
        params = kw
        print params
        if params['tipo']!="cancelar":
            descripcion = params['descripcion']
            nombre = params['nombre']
            tipo = params['tipo']
            self.tipo_rol=params['tipo']
            try:
                per = params['permisos']
                print per
            except:
                flash(("No se puede crear un rol sin permisos!"), 'error')
                raise redirect("/rol/new")
            permisos = rm.getListaPermisos(per)
            p.nombre = nombre
            p.descripcion = descripcion
            p.tipo = tipo
            p.permisos = permisos
            rm.add(p)
#            try:
            if tipo == 1:
                raise redirect('/rol?id_proyecto='+session['id_proyecto'])
            else:
                raise redirect('/rol')
#            except:
#                raise redirect('/rol')

        else:
            if session['admin_sistema']:
                raise redirect ('/rol')
            raise redirect('/rol?id_proyecto='+session['id_proyecto'])

# ################################################################################################
#                                    EDITAR
# ################################################################################################
     
    @expose('sgp.templates.editRol')
    def edit (self, *args, **kw):
        id_rol = int(args[0])
        r = RolManager().getById(id_rol)
        permisos = r.permisos
        nombre = r.nombre
        self.tipo_rol = r.tipo
        descripcion = r.descripcion
        totalPermisos = RolManager().getPermisosByTipo(self.tipo_rol)
        lista = []
        for i in totalPermisos:
            if i in permisos:
                print (i.nombre + " esta en la lista")
                p = Permi()
                p.nombre = i.nombre
                p.id= i.id_permiso
                p.activo = 1
            else:
                p = Permi()
                p.nombre = i.nombre
                p.id= i.id_permiso
                p.activo = 0
            lista.append(p)
        return dict(permisos = lista,tipo = self.tipo_rol, accion="new", nombre=nombre, descripcion=descripcion, id_rol = id_rol)
        

# ------------------------------------------------------------------------------------------------
    @expose()
    def put(self, *args, **kw):
        print "EN EL PUT"
        print kw
        print args
        rm = RolManager()
        params = kw
        p = rm.getById(params['id_rol'])
        descripcion = params['descripcion']
        nombre = params['nombre']
        per = params['permisos']
        tipo = params['tipo']
        permisos = rm.getListaPermisos(per)
        p.nombre = nombre
        p.descripcion = descripcion
        p.permisos = permisos
        p.tipo=tipo
        rm.update(p)
        params['id_proyecto']=session['actual_p']
        redirect('/rol?id_proyecto=' + params['id_proyecto'])
# ################################################################################################
    @expose()
    def post_delete(self, *args, **kw):
        pm = RolManager()
        pm.deleteById(int(args[0]))
        raise redirect('/rol?id_proyecto='+session['id_proyecto'])
# ################################################################################################
#                                ASIGNAR
# ################################################################################################       
       
    @expose('sgp.templates.asignacion')
    @expose('json')
    def asignar(self, *args, **kw):
        rm = RolManager()
        params = kw
        r = rm.getById(int(params['id']))
        if r.tipo == 0:
            print "Rol de Sistema"
            u = UsuarioManager().getNoThisRol(r.id_rol)
            f=[]
            p=[]
        if r.tipo == 1:
            print "Rol de Proyecto"
            u = UsuarioManager().getNotThisRolThisProject(r.id_rol, int(session['id_proyecto']))
            f = PermisoManager().getFases(session['id_proyecto'])
            p = PermisoManager().getProyecto(session['id_proyecto'])

        return dict(id=r.id_rol,nombre = r.nombre, tipo = r.tipo, usuarios= u, proyectos=p, fases=f, permisos = r.permisos )
    #Submit Asignar
    @expose()
    def s_asignar(self, *args, **kw):
        params = kw
        print args
        print kw
        usuarios = params['usuarios']
        rol = params['id_rol']
        tipo = RolManager().getById(int(rol)).tipo
        if tipo==1:
            permisos_recursos = params['s_recursos']
            RolManager().addPermisoRecursoRolUsuario(permisos_recursos, usuarios, rol, session['id_proyecto'])
            redirect("/rol?id_proyecto="+session['id_proyecto'])
        if tipo==0:
            RolManager().addRolSistemaUsuario(rol,usuarios)
            redirect("/rol")
        
# ################################################################################################       
#                            DESASIGNAR
# ################################################################################################       
    @expose('sgp.templates.desasignacion')
    @expose('json')
    def desasignar(self, *args, **kw):
        rm = RolManager()
        params = kw
        r = rm.getById(int(params['id']))
        if r.tipo == 0:
            print "Rol de Sistema"
            u = UsuarioManager().getThisRol(r.id_rol)
        if r.tipo == 1:
            print "Rol de Proyecto"
            u = UsuarioManager().getThisRolThisProject(r.id_rol, int(session['id_proyecto']))
        return dict(id=r.id_rol,nombre = r.nombre, tipo = r.tipo, usuarios= u, permisos = r.permisos )
    @expose()
    def s_desasignar(self, *args, **kw):
        usuarios = kw['usuarios']
        id_rol = kw['id_rol']
        tipo = RolManager().getById(int(id_rol)).tipo
        if tipo==1:
            print "Desasignar proyecto"
            RolManager().desasignar( id_rol, usuarios, session['id_proyecto'])
            redirect("/rol?id_proyecto="+session['id_proyecto'])
        if tipo==0:
            print "Desasignar sistema"
            RolManager().desasignar( id_rol, usuarios,'-1')
            redirect("/rol")

        
    