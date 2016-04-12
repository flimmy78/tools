#! /usr/bin/env python
#coding=utf-8

All_help = """
"help + command name" to show the full introduction.
command list:
ISO image Management(help keyword 'isoimage')
    query_iso_image                 query all iso images information.
    modify_iso_image                modify iso image parameter.
    delete_iso_image                delete a iso image.
    upload_iso_image                upload a iso image to platform.

Disk image Management(help keyword 'diskimage')
    query_disk_image                query all disk images information.
    create_disk_image               create a new disk image from a exist host.
    modify_disk_image               modify a disk image.
    delete_disk_image               delete a exist disk image.
    
Host Management(help keyword 'host')
    query_host                      query hosts from a computer pool.
    query_host_info                 query a host full information.
    create_host                     create a new host.
    start_host                      start a host.
    stop_host                       stop a host.
    restart_host                    restart a host.
    halt_host                       host a host.
    reset_host                      reset a host.
    delete_host                     delete a host.
    modify_host                     modify a host parameter.
    
Service Management (help keyword 'service')
    query_service                   query service status.
    
Compute pool Management(help keyword 'compute')
    query_compute_pool              query all compute pool information.
    query_compute_resource          query compute pool resource.
    create_compute_pool             create a new compute pool.
    delete_compute_pool             delete a exist compute pool.
    modify_compute_pool             modify a exist compute pool.
    add_compute_resource            add the node_client to compute pool.
    remove_compute_resource         remove a node_client from a compute pool.
    
Address pool Management (help keyword 'address')
    query_address_pool              query address pool data.
    create_address_pool             create a new address pool.
    delete_address_pool             delete a address pool.
    query_address_resource          query the ips of address pool.
    add_address_resource            add ips to the address pool.
    remove_address_resource         remove the ip from address pool.
    

Port pool Management(help keyword 'port')
    create_port_pool                create a new port pool.
    delete_port_pool                delete a exist port pool.
    query_port_resource             query a port pool resource.
    add_port_resource               add a ip list to port pool.
    remove_port_resource            remove a ip list to port pool.
    
Storage pool Management(help keyword 'storage')
    query_storage_pool              query storage pool data.
    create_storage_pool             create a storage pool.
    modify_storage_pool             modify a storage pool.
    delete_storage_pool             delete a storage pool.
    query_storage_resource          query storage pool resource.
    add_storage_resource            add the data_node to storage pool.
    remove_storage_resource         remove the data_node from storage pool.
    
Forwarder Management(help keyword 'forwarder')
    query_forwarder                 query host forwarder.
    add_forwarder                   add a forwarder to a host.
    remove_forwarder                remove a forwarder from a host.
    set_forwarder_status            set the forwarder status.
    get_forwarder                   read the forwarder configure.
    
Disk Management(help keyword 'disk')
    attach_disk                     attach a disk to host.
    detach_disk                     detach a disk from host.
    
Device Management(help keyword 'device')
    query_device                    query storage device.
    create_device                   create a new device.
    delete_device                   delete a exist device.
    modify_device                   modify a device parameter.
    
Snapshot Management (help keyword 'snapshot')
    create_snapshot_pool            
    query_snapshot                  query snapshot.
    create_snapshot                 create a new snapshot.
    delete_snapshot                 delete a snapshot.
    resume_snapshot                 resume a snapshot to create time.

"""

ISO_HELP = """
ISO image Management(help keyword 'isoimage')
    query_iso_image                 query all iso images information.
    modify_iso_image                modify iso image parameter.
    delete_iso_image                delete a iso image.
    upload_iso_image                upload a iso image to platform.
    
"""
