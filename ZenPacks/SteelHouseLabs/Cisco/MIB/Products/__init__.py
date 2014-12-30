import Globals
import os
import logging
from ZODB.transact import transact

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.ZenMenu import ZenMenu

class ZenPack(ZenPackBase):
    def install(self, app):
        ZenPackBase.install(self, app)
        self.buildProducts(app.zport.dmd)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)

    @transact
    def buildProducts(self, dmd):
        from transaction import commit

        manu=dmd.Manufacturers._getOb('Cisco')
        mibs=dmd.Mibs.mibs._getOb('CISCO-PRODUCTS-MIB')
        for entry in manu.products():
            manu.manage_deleteProducts([entry.id])
        products={}
        for node in mibs.nodes():
            prodId = node.id
            prodKey = node.propertyValues()[2]
            products[prodId] = prodKey
        for entry in products:
            manu.manage_addHardware(str(entry))
            newProd = manu.products._getOb(str(entry))
            newProd.productKeys = ['.' + str(products[entry])]
        dmd.Manufacturers.reIndex()
        commit()
