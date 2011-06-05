# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

engine = create_engine('postgres://postgres:a@localhost:5432/sgpdb')
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

try:
    from sqlalchemy.dialects.postgresql import *
except ImportError:
    from sqlalchemy.databases.postgres import *
import os
from datetime import datetime
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import synonym
from sgp.model import DBSession

import os
from datetime import datetime
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from sgp.model import DeclarativeBase, metadata, DBSession
#__all__ = ['User', 'Group', 'Permission']

__all__ = ['Usuario', 'Rol', 'Permiso', 'PermisoRecurso', 'Recurso', 'RolUsuario', 'Recurso']
#

atributo = Table(u'atributo', metadata,
    Column(u'id_atributo', INTEGER(), primary_key=True, nullable=False),
    Column(u'id_item', INTEGER(), ForeignKey('item.id_item'), nullable=False),
    Column(u'id_campo', INTEGER(), ForeignKey('campo.id_campo'), nullable=False),
    Column(u'valor', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
)

item = Table(u'item', metadata,
    Column(u'id_item', INTEGER(), primary_key=True, nullable=False),
    Column(u'identificador', VARCHAR(length=45, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
    Column(u'observacion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
    Column(u'complejidad', INTEGER(), nullable=False),
    Column(u'id_fase', INTEGER(), ForeignKey('fase.id_fase'), nullable=False),
    Column(u'id_linea_base', INTEGER(), ForeignKey('linea_base.id_linea_base')),
    Column(u'id_tipo_item', INTEGER(), ForeignKey('tipo_item.id_tipo_item')),
    Column(u'descripcion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column(u'version', INTEGER(), nullable=False),
    Column(u'estado', VARCHAR(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column(u'actual', VARCHAR(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column(u'codigo', VARCHAR(length=5, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
)

permiso_recurso = Table(u'permiso_recurso', metadata,
    Column(u'id_permiso_recurso', INTEGER(), primary_key=True, nullable=False),
    Column(u'id_permiso', INTEGER(), ForeignKey('permiso.id_permiso'), nullable=False),
    Column(u'id_recurso', INTEGER(), ForeignKey('recurso.id_recurso'), nullable=False),
    Column(u'rol_usuario', INTEGER(), ForeignKey('rol_usuario.id_rol_usuario'), nullable=False),
)

linea_base = Table(u'linea_base', metadata,
    Column(u'id_linea_base', INTEGER(), primary_key=True, nullable=False),
    Column(u'estado', INTEGER(), nullable=False),
    Column(u'fecha', DATE(), nullable=False),
    Column(u'usuario', INTEGER(), ForeignKey('usuario.id_usuario'), nullable=False),
    Column(u'fase', INTEGER(), ForeignKey('fase.id_fase'), nullable=False),
)

recurso = Table(u'recurso', metadata,
    Column(u'id_recurso', INTEGER(), primary_key=True, nullable=False),
    Column(u'tipo', INTEGER(), nullable=False),
    Column(u'id_fase', INTEGER(), ForeignKey('fase.id_fase')),
    Column(u'id_proyecto', INTEGER(), ForeignKey('proyecto.id_proyecto')),
)

rol_permiso = Table(u'rol_permiso', metadata,
    Column(u'id_rol', INTEGER(), ForeignKey('rol.id_rol'), primary_key=True, nullable=False),
    Column(u'id_permiso', INTEGER(), ForeignKey('permiso.id_permiso'), primary_key=True, nullable=False),
)

rol_usuario = Table(u'rol_usuario', metadata,
    Column(u'id_rol_usuario', INTEGER(), primary_key=True, nullable=False),
    Column(u'id_rol', INTEGER(), ForeignKey('rol.id_rol'), nullable=False),
    Column(u'id_usuario', INTEGER(), ForeignKey('usuario.id_usuario'), nullable=False),
    Column(u'id_proyecto', INTEGER()),
    
)
class Adjunto(DeclarativeBase):
    __tablename__ = 'adjunto'

    #column definitions
    archivo = Column(u'archivo', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))
    id_adjunto = Column(u'id_adjunto', INTEGER(), primary_key=True, nullable=False)
    id_item = Column(u'id_item', INTEGER(), ForeignKey('item.id_item'), nullable=False)
    nombre = Column(u'nombre', VARCHAR(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    #relation definitions


class Atributo(DeclarativeBase):
    __table__ = atributo
    id_atributo = Column(u'id_atributo', INTEGER(), primary_key=True, nullable=False),
    id_item = Column(u'id_item', INTEGER(), ForeignKey('item.id_item'), nullable=False),
    id_campo = Column(u'id_campo', INTEGER(), ForeignKey('campo.id_campo'), nullable=False),
    valor = Column(u'valor', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),

    #relation definitions
    campo = relationship("Campo", backref=backref("atributo", uselist=False))


class Campo(DeclarativeBase):
    __tablename__ = 'campo'

    #column definitions
    id_campo = Column(u'id_campo', INTEGER(), primary_key=True, nullable=False)
    id_tipo_item = Column(u'id_tipo_item', INTEGER(), ForeignKey('tipo_item.id_tipo_item'), nullable=False)
    nombre = Column(u'nombre', VARCHAR(length=30, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    tipo_dato = Column(u'tipo_dato', VARCHAR(length=8, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    #relation definitions

class Codigo(DeclarativeBase):
    __tablename__ = 'codigo'

    #column definitions
    codigo = Column(u'codigo', INTEGER(), primary_key=True, nullable=False)
    valor = Column(u'valor', INTEGER())

    #relation definitions

class Fase(DeclarativeBase):
    __tablename__ = 'fase'

    #column definitions
    nombre = Column(u'nombre', VARCHAR(length=45, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    descripcion = Column(u'descripcion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))
    id_fase = Column(u'id_fase', INTEGER(), primary_key=True, nullable=False)
    id_proyecto = Column(u'id_proyecto', INTEGER(), ForeignKey('proyecto.id_proyecto'), nullable=False)
    nro_item = Column(u'nro_item', INTEGER())
    orden = Column(u'orden', INTEGER())
    #relation definitions
    items = relationship("Item", backref="fase")
    tipo_items = relation("TipoItem")

class Item(DeclarativeBase):
    __tablename__ = 'item'

    #column definitions
    id_item = Column(u'id_item', INTEGER(), primary_key=True, nullable=False),
    codigo = Column(u'codigo', VARCHAR(length=8, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
    identificador = Column(u'identificador', VARCHAR(length=45, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
    observacion = Column(u'observacion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
    estado = Column(u'estado', VARCHAR(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    complejidad = Column(u'complejidad', INTEGER(), nullable=False),
    id_fase = Column(u'id_fase', INTEGER(), ForeignKey('fase.id_fase'), nullable=False),
    id_linea_base = Column(u'id_linea_base', INTEGER(), ForeignKey('linea_base.id_linea_base')),
    id_tipo_item = Column(u'id_tipo_item', INTEGER(), ForeignKey('tipo_item.id_tipo_item'), nullable=False),
    descripcion = Column(u'descripcion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    version = Column(u'version', INTEGER(), nullable=False),
    actual =  Column(u'actual', VARCHAR(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    
    #relation definitions
    adjuntos = relationship("Adjunto", backref="item")
    atributos = relationship("Atributo", backref="item")
    tipo = relationship("TipoItem")


class LineaBase(DeclarativeBase):
    __table__ = linea_base

    id_linea_base = Column(u'id_linea_base', INTEGER(), primary_key=True, nullable=False),
    estado = Column(u'estado', INTEGER(), nullable=False),
    fecha = Column(u'fecha', DATE(), nullable=False),
    usuario = Column(u'usuario', INTEGER(), ForeignKey('usuario.id_usuario'), nullable=False),
    fase = Column(u'fase', INTEGER(), ForeignKey('fase.id_fase'), nullable=False),

    #relation definitions
    items = relationship("Item", backref="linea_base")
class Permiso(DeclarativeBase):
    __tablename__ = 'permiso'

    #column definitions
    descripcion = Column('descripcion', VARCHAR(length=100, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    id_permiso = Column('id_permiso', INTEGER(), primary_key=True, nullable=False)
    nombre = Column('nombre', VARCHAR(length=45, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    tipo = Column('tipo', INTEGER(), nullable=False)
    roles = relation('Rol', secondary=rol_permiso, backref='permiso')

    #relation definitions
class Usuario(DeclarativeBase):
    __tablename__ = 'usuario'

    #column definitions
    nombre = Column(u'nombre', VARCHAR(length=45, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    id_usuario = Column(u'id_usuario', INTEGER(), primary_key=True, nullable=False)
    telefono = Column(u'telefono', VARCHAR(length=20, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    usuario = Column(u'usuario', VARCHAR(length=20, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    _password = Column(u'password', VARCHAR(length=35, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)


    #relation definitions
    roles = relationship("RolUsuario", backref="usuario")
    @property
    def permissions(self):
        """Return a set with all permissions granted to the user."""
        perms = set()
        for g in self.grupos:
            perms = perms | set(g.permissions)
        return perms
    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter_by(nombre=username).first()
    
    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        # Make sure password is a str because we cannot hash unicode objects
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password + salt.hexdigest())
        password = salt.hexdigest() + hash.hexdigest()
        # Make sure the hashed password is a unicode object at the end of the
        # process because SQLAlchemy _wants_ unicode objects for Unicode cols
        if not isinstance(password, unicode):
            password = password.decode('utf-8')
        self._password = password

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,_set_password))
    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hash = sha1()
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        hash.update(password + str(self.password[:40]))
        return self.password[40:] == hash.hexdigest()

class Proyecto(DeclarativeBase):
    __tablename__ = 'proyecto'

    #column definitions
    nombre = Column(u'nombre', VARCHAR(length=100, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    costo_estimado = Column(u'costo_estimado', INTEGER())
    descripcion = Column(u'descripcion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))
    estado = Column(u'estado', VARCHAR(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))
    fecha_finalizacion = Column(u'fecha_finalizacion', DATE())
    fecha_inicio = Column(u'fecha_inicio', DATE())
    id_proyecto = Column(u'id_proyecto', INTEGER(), primary_key=True, nullable=False)
    id_administrador = Column(u'administrador', INTEGER(), ForeignKey('usuario.id_usuario'), nullable=False)
    nro_fase = Column(u'nro_fase', INTEGER(), nullable=False)
    prefijo = Column(u'prefijo', VARCHAR(length=3, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)

    #relation definitions
    fases = relationship("Fase", backref="proyecto")
    administrador = relationship("Usuario", backref=backref("proyecto", uselist=False))

class PermisoRecurso(DeclarativeBase):
    __table__ = permiso_recurso
    id_permiso_recurso = Column(u'id_permiso_recurso', INTEGER(), primary_key=True, nullable=False),
    id_permiso = Column(u'id_permiso', INTEGER(), ForeignKey('permiso.id_permiso'), nullable=False),
    id_recurso = Column(u'id_recurso', INTEGER(), ForeignKey('recurso.id_recurso'), nullable=False),
    rol_usuario = Column(u'rol_usuario', INTEGER(), ForeignKey('rol_usuario.id_rol_usuario'), nullable=False),
    
    #relation definitions
    permiso = relationship("Permiso", backref=backref("permiso_recurso", uselist=False))
    recurso = relationship("Recurso", backref=backref("permiso_recurso", uselist=False))
    
class Recurso(DeclarativeBase):
    __table__ = recurso
    id_recurso = Column(u'id_recurso', INTEGER(), primary_key=True, nullable=False),
    tipo = Column(u'tipo', INTEGER(), nullable=False),
    id_fase = Column(u'id_fase', INTEGER(), ForeignKey('fase.id_fase')),
    id_proyecto = Column(u'id_proyecto', INTEGER(), ForeignKey('proyecto.id_proyecto')),
    #relation definitions
    fase = relationship("Fase")
    proyecto = relationship("Proyecto")
    

class Relacion(DeclarativeBase):
    __tablename__ = 'relacion'

    #column definitions
    id_item1 = Column(u'id_item1', INTEGER(), ForeignKey('item.id_item'), primary_key=True, nullable=False)
    id_item2 = Column(u'id_item2', INTEGER(), ForeignKey('item.id_item'), primary_key=True, nullable=False)
    tipo_relacion = Column(u'tipo_relacion', INTEGER(), primary_key=True, nullable=False)

    #relation definitions


class Rol(DeclarativeBase):
    __tablename__ = 'rol'

    #column definitions
    descripcion = Column(u'descripcion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    id_rol = Column(u'id_rol', INTEGER(), primary_key=True, nullable=False)
    nombre = Column(u'nombre', VARCHAR(length=45, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    tipo = Column('tipo', INTEGER(), nullable=False)


    #relation definitions
    permisos = relationship("Permiso", secondary = rol_permiso)
    usuarios = relationship("Usuario",secondary=rol_usuario, backref='rol')
    

class TipoItem(DeclarativeBase):
    __tablename__ = 'tipo_item'

    #column definitions
    nombre = Column(u'nombre', VARCHAR(length=30, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False)
    id_fase = Column(u'id_fase', INTEGER(), ForeignKey('fase.id_fase'), nullable=False)
    id_tipo_item = Column(u'id_tipo_item', INTEGER(), primary_key=True, nullable=False)
    prefijo = Column(u'prefijo', VARCHAR(length=3, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))
    descripcion = Column(u'descripcion', TEXT(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))
    #relation definitions
    fase = relationship("Fase")
    campos = relationship("Campo", backref=backref("tipo_item", uselist=False))


    

class RolUsuario(DeclarativeBase):
    __table__ = rol_usuario
    id_rol_usuario = Column(u'id_rol_usuario', INTEGER(), primary_key=True, nullable=False),
    id_rol = Column(u'id_rol', INTEGER(), ForeignKey('rol.id_rol'), nullable=False),
    id_usuario = Column(u'id_usuario', INTEGER(), ForeignKey('usuario.id_usuario'), nullable=False),
    id_proyecto = Column(u'id_proyecto', INTEGER()),
    nombre = "hola"
   
    #relation definitions
    rol = relationship("Rol")
    permisos_recursos = relationship("PermisoRecurso")
    def insert(self, rol,usuario,proyecto):
        inru = rol_usuario.insert()
        inru = rol_usuario.insert().values(id_rol= rol, id_usuario=usuario,id_proyecto=proyecto)
        conn = engine.connect()
        print inru.compile().params
        result = conn.execute(inru)
        result.close()
        return result
# -----------------------------------------------------------------------------------------------------------
class menu_class():
    nombre=None
    id=None
    fases=[]
# -----------------------------------------------------------------------------------------------------------
class rec():
    nombre = None
    id = None    
# -----------------------------------------------------------------------------------------------------------
class CampoValor():
    valor = None
    campo = None
    tipo = None
