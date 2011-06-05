from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Relacion
from sgp.managers.RelacionMan import RelacionManager
from tg import expose, flash, redirect
from tg.decorators import without_trailing_slash, with_trailing_slash

from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller
#from tw.forms.fields import FileField
from tw.forms.fields import InputField

from tg.decorators import paginate
import pylons
from pylons import tmpl_context 
from tg import session
import os

##############################################################################

class RelacionController(CrudRestController):
    model = Relacion
#    table = relacion_table
#    table_filler = relacion_table_filler
#    new_form = relacion_add_form
#******************************************************************************************    
    @without_trailing_slash
    @expose('sgp.templates.newRelacion')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        rm = RelacionManager()
        id_fase = kw['id_fase']
        items1 = rm.getItemByFase(id_fase)
        item2 = rm.getItems(id_fase)
            
        return dict(value=kw, model=self.model.__name__, items1=items1, items2= items2)