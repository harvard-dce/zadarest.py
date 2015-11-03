# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'

base_json_server_tmpl = '''{
            "access_type": "NFS",
            "container": "no",
            "container_path": null,
            "created_at": "2015-09-09T15:12:50+00:00",
            "display_name": "{{ server_name }}",
            "host_chap_secret": null,
            "host_chap_user": null,
            "ipsec_iscsi": "0",
            "ipsec_nfs": "0",
            "iqn": null,
            "iscsi_ip": "10.1.0.0/24",
            "lun": null,
            "modified_at": "2015-09-09T15:12:50+00:00",
            "name": "{{ server_name }}",
            "os": null,
            "pm_status": "In-use",
            "read_only": "NO",
            "registered": "no",
            "status": "Active",
            "target": null,
            "thresholds": null,
            "vpsa_chap_secret": "1234",
            "vpsa_chap_user": "user"
      }'''

def get_json_server( server_name='svr' ):
    p = base_json_server_tmpl
    q = p.replace('{{ server_name }}', server_name )
    return q


def get_json_server_response( server_name='svr', response_status=0 ):
    return '{ "response": { "status": %d, "server": %s } }' % ( response_status, get_json_server( server_name ) )


def get_json_server_list_response(
        size=1,
        prefix_for_server_name='svr',
        response_status=0 ):

    server_list = []

    for i in range( size ):
        server_list.append( get_json_server( '%s_%d' % ( prefix_for_server_name, i ) ) )

    return '''{
            "response": {
                "status": %d,
                "count": %d,
                "servers": [ %s ]
            } }''' % ( response_status, size, ','.join( server_list ) )





