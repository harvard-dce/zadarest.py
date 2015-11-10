# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'


import pytest
import requests
import httpretty
from sure import expect, should, should_not

from zadarest import ZConsoleClient
from zadarest import ZVpsaClient

from json_response_for_vpsa import *
from json_response_for_volume import *
from json_response_for_server import *
from json_response_for_snapshot import *


zconsole_url = 'https://fake.example.edu'
zconsole_token = 'fakeToken12345'

class TestZVpsaClient( object ):

    @httpretty.activate
    def setup( self ):
        self.c = ZConsoleClient( zconsole_url, zconsole_token )

        vpsa_id = 123
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas/%d.json' % ( zconsole_url, vpsa_id ),
                body=get_json_vpsa_response( vpsa_id=vpsa_id )
        )

        vpsa_c = ZVpsaClient( self.c, vpsa_token='vpsa_token_1234', vpsa_id=vpsa_id )
        self.v = vpsa_c


    @httpretty.activate
    def test_zvpsa_init_with_export_path( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas.json' % zconsole_url,
                body=get_json_vpsa_list_response( size=3, initial_vpsa_id=123 )
        )
        httpretty.register_uri( httpretty.GET,
                'https://vpsa-00000123-aws2.zadaravpsa.com/api/volumes.json',
                body=get_json_volume_list_response( 1 )
        )
        httpretty.register_uri( httpretty.GET,
                'https://vpsa-00000125-aws2.zadaravpsa.com/api/volumes.json',
                body=get_json_volume_list_response( 5 )
        )

        vpsa_c = ZVpsaClient( self.c, vpsa_token='vpsa_token_1234',
                export_path='10.0.0.10/export/volume_00000003')

        vpsa_c.info['id'].must.be.equal( 125 )


    @httpretty.activate
    def test_zvpsa_init_with_vpsa_url( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas.json' % zconsole_url,
                body=get_json_vpsa_list_response( size=4, initial_vpsa_id=1 )
        )

        vpsa_c = ZVpsaClient( self.c, vpsa_token='vpsa_token_1234',
                url='https://vpsa-00000003-aws2.zadaravpsa.com',
                export_path='10.0.0.10/export/volume_00000003')

        vpsa_c.info['id'].must.be.equal( 3 )


    @httpretty.activate
    def test_zvpsa_init_with_vpsa_id( self ):
        vpsa_id = 2222
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas/%d.json' % ( zconsole_url, vpsa_id ),
                body=get_json_vpsa_response( vpsa_id=vpsa_id )
        )

        vpsa_c = ZVpsaClient( self.c, vpsa_token='vpsa_token_1234',
                vpsa_id=vpsa_id,
                url='https://vpsa-00000003-aws2.zadaravpsa.com',
                export_path='10.0.0.10/export/volume_00000003')

        vpsa_c.info['id'].must.be.equal( vpsa_id )


    @httpretty.activate
    def test_zvpsa_volume_by_display_name( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/volumes.json' % self.v.url,
                body=get_json_volume_list_response( 3 )
        )

        volume = self.v.get_volume_by_display_name( 'display_name_volume-00000002' )
        assert( volume is not None )
        volume['name'].should_not.be.different_of( 'volume-00000002' )


    @httpretty.activate
    def test_zvpsa_volume_by_export_path( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/volumes.json' % self.v.url,
                body=get_json_volume_list_response( 3 )
        )

        volume = self.v.get_volume_by_export_path( '10.0.0.10/export/volume_00000001' )
        assert( volume is not None )
        volume['name'].should_not.be.different_of( 'volume-00000001' )


    @httpretty.activate
    def test_zvpsa_volume_servers( self ):
        v_name = 'volume-12345678'
        httpretty.register_uri( httpretty.GET,
                '%s/api/volumes/%s/servers.json' % ( self.v.url, v_name ),
                body=get_json_server_list_response( size=2 ) )










