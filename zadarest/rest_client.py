# -*- coding: utf-8 -*-

"""
zadarest.rest_client
====================
defines a parent zadara api client class
"""

import sys
import json
import requests
from urlparse import urljoin

def handle_http_exceptions( callbacks={} ):
    def wrapper( f ):
        def newfunc( *args, **kwargs ):
            try:
                return f( *args, **kwargs )
            except requests.HTTPError,e:
                resp = e.response
                req = e.request
                if resp.status_code == 404:
                    print >>sys.stderr, "endpoint not found at %s. " % req.url \
                            + "perharps it is not available on this node?"
                elif resp.status_code == 401:
                    print >>sys.stderr, "access denied: %s" % e
                else:
                    for code, handler in callbacks.items():
                        if resp.status_code == code:
                            handler( e )
        return newfunc
    return wrapper


class MyRESTClientError(Exception):
    """ generic handler for zadara vpsa rest api errors
    """

    def __init__( self, value, msg ):
        self.value = unicode( value, 'utf-8' )
        self.message = unicode( msg, 'utf-8' )

    def __str__( self ):
        return "error(%s): %s" % ( self.value, self.message )


class MyRESTClient( object ):

    def __init__( self, url, token ):
        self.token = token
        self.url = url
        self.default_headers = { 'Content-Type': 'application/json', 'X-Token': self.token }


    def send_request_without_response_check( self, mode, path, params={}, extra_headers={} ):
        """ rest api for vpsa operations (cloud console) returns json response
            without 'status' key, only a message.
            use this method that does not expect response.status in the returned json
        """
        headers = self.default_headers.copy()
        headers.update( extra_headers )
        url = urljoin( self.url, path )
        if mode == 'get':
            resp = requests.get( url, params=params, headers=headers )
        elif mode == 'post':
            resp = requests.post( url, params=params, headers=headers )
        elif mode == 'put':
            resp = requests.put( url, params=params, headers=headers )
        elif mode == 'delete':
            resp = requests.delete( url, params=params, headers=headers )
        else:
            MyRESTClientError('400','unknown http method (%s)' % mode )

        resp.raise_for_status()
        return resp.json()


    def send_request( self, mode, path, params={}, extra_headers={} ):
        r = self.send_request_without_response_check( mode, path, params, extra_headers )
        if 'response' in r.keys():
            status = int( r['response']['status'] )
            if 0 == status:
                return r
            raise MyRESTClientError( status, r['response']['message'] )
        raise MyRESTClientError( 1, 'response to %s invalid, json missing "response" key' )


    def get( self, path, params={}, extra_headers={} ):
        return self.send_request( 'get', path, params, extra_headers )

    def post( self, path, params={}, extra_headers={} ):
        return self.send_request( 'post', path, params, extra_headers )

    def put( self, path, params={}, extra_headers={} ):
        return self.send_request( 'put', path, params, extra_headers )

    def delete( self, path, params={}, extra_headers={} ):
        return self.send_request( 'delete', path, params, extra_headers )


