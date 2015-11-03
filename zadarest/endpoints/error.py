# -*- coding: utf-8 -*-

class ZadaraVpsaError(Exception):
    """ errors returned by zadara vpsa rest api
    """

    def __init__( self, value, msg ):
        self.value = value
        self.message = msg

    def __str__( self ):
        return "error(%s): %s" % ( self.value, self.message )

