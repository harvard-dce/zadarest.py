# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'


import pytest
import requests
import httpretty
from sure import expect, should, should_not

from zadarest.endpoints import ServerEndpoint

from base import *
from json_response_for_server import *


class TestServerEndpoint(EndpointTestCase):

    @httpretty.activate
    def test_server_list( self ):
        httpretty.register_uri( httpretty.GET,
                '%s/api/servers.json' % rest_service_url,
                body=get_json_server_list_response()
        )

        response = ServerEndpoint.servers( self.c )
        response.should_not.be.empty
        response[0].keys().should.contain('display_name')












