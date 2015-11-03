# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'


base_json_vpsa_tmpl = '''{
        "allocation_zones": [
            "zone_0"
        ],
        "cache": {
             "total_partitions": 1,
             "total_gb": 20,
             "gb_from_engine": 20,
             "partitions_from_engine": 1
        },
        "description": "Description for vpsa {{ vpsa_display_name }}",
        "drive_count": 3,
        "drives": [
            "SAS_300GB_15KRPM",
            "SAS_300GB_15KRPM",
            "SAS_300GB_15KRPM"
        ],
        "engine": {
            "key": "vsa.V2.xlarge.vf",
            "name": "1200",
            "specs": "12 CPUs, 48GB RAM"
        },
        "id": {{ vpsa_name }},
        "initial_passcode": "chuchuchu",
        "ip_address": "{{ vpsa_ip }}",
        "locked_down": false,
        "management_url": "{{ vpsa_url }}",
        "name": "{{ vpsa_display_name }}",
        "provider": {
            "key": "aws2",
            "name": "AWS US East (N. Virginia) 2"
        },
        "status": "{{ vpsa_status }}",
        "time_created_gmt": "2015-01-09 22:47:37",
        "version": "Z2"
}'''


def get_json_vpsa(
        vpsa_display_name='this_vpsa',
        vpsa_id=1234,
        vpsa_ip='10.0.0.10',
        vpsa_status='hibernated'
        ):
    p = base_json_vpsa_tmpl
    q = p.replace('{{ vpsa_display_name }}', vpsa_display_name )
    p = q.replace('{{ vpsa_name }}', '%d' % vpsa_id )
    q = p.replace('{{ vpsa_ip }}', vpsa_ip )
    p = q.replace('{{ vpsa_url }}', 'https://vpsa-%08d-aws2.zadaravpsa.com' % vpsa_id )
    q = p.replace('{{ vpsa_status }}', vpsa_status )
    return q


def get_json_vpsa_response(
        vpsa_display_name='this_vpsa',
        vpsa_id=1234,
        vpsa_ip='10.0.0.1',
        vpsa_status='hibernated' ):
    return '{ "vpsa": %s }' % get_json_vpsa(
            vpsa_display_name=vpsa_display_name,
            vpsa_id=vpsa_id,
            vpsa_ip=vpsa_ip,
            vpsa_status=vpsa_status )


def get_json_vpsa_list_response(
        size=1,
        prefix_for_vpsa_name='this_vpsa',
        initial_vpsa_id=1234,
        initial_vpsa_ip='10.0.0.10' ):

    vpsa_list = []

    for i in range( size ):
        ip_list = map(int, initial_vpsa_ip.split('.'))
        ip_list[3] += i  # this might render an invalid ip like 10.0.0.300
        vpsa_display_name = '%s_%d' % ( prefix_for_vpsa_name, i )
        vpsa_id = initial_vpsa_id + i
        vpsa_list.append( get_json_vpsa(
            vpsa_display_name=vpsa_display_name,
            vpsa_id=vpsa_id,
            vpsa_ip='.'.join(['%d' %t for t in ip_list ]),
            vpsa_status = ( 'hibernated' if vpsa_id %2 == 0 else 'created' ) ) )

    return '{ "vpsas": [ %s ] }' % ','.join( vpsa_list )





