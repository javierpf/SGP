# -*- coding: utf-8 -*-
from repoze.what.predicates import Predicate, is_anonymous
from sgp.model.auth import PermisoRecurso, Proyecto, Fase, DBSession, Usuario, Recurso, RolUsuario
from tg import request

class EvaluarPermiso(Predicate):
    message = "El usuario no cuenta con los permisos necesarios para realizar esta operacion"
    
    def __init__(self, permiso ,**kwargs):
        self.id_permiso = permiso
        if "id_proyecto" in kwargs: 
            self.id_proyecto = kwargs["id_proyecto"]
        else: self.id_proyecto = None
        if "id_fase" in kwargs: 
            self.id_fase = kwargs["id_fase"]
        else: self.id_fase = None
    
    

    def evaluate(self, environ, credentials):
        if is_anonymous().is_met(request.environ): self.unmet()
        usuario = DBSession.query(Usuario).filter_by(nombre = credentials.get('repoze.what.userid')).first()
        roles_de_usuario = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario == usuario.id_usuario)
        id_roles_usuario = []
        for iterador in roles_de_usuario:
            id_roles_usuario.append(iterador.id_rol_usuario)
        denegar = 1
        for ids in id_roles_usuario:
            permisos_recursos = DBSession.query(PermisoRecurso).filter(PermisoRecurso.rol_usuario == ids)
            for permiso_recurso in permisos_recursos:
                if permiso_recurso.id_permiso == self.id_permiso:
                    if self.id_fase:
                        fase = DBSession.query(Recurso).filter(Recurso.id_fase == self.id_fase)
                        if fase.count() > 0:
                            denegar = 0
                    if self.id_proyecto:
                        proyecto = DBSession.query(Recurso).filter(Recurso.id_proyecto == self.id_proyecto)
                        if proyecto.count() > 0:
                            denegar = 0
        if denegar == 1:
            self.unmet()
                