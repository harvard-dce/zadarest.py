# -*- coding: utf-8 -*-

from base import Endpoint

__all__ = ['SnapshotPolicyEndpoint']

class SnapshotPolicyEndpoint( Endpoint ):

    @classmethod
    def snapshot_policies( cls, client ):
        r = client.get('api/snapshot_policies.json')
        if 'response' in r.keys():
            status = int( r['response']['status'] )
            if 0 == status:
                return r['response']['snapshot_policies']
            raise ZadaraVpsaError( status, r['response']['message'] )
        raise ZadaraVpsaError( 1, 'snapshot_policies() json missing "response" key' )


    @classmethod
    def snapshot_policy( cls, client, snapshot_policy_name ):
        r = client.get('api/snapshot_policies/%s.json' % unicode( snapshot_policy_name, 'utf-8' ) )
        if 'response' in r.keys():
            status = int( r['response']['status'] )
            if 0 == status:
                return r['response']['snapshot_policy']
            raise ZadaraVpsaError( status, r['response']['message'] )
        raise ZadaraVpsaError( 1, 'snapshot_policy() json missing "response" key' )






