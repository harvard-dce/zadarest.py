# -*- coding: utf-8 -*-

import json
from base import Endpoint

__all__ = ['ServerEndpoint']

class ServerEndpoint( Endpoint ):

    @classmethod
    def servers( cls, client ):
        r = client.get('api/servers.json')
        if 'response' in r.keys():
            status = int( r['response']['status'] )
            if 0 == status:
                return r['response']['servers']
            raise ZadaraVpsaError( status, r['response']['message'] )
        raise ZadaraVpsaError( 1, 'servers() json missing "response" key' )

    @classmethod
    def attach_volume( cls, client, server_list, volume_name,
            access_type='NFS', readonly='NO', force='NO' ):
        if 1 > len( server_list ):
            raise ValueError( 'empty server_list not allowed' )

        data = { 'id': '%s' % ','.join( server_list ),
                'volume_name': volume_name,
                'access_type': access_type,
                'readonly': readonly,
                'force': force }

        r = client.post( 'api/servers/{0}/volumes.json'.format( server_list[0] ),
                params=data )
        if 'response' in r.keys():
            status = int( r['response']['status'] )
            if 0 == status:
                return server_list
            raise ZadaraVpsaError( status, r['response']['message'] )
        raise ZadaraVpsaError( 1, 'attach_volume() json missing "response" key' )


