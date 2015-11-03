# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'

import json

snapshot_policies = [
        {
            "attach": "YES",
            "create_empty": "NO",
            "create_policy": "0 * * * *",
            "created_at": "2014-12-05T22:13:39+00:00",
            "delete_policy": "N24",
            "destination": "NO",
            "destination_delete_policy": "N24",
            "display_name": "Hourly Snapshots for a Day",
            "job_display_name": None,
            "job_name": None,
            "modified_at": "2014-12-05T22:13:39+00:00",
            "name": "policy-00000002",
            "paused": "NO",
            "type": None
        },
        {
            "attach": "YES",
            "create_empty": "NO",
            "create_policy": "0 0 * * *",
            "created_at": "2014-12-05T22:13:39+00:00",
            "delete_policy": "N7",
            "destination": "NO",
            "destination_delete_policy": "N7",
            "display_name": "Daily Snapshots for a Week",
            "job_display_name": None,
            "job_name": None,
            "modified_at": "2014-12-05T22:13:39+00:00",
            "name": "policy-00000003",
            "paused": "NO",
            "type": None
        },
        {
            "attach": "YES",
            "create_empty": "NO",
            "create_policy": "0 0 * * 0",
            "created_at": "2014-12-05T22:13:39+00:00",
            "delete_policy": "N53",
            "destination": "NO",
            "destination_delete_policy": "N53",
            "display_name": "Weekly Snapshots for a Year",
            "job_display_name": None,
            "job_name": None,
            "modified_at": "2014-12-05T22:13:39+00:00",
            "name": "policy-00000004",
            "paused": "NO",
            "type": None
        },
        {
            "attach": "NO",
            "create_empty": "NO",
            "create_policy": "manual",
            "created_at": "2015-07-09T21:03:00+00:00",
            "delete_policy": None,
            "destination": "NO",
            "destination_delete_policy": None,
            "display_name": "manual policy",
            "job_display_name": None,
            "job_name": None,
            "modified_at": "2015-07-09T21:03:00+00:00",
            "name": "policy-00000006",
            "paused": "NO",
            "type": None
        }
    ]

base_json_snapshot_tmpl = '''{
        "cg_display_name": "{{ cg_display_name }}",
        "cg_name": "{{ cg_name }}",
        "created_at": "2015-10-27T15:00:16+00:00",
        "display_name": "{{ snapshot_display_name }}",
        "modified_at": "2015-10-27T15:00:17+00:00",
        "name": "{{ snapshot_name }}",
        "pool_name": "pool-00000001",
        "status": "normal"
    }'''

def get_json_snapshot_policies_list_response( size=1, response_status=0 ):
    policy_list = []
    total = len( snapshot_policies )

    for i in range( size ):
        policy_list.append( json.dumps( snapshot_policies[ i % total ] ) )

    return '''{
            "response": {
                "status": %d,
                "count": %d,
                "snapshot_policies": [ %s ]
       } }''' % ( response_status, size, ','.join( policy_list ) )


def get_json_snapshot(
        cg_display_name='this_volume_display_name',
        cg_name='cg-00000001',
        snapshot_display_name='snapshot_display_name',
        snapshot_name='snap-00000001' ):
    p = base_json_snapshot_tmpl
    q = p.replace('{{ cg_display_name }}', cg_display_name )
    p = q.replace('{{ cg_name }}', cg_name )
    q = p.replace('{{ snapshot_display_name }}', snapshot_display_name )
    p = q.replace('{{ snapshot_name }}', snapshot_name )
    return p


def get_json_snapshot_response(
        cg_display_name='this_volume_display_name',
        cg_name='cg-00000001',
        snapshot_display_name='snapshot_display_name',
        snapshot_name='snap-00000001',
        response_status=0 ):
    return '{ "response": { "status": %d, "snapshot_policy": %s } }' % ( response_status,
            get_json_snapshot(
                cg_display_name=cg_display_name,
                cg_name=cg_name,
                snapshot_display_name=snapshot_display_name,
                snapshot_name=snapshot_name ) )


def get_json_snapshot_list_response(
        size=1,
        cg_display_name='volume_display_name',
        cg_name='cg-00000001',
        response_status=0 ):

    snapshot_list = []

    for i in range( size ):
        snapshot_list.append( get_json_snapshot(
            cg_display_name=cg_display_name,
            cg_name=cg_name,
            snapshot_display_name='snapshot_display_name-%08d' % i,
            snapshot_name='snap-%08d' % i ) )

    return '''{
            "response": {
                "status": %d,
                "count": %d,
                "snapshots": [ %s ]
            } }''' % ( response_status, size, ','.join( snapshot_list ) )





