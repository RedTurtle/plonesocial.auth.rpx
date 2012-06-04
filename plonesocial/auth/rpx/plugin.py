"""Class: RpxHelper
"""

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

import interface
import plugins

class RpxHelper( # -*- implemented plugins -*-
                    plugins.rpx.RPXPlugin,
                               ):
    """Multi-plugin

    """

    meta_type = 'RPX Helper'
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title



classImplements(RpxHelper, interface.IRpxHelper)

InitializeClass( RpxHelper )
