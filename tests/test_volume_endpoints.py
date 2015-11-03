# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'


import pytest
import requests
import httpretty
from sure import expect, should, should_not

from zadarest.endpoints import VolumeEndpoint

from base import *
from json_response_for_volume import *
from json_response_for_server import *
from json_response_for_snapshot import *



class TestVolumeEndpoint(EndpointTestCase):

    @httpretty.activate
    def test_volumes_list( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/volumes.json' % rest_service_url,
                body=get_json_volume_list_response( 3 )
        )

        response = VolumeEndpoint.volumes( self.c )
        len( response ).should.be.equal( 3 )
        response[2].keys().should.contain('name')
        response[2]['name'].should_not.be.different_of('volume-00000002')


    @httpretty.activate
    def test_volume_servers( self ):
        volume_name = 'volume-00000123'
        server_prefix = 'myserver'
        httpretty.register_uri( httpretty.GET,
                '%s/api/volumes/%s/servers.json' % ( rest_service_url, volume_name ),
                body=get_json_server_list_response( size=1, prefix_for_server_name=server_prefix ) )

        response = VolumeEndpoint.servers( self.c, volume_name )
        len( response ).should.be.equal( 1 )
        response[0].keys().should.contain('name')
        response[0]['name'].should_not.be.different_of('%s_0' % server_prefix)


    @httpretty.activate
    def test_volume_snapshot_policies( self ):
        cg_name = 'cg-0000123'
        httpretty.register_uri( httpretty.GET,
                '%s/api/consistency_groups/%s/snapshot_policies.json' % ( rest_service_url, cg_name ),
                body=get_json_snapshot_policies_list_response( 6 ) )

        response = VolumeEndpoint.snapshot_policies( self.c, cg_name )
        len( response ).should.be.equal( 6 )
        response[4].keys().should.contain('display_name')
        response[4]['display_name'].should_not.be.different_of('Hourly Snapshots for a Day')

    @httpretty.activate
    def test_volume_snapshots( self ):
        cg_name = 'cg-00004321'
        httpretty.register_uri( httpretty.GET,
                '%s/api/consistency_groups/%s/snapshots.json' % ( rest_service_url, cg_name ),
                body=get_json_snapshot_list_response( 5 ) )

        response = VolumeEndpoint.snapshots( self.c, cg_name )
        len( response ).should.be.equal( 5 )
        response[2].keys().should.contain('name')
        response[2]['name'].should_not.be.different_of('snap-00000002')




