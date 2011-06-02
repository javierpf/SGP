from sgp.lib.base import BaseController
from sgp.model import metadata, DBSession
from sgp.model.auth import Item,Usuario, Rol, Permiso, TipoItem, Campo
from sgp import model
from sgp.managers.CampoMan import CampoManager
from sgp.managers.FaseMan import FaseManager

import transaction

class TipoItemManager():
        
    def getAll(self):
        user = DBSession.query(TipoItem).all()
        return user
    
    def getByName(self, loginName):
        user = DBSession.query(TipoItem).filter(TipoItem.nombre.like(loginName)).one();
        return user
    
    def getById(self, idUser):
        user = DBSession.query(TipoItem).filter(TipoItem.id_tipo_item==(idUser)).one();
        return user
    
    def add(self, user):
        print "Agregado"
        DBSession.add(user)
        transaction.commit()
    
    def _add(self,name,tel,login, passw):
        u = TipoItem()
        u.nombre= name
        u.telefono=tel
        u.TipoItem = login
        u.password=passw
        DBSession.add(u)
        transaction.commit()
    def addParams(self,nombre, id_fase, id_campos):
        r = TipoItem()
        r.nombre = nombre
        r.id_fase = id_fase
        r.fase = FaseManager().getById(id_fase)
        r.campos = self.getListaCampos(id_campos)
        self.add(r)
    def addSinCampos(self,nombre, id_fase):
        print ("Agregar tipo de item: " + nombre + " en la fase " + str(id_fase))
        r = TipoItem()
        r.nombre = nombre
        r.id_fase = id_fase
        r.fase = FaseManager().getById(id_fase)
        b = self.verificaExistencia(id_fase, nombre)
        if not(b)   :
            self.add(r)
            return True
        return False
        
        
    def verificaExistencia(self, id_fase, name):
        print ("Verificando si existe: " + str(id_fase) + "   " + name)
        c2 = DBSession.query(TipoItem).filter(TipoItem.nombre.like(name))
        c1 = DBSession.query(TipoItem).filter(TipoItem.id_fase==id_fase)
        c = c2.intersect(c1)
        if c.count()>0:
            print "Indica que existe"
            return True
        return False
    def update(self,user):
        DBSession.merge(user)
        transaction.commit()
        print "Actualizado"
        
    def actualizar(self, nombre, fase, id_tipo):
        print( "Actualizacion del tipo de item: " + nombre)
        fases =FaseManager().getById(fase)
        ti = TipoItem()
        ti.nombre = nombre
        ti.id_tipo_item = id_tipo
        ti.fase = fases
        self.update(ti)
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
        print "----------BUSQUEDA TIPO ITEM--------------"
        lista = DBSession.query(TipoItem).filter(TipoItem.nombre.op('~*')(buscado)).all()
        print lista
        return lista
    def getListaCampos(self, lista_id):
        listaCampos = []
        pm = CampoManager()
        for i in lista_id:
            p = pm.getById(i)
            listaCampos.append(p)
        return listaCampos
    def getByNombreFase(self,nombre, fase):
        if fase=='':
            f=0
            nombre=''
        else:
            f=int(fase)
        u = DBSession.query(TipoItem).filter(TipoItem.nombre.like(nombre))
        us= DBSession.query(TipoItem).filter(TipoItem.id_fase==f)
        user = us.intersect(u)
        if user.count()>0:
            return user.one()
        else:
            return None
    def getByNombreIdFase(self,nombre, fase):
        u = DBSession.query(TipoItem).filter(TipoItem.nombre.like(nombre))
        us= DBSession.query(TipoItem).filter(TipoItem.id_fase==fase)
        user = us.intersect(u)
        if user.count()>0:
            return user.one()
        else:
            return None
    def getByFase(self, id_fase):
        tipos = DBSession.query(TipoItem).filter(TipoItem.id_fase == id_fase).all()
        return tipos
    def addCampo(self,nombre, tipodato, tipoItem):
        c = Campo()
        c.nombre = nombre
        c.tipo_dato=tipodato
        tipoItem.append(c)
        self.update(tipoItem)
    
    def importar(self, id_tipo, id_fase):
        transaction.begin()
        ti = self.getById(id_tipo)
        nuevo = TipoItem()
        nuevo.nombre =ti.nombre
        nuevo.id_fase = id_fase
        DBSession.add(nuevo)
        DBSession.flush()
        for c in ti.campos:
            cn = Campo()
            cn.nombre = c.nombre
            cn.tipo_dato = c.tipo_dato
            nuevo.campos.append(cn)
            DBSession.merge(nuevo)
            DBSession.flush()
        transaction.commit()
    def getNotThisFase(self, id_fase):
        tipos = DBSession.query(TipoItem).filter(TipoItem.id_fase!=id_fase).all()
        return tipos 
        