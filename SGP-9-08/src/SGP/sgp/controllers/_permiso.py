from tg import expose
from sgp.lib.base import BaseController
from sgp.model import DBSession
from sgp.model.auth import Permiso
from sgp.managers.PermisoMan import PermisoManager

from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller

from tw.core import WidgetsList
from tw.forms import TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from formencode.validators import Int, NotEmpty, DateConverter, DateValidator
from tg import redirect

class PermisoTable(TableBase):
    __model__ = Permiso
    __omit_fields__ = ['id_permiso','permiso_recurso']
permiso_table = PermisoTable(DBSession)

class PermisoTableFiller(TableFiller):
    __model__ = Permiso
permiso_table_filler = PermisoTableFiller(DBSession)

class PermisoAddForm(AddRecordForm):
    __model__ = Permiso
    __omit_fields__ = ['genre_id','id_permiso']
    __omit_fields__ = ['permiso_recurso']
    __field_order__        = ['nombre','descripcion','tipo']
permiso_add_form = PermisoAddForm(DBSession)

class PermisoEditForm(EditableForm):
    __model__ = Permiso
    __omit_fields__ = ['id_permiso', 'permiso_recurso']
permiso_edit_form = PermisoEditForm(DBSession)

class PermisoEditFiller(EditFormFiller):
    __model__ = Permiso
permiso_edit_filler = PermisoEditFiller(DBSession)

class _PermisoController(CrudRestController):
    model = Permiso
    table = permiso_table
    table_filler = permiso_table_filler
    new_form = permiso_add_form
    edit_form = permiso_edit_form
    edit_filler = permiso_edit_filler
    
    @expose()
    def post(self, **kw):
        pm = PermisoManager()
        params = kw
        pm.addParams(params)
        raise redirect('./')