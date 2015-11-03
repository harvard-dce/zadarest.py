# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'


import pytest
import requests
import httpretty
from sure import expect, should, should_not

from zadarest import ZConsoleClient

from json_response_for_vpsa import *
from json_response_for_volume import *


zconsole_url = 'https://fake.example.edu'
zconsole_token = 'fakeToken12345'

class TestZConsoleClient( object ):

    def setup( self ):
        self.c = ZConsoleClient( zconsole_url, zconsole_token )

    @httpretty.activate
    def test_zconsole_vpsa_list( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas.json' % zconsole_url,
                body=get_json_vpsa_list_response( 3 )
        )

        response = self.c.vpsas()
        len( response ).should.be.equal( 3 );
        response[2].keys().should.contain('name')
        response[2]['name'].should_not.be.different_of('this_vpsa_2')


    @httpretty.activate
    def test_zconsole_vpsa_state( self ):
        vpsa_id = 3456
        vpsa_state = 'created'

        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas/%d.json' % ( zconsole_url, vpsa_id ),
                body=get_json_vpsa_response(
                    vpsa_display_name='vpsa-%08d' % vpsa_id,
                    vpsa_id=vpsa_id,
                    vpsa_ip='10.0.0.1',
                    vpsa_status=vpsa_state )
        )

        response = self.c.vpsa_state( vpsa_id )
        response.should_not.be.different_of( vpsa_state )


    @httpretty.activate
    def test_zconsole_vpsa_up( self ):
        vpsa_id = 3456
        vpsa_state = 'created'

        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas/%d.json' % ( zconsole_url, vpsa_id ),
                body=get_json_vpsa_response(
                    vpsa_display_name='vpsa-%08d' % vpsa_id,
                    vpsa_id=vpsa_id,
                    vpsa_ip='10.0.0.1',
                    vpsa_status=vpsa_state )
        )

        response = self.c.vpsa_state( vpsa_id )
        assert( response )


    @httpretty.activate
    def test_zconsole_success_in_vpsa_do_wakeup( self ):
        vpsa_id = 3456
        vpsa_display_name = 'vpsa-%08d'
        vpsa_ip = '10.0.0.1'

        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas/%d.json' % ( zconsole_url, vpsa_id ),
                responses=[
                    httpretty.Response( body=get_json_vpsa_response(
                        vpsa_display_name=vpsa_display_name,
                        vpsa_id=vpsa_id, vpsa_ip=vpsa_ip,
                        vpsa_status='hibernated' ), status=200 ),
                    httpretty.Response( body=get_json_vpsa_response(
                        vpsa_display_name=vpsa_display_name,
                        vpsa_id=vpsa_id, vpsa_ip=vpsa_ip,
                        vpsa_status='launching' ), status=200 ),
                    httpretty.Response( body=get_json_vpsa_response(
                        vpsa_display_name=vpsa_display_name,
                        vpsa_id=vpsa_id, vpsa_ip=vpsa_ip,
                        vpsa_status='booting' ), status=200 ),
                    httpretty.Response( body=get_json_vpsa_response(
                        vpsa_display_name=vpsa_display_name,
                        vpsa_id=vpsa_id, vpsa_ip=vpsa_ip,
                        vpsa_status='created' ), status=200 )
                ]
        )
        httpretty.register_uri( httpretty.POST,
                '%s/api/vpsas/%d/restore.json' % ( zconsole_url, vpsa_id ),
                body='{"response": "VPSA restoring."}' )

        response = self.c.do_wakeup( vpsa_id, timeout_in_sec=1 )
        assert( response )


    @httpretty.activate
    def test_zconsole_vpsa_by_url( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas.json' % zconsole_url,
                body=get_json_vpsa_list_response( size=4, initial_vpsa_id=1 )
        )

        response = self.c.vpsa_by_url('https://vpsa-00000003-aws2.zadaravpsa.com')
        assert( response )
        response.should.contain('id')
        response['id'].should.be.equal(3)


    @httpretty.activate
    def test_zconsole_vpsa_by_export_path( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas.json' % zconsole_url,
                body=get_json_vpsa_list_response( size=3, initial_vpsa_id=123 )
        )
        httpretty.register_uri( httpretty.GET,
                'https://vpsa-00000123-aws2.zadaravpsa.com/api/volumes.json',
                body=get_json_volume_list_response( 1 )
        )
        httpretty.register_uri( httpretty.GET,
                'https://vpsa-00000124-aws2.zadaravpsa.com/api/volumes.json',
                body=get_json_volume_list_response( 1 )
        )
        httpretty.register_uri( httpretty.GET,
                'https://vpsa-00000125-aws2.zadaravpsa.com/api/volumes.json',
                body=get_json_volume_list_response( 5 )
        )

        response = self.c.vpsa_by_export_path('10.0.0.10/export/volume_00000003', 'fakeToken123')
        assert( response )
        response.keys().should.contain('id')
        response['id'].should.be.equal(125)

