from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Fase
from sgp.managers.FaseMan import FaseManager
from sgp.managers.ProyectoMan import ProyectoManager
from sgp.managers.CodigoMan import CodigoManager


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
class faselist():
    nombre = None
    id = None
##############################################################################
class FaseTable(TableBase):
    __model__ = Fase
    __omit_fields__ = ['id_fase','id_proyecto','items','proyecto','codigo','tipo_items']    
fase_table = FaseTable(DBSession)
##############################################################################
class FaseTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    def init(self,buscado):
        self.buscado=buscado
        
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Fasees = pm.buscar_por_proyecto(self.buscado)
        return len(Fasees), Fasees   
    
fase_table_filler = FaseTableFiller(DBSession)

############################################################################## 
class FaseAddForm(AddRecordForm):
    __model__ = Fase
    __omit_fields__ = ['id_Fase','proyecto','items','estado','codigo','tipo_items']
fase_add_form = FaseAddForm(DBSession)
##############################################################################
class FaseEditForm(EditableForm):
    __model__ = Fase
    __omit_fields__ = ['id_Fase', 'proyecto','items','estado','codigo','tipo_items','nro_item']
#    __field_order__ = ['nombre','descripcion','permisos']   
#    __field_attrs__ = {'descripcion':{'rows':'2'}}

    
fase_edit_form = FaseEditForm(DBSession)
##############################################################################
class FaseEditFiller(EditFormFiller):
    __model__ = Fase
    __omit_fields__ = ['estado']
fase_edit_filler = FaseEditFiller(DBSession)
##############################################################################
class FasesProyectoTable(TableBase):
    __model__ = Fase
    __limit_fields__=['nombre', 'descripcion']
    __xml_fields__ = ['nombre']
fase_proyecto_table = FasesProyectoTable(DBSession)
class FasesProyectoTableNotActions(TableBase):
    __model__ = Fase
    __limit_fields__=['nombre', 'descripcion']
    __omit_fields__=['__actions__']
    __xml_fields__ = ['nombre']
fase_proyecto_table_not_actions = FasesProyectoTableNotActions(DBSession)
# ################################################################################################       
class FasePorProyectoTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    estado = ""
    def init(self,buscado):
        self.buscado=buscado
    def initEstado(self, estado):
        self.estado=estado
        
    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/item/?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
#        nombre = ('<div>'+'<a href="/item/get_all?id_proyecto='+str(obj.id_proyecto)+'&id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        if self.estado == "creado":
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
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Fasees = pm.buscar_por_proyecto(self.buscado)
        return len(Fasees), Fasees   
####################################################################################################    
class BusquedaTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    def init(self,buscado):
        self.buscado=buscado
        

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Campoes = pm.buscar(self.buscado, session['id_proyecto'])
        return len(Campoes), Campoes  
####################################################################################################    
class BusquedaProyectoTableFiller(TableFiller):
    __model__ = Fase
    buscado=""
    def init(self,buscado,id_proyecto):
        self.buscado=buscado
        self.id_proyecto = id_proyecto

    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/item'+'">'+obj.nombre+'</a>'+'</div>')
#        nombre = ('<div>'+'<a href="/item/get_all?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre

    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        pm = FaseManager()
        Campoes = pm.buscar(self.buscado, self.id_proyecto)
        return len(Campoes), Campoes  
