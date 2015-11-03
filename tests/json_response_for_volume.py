# -*- coding: utf-8 -*-

import os
os.environ['TESTING'] = 'True'

base_json_volume_tmpl = ''' {
                "access_type": null,
                "alert_mode": 360,
                "allocated_capacity": 10,
                "atime_update": "NO",
                "cache": null,
                "capacity_history": 60,
                "cg_display_name": "{{ volume_display_name }}",
                "cg_name": "{{ cg_name }}",
                "cg_user_created": "NO",
                "created_at": "2015-02-14T00:15:31+00:00",
                "data_copies_capacity": 125,
                "data_type": "File-System",
                "display_name": "{{ volume_display_name }}",
                "encryption": "NO",
                "ext_metering": "NO",
                "has_backup": "NO",
                "has_mirror": "NO",
                "has_snapshots": "YES",
                "images_repo": "NO",
                "lun": null,
                "modified_at": "2015-10-13T13:40:26+00:00",
                "mount_sync": "YES",
                "name": "{{ volume_name }}",
                "nfs_export_path": "{{ volume_export_path }}",
                "nfs_root_squash": "NO",
                "pool_display_name": "poolname",
                "pool_name": "poolname",
                "read_iops_limit": "0",
                "read_mbps_limit": "0",
                "read_only": null,
                "server_name": {{ volume_server_name }},
                "smb_aio_size": 1,
                "smb_dir_create_mask": "0755",
                "smb_export_path": null,
                "smb_file_create_mask": "0744",
                "smb_guest": "NO",
                "smb_map_archive": "NO",
                "smb_only": "NO",
                "smb_windows_acl": "NO",
                "status": "{{ volume_status }}",
                "target": null,
                "tenant_id": 10,
                "thin": "NO",
                "thresholds": null,
                "virtual_capacity": 200,
                "write_iops_limit": "0",
                "write_mbps_limit": "0"
        }'''

def get_json_volume(
        volume_name='volume-0000001',
        volume_display_name='this_volume_display_name',
        cg_name='cg-0000001',
        volume_export_path='10.0.0.10/export',
        volume_server_name='null',
        volume_status='Available' ):
    p = base_json_volume_tmpl
    q = p.replace('{{ volume_name }}', volume_name )
    p = q.replace('{{ volume_display_name }}', volume_display_name )
    q = p.replace('{{ cg_name }}', cg_name )
    p = q.replace('{{ volume_export_path }}', volume_export_path )
    q = p.replace('{{ volume_server_name }}', volume_server_name )
    p = q.replace('{{ volume_status }}', volume_status )
    return p


def get_json_volume_response(
        volume_id='1234567',
        volume_export_path='10.0.0.10/export',
        volume_server_name='null',
        volume_status='Available',
        response_status=0 ):
    return '{ "response": { "status": %d, "volume": %s } }' % ( response_status,
            get_json_volume(
                volume_name='volume-%s' % volume_id,
                volume_display_name='display_name_volume-%s' % volume_id,
                cg_name='cg-%s' % volume_id,
                volume_export_path=volume_export_path,
                volume_server_name=volume_server_name,
                volume_status=volume_status ) )


def get_json_volume_list_response(
        size=1,
        initial_id=1,
        prefix_for_export_path='10.0.0.10/export',
        volume_server_name='null',
        response_status=0 ):
        # volume_status will alternate 'Available', 'In-Use'

    volume_list = []

    for i in range( size ):
        volume_list.append( get_json_volume(
            volume_name='volume-%08d' % i,
            volume_display_name='display_name_volume-%08d' % i,
            cg_name='cg_%08d' % i,
            volume_export_path='%s/volume_%08d' % ( prefix_for_export_path, i ),
            volume_server_name=volume_server_name,
            volume_status= ( 'Available' if i % 2 == 0 else 'In-use' ) ) )

    return '''{
            "response": {
                "status": %d,
                "count": %d,
                "volumes": [ %s ]
            } }''' % ( response_status, size, ','.join( volume_list ) )



