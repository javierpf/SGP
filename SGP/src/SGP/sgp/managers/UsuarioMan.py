from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, menu_class, rec, Proyecto
from sgp.managers.ProyectoMan import ProyectoManager
from sgp import model
import transaction

class UsuarioManager():
        
    def getAll(self):
        user = DBSession.query(Usuario).all()
        return user
    
    def getByLogin(self, loginName):
        user = DBSession.query(Usuario).filter(Usuario.usuario.like(loginName)).one();
        return user
    def getByNombre(self, loginName):
        user = DBSession.query(Usuario).filter(Usuario.nombre.like(loginName)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(Usuario).filter(Usuario.id_usuario==(idUser)).one();
        return user
    
    def add(self, user):
        DBSession.add(user)
        transaction.commit()
    
    def _add(self,name,tel,login, passw):
        u = Usuario()
        u.nombre= name
        u.telefono=tel
        u.usuario = login
        u.password=passw
        DBSession.add(u)
        transaction.commit()
        
    def update(self,user):
        DBSession.merge(user)
        transaction.commit()
        
    def delete(self,user):
        DBSession.delete(user)
        transaction.commit()
    
    def deleteById(self, id):
        u = self.getById(id)
        DBSession.delete(u)
        transaction.commit()
        
    def deleteByLogin(self,name):
        u = self.getByLogin(name)
        DBSession.delete(u)
        transaction.commit()
    def buscar(self, buscado):
        lista = DBSession.query(Usuario).filter(Usuario.nombre.op('~*')(buscado)).all()
        return lista
    def getProyectos(self, u_id):
        print "Get Proyectos"
        u = self.getById(u_id)
        l = []
        print u.roles
        for i in u.roles:
            for x in i.permisos_recursos:
                if x.recurso.proyecto in l:
                    pass
                else:
                    if x.recurso.proyecto !=None:
                        l.append(x.recurso.proyecto)
                        print x.recurso.proyecto
                if x.recurso.fase != None:
                    p =ProyectoManager().getById(x.recurso.fase.id_proyecto) 
                    if not(p in l):
                        l.append(ProyectoManager().getById(x.recurso.fase.id_proyecto))
        return l

    def getProyecto(self, uid):
        u = self.getById(uid)
        l = []
        sistema = False
        for i in u.roles:
            if i.id_proyecto >=0:
                l.append(ProyectoManager().getById(i.id_proyecto))
            if i.id_proyecto == -1:
                sistema = True
        
        y = DBSession.query(Proyecto).all()
        for i in y:
            if i.id_administrador == u.id_usuario:
                if not(i in l):
                    l.append(i)
        return (l,sistema)
                           
    def esta(self, m, l):
        for i in l:
            if i.nombre == m.nombre and i.id == m.id:
                return True
        return False
    def index(self, m,l):
        x = 0
        for i in l:
            if i.nombre == m.nombre and i.id==m.id:
                return x
            x=x+1
    def getMenu(self, id_user):
        print "Get Menu"
        u = self.getById(id_user)
        l = []
        for x in u.roles:
            for y in x.permisos_recursos:
                m = menu_class();
                if y.recurso.proyecto != None:
                    m.nombre = y.recurso.proyecto.nombre; m.id = y.recurso.proyecto.id_proyecto
                    if not(self.esta(m,l)):
                        l.append(m)
                if y.recurso.fase != None:
                    m.nombre = y.recurso.fase.nombre; m.id = y.recurso.fase.id_fase
                    m2 = menu_class()
                    m2.nombre = ProyectoManager().getById(y.recurso.fase.id_proyecto).nombre
                    m2.id = ProyectoManager().getById(y.recurso.fase.id_proyecto).id_proyecto
                    if self.esta(m2,l):
                        if self.esta(m, l[self.index(m2,l)].fases):
                            l[l.index(m2)].fases.append(m)
                    else:
                        m2.fases.append(m)
                        l.append(m2)
        return l
    def getThisRol(self, id_rol):
        users = self.getAll()
        l = []
        for i in users:
            for j in i.roles:
                if j.id_rol == id_rol:
                    l.append(i)
                    break         
        return l
    def getNoThisRol(self, id_rol):
        users = self.getAll()
        l = []
        tiene = False
        for i in users:
            for j in i.roles:
                if j.id_rol == id_rol:
                    tiene = True
                    print ("Usuario NO habilitado: " + i.nombre)
                    break         
            if not(tiene):
                print ("Usuario habilitado: " + i.nombre)
                l.append(i)
            tiene = False 
        return l

    def getNotThisRolThisProject(self, id_rol, id_proyecto):
        users = self.getAll()
        l = []
        tiene = False
        for i in users:
            for j in i.roles:
                if j.id_rol == id_rol:
                    if j.id_proyecto == id_proyecto:
                        tiene = True
                        print ("Usuario NO habilitado: " + i.nombre)     
                        break           
                        
            if not(tiene):
                print ("Usuario habilitado: " + i.nombre)                
                l.append(i)
            tiene = False 
        return l 
    def getThisRolThisProject(self, id_rol, id_proyecto):
        users = self.getAll()
        l = []
        for i in users:
            for j in i.roles:
                if j.id_rol == id_rol:
                    if j.id_proyecto == id_proyecto:
                        l.append(i)
                        break           
        return l 