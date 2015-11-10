# -*- coding: utf-8 -*-

"""
zadarest
========
defines the main api client class
"""

import sys
import time
import json
import requests
from rest_client import *
from endpoints import *


class ZConsoleClient( MyRESTClient ):

    def __init__( self, url, token ):
        MyRESTClient.__init__( self, url, token )


    @handle_http_exceptions()
    def vpsas(self):
        return VpsaEndpoint.vpsas( self )


    @handle_http_exceptions()
    def vpsa_by_id(self, vpsa_id):
        return VpsaEndpoint.vpsa( self, vpsa_id )


    @handle_http_exceptions()
    def vpsa_state( self, vpsa_id ):
        resp = VpsaEndpoint.vpsa( self, vpsa_id )
        return resp['status']


    @handle_http_exceptions()
    def is_vpsa_up( self, vpsa_id ):
        if 'created' in self.vpsa_state( vpsa_id ):
            return True
        else:
            return False


    @handle_http_exceptions()
    def is_vpsa_down( self, vpsa_id ):
        if 'hibernated' in self.vpsa_state( vpsa_id ):
            return True
        else:
            return False


    @handle_http_exceptions()
    def restore( self, vpsa_id ):
        return VpsaEndpoint.restore( self, vpsa_id )


    @handle_http_exceptions()
    def hibernate( self, vpsa_id ):
        return VpsaEndpoint.hibernate( self, vpsa_id )


    @handle_http_exceptions()
    def do_wakeup( self, vpsa_id, max_tries=5, timeout_in_sec=15 ):
        if self.is_vpsa_up( vpsa_id ):
            return True

        VpsaEndpoint.restore( self, vpsa_id )
        n_tries = 0
        while ( not self.is_vpsa_up( vpsa_id ) ) and n_tries < max_tries:
            time.sleep( timeout_in_sec )
        return True if n_tries < max_tries else False


    @handle_http_exceptions()
    def do_hibernate( self, vpsa_id, max_tries=5, timeout_in_sec=15 ):
        if self.is_vpsa_down( vpsa_id ):
            return True

        VpsaEndpoint.hibernate( self, vpsa_id )
        n_tries = 0
        while ( not self.is_vpsa_down( vpsa_id ) ) and n_tries < max_tries:
            time.sleep( timeout_in_sec )
        return True if n_tries < max_tries else False


    @handle_http_exceptions()
    def vpsa_by_url( self, vpsa_url ):
        all_vpsas = self.vpsas()
        for v in all_vpsas:
            if v['management_url'].find( vpsa_url ) == 0:
                return v
        return None

    @handle_http_exceptions()
    def vpsa_by_export_path( self, export_path, vpsa_token ):
        """ it can only identify a vpsa by export_path if the vpsa is in state 'created'
            vpsas in state 'hibernate' are ignored

            the docs also refer to export_name and it's not clear the difference between
            export_name and export_path, but this is what it's assumed:
            nfs_export_path = '%s:/export/%s' % (server_ip, export_name)
        """
        all_vpsas = self.vpsas()
        for v in all_vpsas:
            if "created" == v['status']:
                vpsa_url = v['management_url']
                headers = { 'Content-Type': 'application/json', 'X-Token': vpsa_token }
                resp = requests.get(
                    urljoin( vpsa_url, "/api/volumes.json" ),
                    headers=headers )
                if 200 == resp.status_code:
                    r = resp.json()
                    if 'response' in r.keys() and 0 == r['response']['status']:
                        for vol in r['response']['volumes']:
                            if 'nfs_export_path' in vol.keys() and vol['nfs_export_path'].find(export_path) >= 0:
                                 return v

                # vpsas that return errors are considered unreachable and ignored
            # vpsas in 'hibernate' status are ignored

        return None