##############################################################################
class FasesProyectoTableFiller(TableFiller):
    __model__ = Fase

    buscado=""
    estado=""
    def init(self,id_proyecto):
        self.id_proyecto= id_proyecto
    def initEstado(self, estado):
        self.estado=estado
    def __actions__(self, obj):
        """Override this function to define how action links should be displayed for the given record."""
        primary_fields = self.__provider__.get_primary_fields(self.__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
        if self.estado == "creado":
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
    def nombre(self, obj):
        nombre = ('<div>'+'<a href="/item/items?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
#        nombre = ('<div>'+'<a href="/item/get_all?id_fase='+str(obj.id_fase)+'">'+obj.nombre+'</a>'+'</div>')
        return nombre
        
    def _do_get_provider_count_and_objs(self, buscado="", **kw):
        print self.id_proyecto
        pm = FaseManager()
        Fasees = pm.buscar_por_proyecto(self.id_proyecto)
        return len(Fasees), Fasees   

# ####################FASe############################################################################       

class FaseController(CrudRestController):
    model = Fase
    table = fase_table
    table_filler = fase_table_filler
    new_form = fase_add_form
    edit_form = fase_edit_form
    edit_filler = fase_edit_filler
    table_fases = fase_proyecto_table
    table_fases_action_null=fase_proyecto_table_not_actions
    
    fase=0
# ################################################################################################
    @with_trailing_slash
    @expose('sgp.templates.get_all_fase')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        """Return all records.
           Pagination is done by offset/limit in the filler method.
           Returns an HTML page with the records if not json.
        """   
        busqueda_filler = FaseTableFiller(DBSession)
        id_proyecto = session['id_proyecto']
        busqueda_filler.init(id_proyecto)
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        return dict(value_list=value, model="Fase", id_proyecto =id_proyecto)

# ################################################################################################            
    @with_trailing_slash
    @expose('sgp.templates.get_all_fase')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar(self, **kw):
        params = kw     
        busqueda_filler = BusquedaTableFiller(DBSession)
        busqueda_filler.init(params["parametro"])
        
        tmpl_context.widget = self.table
        value = busqueda_filler.get_value()
        cantidad = FaseManager().cantidad(int(session['id_proyecto']))
        return dict(value_list=value, model="Fase", cant_fases = cantidad)

# ################################################################################################   
    @with_trailing_slash
    @expose('sgp.templates.proyecto_fases')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def buscar_proyecto_fases(self,*args,**kw):
        params = kw     
        busqueda_filler = BusquedaProyectoTableFiller(DBSession)
        print params['id_proyecto']
        busqueda_filler.init(params['parametro'],params['id_proyecto'])
        self.table_fases(ProyectoManager().getById(int(params['id_proyecto'])).estado)
        tmpl_context.widget = self.table_fases
        value = busqueda_filler.get_value()
        
        return dict(value_list=value, model="Fase",id_proyecto = params['id_proyecto'])
    
    @expose()
    def post(self, **kw):
        '''Nuevo'''
        rm = FaseManager()
        params = kw
        '''crear la nueva fase'''
        fase = Fase()
        fase.nombre = params['nombre']
        fase.descripcion = params['descripcion']
        fase.id_proyecto = session['id_proyecto']
        fase.estado = 'inicial'
        fase.nro_item=0
        fase.orden=0
        
        codigo= rm.generarCodigo(session['id_proyecto'])
        print codigo
        
        fase.codigo = codigo
        rm.add(fase)
        raise redirect('/fase/fases_por_proyecto?id_proyecto='+session['id_proyecto'])

# ################################################################################################       
    @expose()
    def put(self, *args, **kw):
        '''editar'''
        rm = FaseManager()
        p = rm.getById(args)
        params = kw
        
        p.descripcion = params['descripcion']
        p.nombre = params['nombre']
        rm.update(p)
        raise redirect('../')
# ################################################################################################       
    @expose()
    def post_delete(self, *args, **kw):
        pm = FaseManager()
        pm.deleteById(args)
        raise redirect('./')
# ################################################################################################
    @with_trailing_slash
    @expose('sgp.templates.proyecto_fases')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def fases_por_proyecto(self, *args, **kw):
        print "Fases por proyecto"
        params = kw
        fase_filler = FasesProyectoTableFiller(DBSession)
        id_proyecto = params['id_proyecto']
        proyecto = ProyectoManager().getById(int(id_proyecto))
        session['id_proyecto']=id_proyecto; session.save()
        session['proyecto']=proyecto.nombre; session.save()
        session['conn_tipo'] = 0; session.save()
        
        if proyecto.estado !="creado":
            session['estado']="iniciado"
        else:
            session['estado']="creado"
        session.save()                
        if proyecto.estado=="creado":
            if proyecto.fases == []:
                try:
                    if not(params['sist']):
                        raise redirect ('/proyecto/'+params['id_proyecto']+'/edit')
                except:
                    raise redirect ('/proyecto/'+params['id_proyecto']+'/edit')                    
        cantidad=False
        if len(proyecto.fases)>1:
            cantidad = True
        fase_filler.initEstado(proyecto.estado)
        fase_filler.init(id_proyecto)
        #self.table_fases.init(proyecto.estado)
        if proyecto.estado=="iniciado":
            tmpl_context.widget = self.table_fases_action_null
        else:
            tmpl_context.widget = self.table_fases
            
        value = fase_filler.get_value()
        
        return dict(value_list=value, model="Fase", cant_fases=cantidad)
    @expose()
    def terminar(self, **kw):
        print"terminar"
        print ("id_proyecto:" + session['id_proyecto'])
        pm=ProyectoManager()
        p = pm.getById(int(session['id_proyecto']))
        p.estado = 'iniciado'
        pm.update(p)
        raise redirect('/fase/fases_por_proyecto?id_proyecto='+session['id_proyecto'])
    @expose("sgp.templates.ordenar_fases")
    def ordenar(self):
        proyecto = ProyectoManager().getById(int(session['id_proyecto']))
        cantidad = len(proyecto.fases)
        orden = []
        for i in range(cantidad):
            x = i+1
            orden.append(x)
        fases = []
        for f in proyecto.fases:
            fa = faselist(); fa.nombre =f.nombre; fa.id = f.id_fase 
            fases.append(fa)
        print fases
        print orden
        return dict(orden = orden, fases=fases)
    @expose()
    def s_ordenar(self,*args, **kw):
        params  = kw
        print params
        if params['submit']=="terminar":
            for i in params['posicion']:
                orden, fase = i.split('#')
                FaseManager().ordenarFase(int(orden), int(fase))
            self.terminar()
        else:
            raise redirect('/fase/fases_por_proyecto?id_proyecto='+session['id_proyecto'])