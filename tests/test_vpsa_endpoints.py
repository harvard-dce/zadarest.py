# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'


import pytest
import requests
import httpretty
from sure import expect, should, should_not

from zadarest.endpoints import VpsaEndpoint

from base import *
from json_response_for_vpsa import *



class TestVpsaEndpoint(EndpointTestCase):

    @httpretty.activate
    def test_vpsas_empty_list( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas.json' % rest_service_url,
                body='{ "error": "vpsa not found" }')

        response = VpsaEndpoint.vpsas( self.c )
        response.should.be.empty;


    @httpretty.activate
    def test_vpsas_list( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas.json' % rest_service_url,
                body=get_json_vpsa_list_response( 3 )
        )

        response = VpsaEndpoint.vpsas( self.c )
        len( response ).should.be.equal( 3 );
        response[2].keys().should.contain('name')
        response[2]['name'].should_not.be.different_of('this_vpsa_2')


    @httpretty.activate
    def test_vpsa_per_id( self ):
        vpsa_id = 3456
        httpretty.register_uri( httpretty.GET,
                '%s/api/vpsas/%d.json' % ( rest_service_url, vpsa_id ),
                body=get_json_vpsa_response( vpsa_id = vpsa_id )
        )

        response = VpsaEndpoint.vpsa( self.c, vpsa_id )
        response.keys().should.contain('name')
        response['name'].should_not.be.different_of('this_vpsa')


    @httpretty.activate
    def test_hibernate_vpsa( self ):
        httpretty.register_uri( httpretty.POST,
                '%s/api/vpsas/1234/hibernate.json' % rest_service_url,
                body='''{
                    "response": "VPSA being put into hibernating state."
                    }'''
        )

        response = VpsaEndpoint.hibernate( self.c, 1234 )
        response.should.contain('being put into hibernating state')

        # not clear by api doc what is returned in case of error, or what sort of errors
        # can occur when hibernating a vpsa


    @httpretty.activate
    def test_restore_vpsa( self ):
        httpretty.register_uri( httpretty.POST,
                '%s/api/vpsas/1234/restore.json' % rest_service_url,
                body='''{
                    "response": "VPSA restoring."
                    }'''
        )

        response = VpsaEndpoint.restore( self.c, 1234 )
        response.should.contain('restoring')

        # not clear by api doc what is returned in case of error, or what sort of errors
        # can occur when restoring a vpsa