class ZVpsaClient( MyRESTClient ):

    def __init__( self, console_client, vpsa_token, vpsa_id=0, url=None, export_path=None ):
        """ console_client is required to check if vpsa is in 'hibernate' status
            one of the arguments vpsa_id, url, or export_path must be present to identify
            which vpsa to manage; if more than one is present, the first in this order
            will be used: 1. vpsa_id, 2. url, 3. export_path
        """
        self._console_client = console_client

        if vpsa_id > 0:
            v = console_client.vpsa_by_id( vpsa_id )
            if not v:
                raise MyRESTClientError('100', 'vpsa (%s) not found.' % vpsa_id )
            self.info = v

        elif url is not None:
            v = console_client.vpsa_by_url( url )
            if not v:
                raise MyRESTClientError('101', 'vpsa with url (%s) not found.' % self.url )
            self.info = v

        elif export_path is not None:
            v = console_client.vpsa_by_export_path( export_path, vpsa_token )
            if not v:
                raise MyRESTClientError('102', 'vpsa with export_path (%s) not found.' % export_path )
            self.info = v

        MyRESTClient.__init__( self, self.info['management_url'], vpsa_token )


    @handle_http_exceptions()
    def get_volumes(self):
        return VolumeEndpoint.volumes( self )


    @handle_http_exceptions()
    def get_volume(self, volume_name):
        return VolumeEndpoint.volume( self, volume_name )


    @handle_http_exceptions()
    def get_volume_by_display_name( self, display_name ):
        list = VolumeEndpoint.volumes( self )
        if 0 == len( list ):
            return None
        for v in list:
            if v['display_name'] == display_name:
                return v
        return None


    @handle_http_exceptions()
    def get_volume_by_export_path( self, export_path ):
        list = VolumeEndpoint.volumes( self )
        if 0 == len( list ):
            return None
        for v in list:
            if  export_path == v['nfs_export_path']:
                return v
        return None


    @handle_http_exceptions()
    def get_snapshots_for_cgroup(self, cgroup):
        return VolumeEndpoint.snapshots( self, cgroup )


    @handle_http_exceptions()
    def create_snapshot_for_cgroup(self, cgroup, display_name):
        return VolumeEndpoint.create_snapshot( self, cgroup, display_name )


    @handle_http_exceptions()
    def get_all_servers_for_volume(self, volume_name ):
        return VolumeEndpoint.servers( self, volume_name )


    @handle_http_exceptions()
    def detach_volume_from_server( self, volume_name, server_name ):
        return VolumeEndpoint.detach_servers( self, volume_name, server_list=[ server_name ] )


    @handle_http_exceptions()
    def detach_volume_from_all_servers(self, volume_name):
        servers = self.get_all_servers_for_volume( volume_name )

        s_list = []
        for s in servers:
            s_list.append( s['name'] )

        # detach from all servers
        return VolumeEndpoint.detach_servers( self, volume_name, s_list )


    @handle_http_exceptions()
    def attach_volume_to_servers( self, volume_name, server_list ):
        return ServerEndpoint.attach_volume( self, server_list, volume_name )


    @handle_http_exceptions()
    def clone_volume(self,
            cgroup,
            clone_name,
            snap_id=None,
            max_checks=5,
            timeout_in_sec=15 ):
        i = 0
        clone_cg = VolumeEndpoint.clone( self, cgroup, clone_name, snap_id )

        while clone_cg is None and i < max_checks:
            # retrieve cloned volume
            time.sleep( timeout_in_sec )
            cloned_volume = self.get_volume_by_display_name( clone_name )
            if cloned_volume is not None:
                clone_cg = cloned_volume['cg_name']
            i += 1

        if clone_cg is None:
            raise MyRESTClientError( 1, "not able to check that volume was cloned" )

        return cloned_volume


    @handle_http_exceptions()
    def update_export_name_for_volume(self, volume_name, export_name):
        return VolumeEndpoint.update_export_name( self, volume_name, export_name )


    @handle_http_exceptions()
    def get_snapshot_policies_for_cgroup( self, cgroup_name ):
        return VolumeEndpoint.snapshot_policies( self, cgroup_name )

    @handle_http_exceptions()
    def attach_snapshot_policy_to_cgroup( self, cgroup_name, snapshot_policy_name ):
        return VolumeEndpoint.attach_snapshot_policy( self, cgroup_name,
                snapshot_policy_name )

    @handle_http_exceptions()
    def attach_daily_weekly_snapshot_policies_to_cgroup( self, cgroup_name ):
        policies = self.get_all_snapshot_policies()
        for p in policies:
            if 'Daily' in p['display_name']:
                VolumeEndpoint.attach_snapshot_policy( self, cgroup_name, p['name'] )
                continue
            if 'Weekly' in p['display_name']:
                VolumeEndpoint.attach_snapshot_policy( self, cgroup_name, p['name'] )
                continue

    @handle_http_exceptions()
    def get_all_snapshot_policies( self ):
        return SnapshotPolicyEndpoint.snapshot_policies( self )



