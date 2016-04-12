#! /usr/bin/env python
#coding=utf-8

All_help = """
"help + command name" to show the full introduction.
command list:
Address pool Management (help keyword 'address')
    query_address_pool              query address pool data.
    create_address_pool             create a new address pool.
    delete_address_pool             delete a address pool.
    query_address_resource          query the ips of address pool.
    add_address_resource            add ips to the address pool.
    remove_address_resource         remove the ip from address pool.

Bind management(help keyword 'bind')
    bind_domain                     bind a host or balancer domain.
    unbind_domain                   unbind a host or balancer from domain.
    query_domain_name               query domain name.
    get_bound_domain                get domain name.


Compute pool Management (help keyword 'compute')
    query_compute_pool_detail       query all compute pool information.
    query_compute_resource          query compute pool resource.
    create_compute_pool             create a new compute pool.
    delete_compute_pool             delete a exist compute pool.
    modify_compute_pool             modify a exist compute pool.
    add_compute_resource            add the node_client to compute pool.
    remove_compute_resource         remove a node_client from a compute pool.

Device management(help keyword 'device')
    query_device                    query storage device.
    create_device                   create a new device.
    delete_device                   delete a exist device.
    modify_device                   modify a device parameter.


Disk image Management(help keyword 'diskimage')
    query_disk_image                query all disk images information.
    create_disk_image               create a new disk image from a exist host.
    modify_disk_image               modify a disk image.
    delete_disk_image               delete a exist disk image.
    flush_disk_image                flush a disk image.

Disk management(help keyword 'disk')
    attach_disk                     attach a disk to host.
    detach_disk                     detach a disk from host.
    
Forwarder management(help keyword 'forwarder')
    query_forwarder                 query host forwarder.
    add_forwarder                   add a forwarder to a host.
    remove_forwarder                remove a forwarder from a host.
    set_forwarder_status            set the forwarder status.
    get_forwarder                   read the forwarder configure.

Host management(help keyword 'host')
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
    backup_host                     backup a host.
    resume_host                     resume host when running.
    query_host_backup               query a host backup.
    attach_host                     attach a host to VPC.
    detach_host                     detach the host from VPC.

ISO image management(help keyword 'isoimage')
    query_iso_image                 query all iso images information.
    modify_iso_image                modify iso image parameter.
    delete_iso_image                delete a iso image.
    upload_iso_image                upload a iso image to platform.

Load balancer Management(help keyword 'balancer')
    enable_load_balancer            enable a load balancer.
    disable_load_balancer           disable a load balancer.
    delete_load_balancer            delete a load balancer.
    attach_address                  attach an IP to load_balancer 
    detach_address                  detach a IP from load_balancer.
    get_load_balancer               get load balancer information.
    query_load_balancer             query load balancer information.
    query_balancer_detail           query load balancer information.
    create_load_balancer            create a load balancer.
    add_balancer_node               add a balancer node.
    remove_balancer_node            remove a balancer node.
    modify_balancer_node            modify a balancer node.
    
Monitor management(help keyword 'monitor')    
    start_monitor                   start monitor.
    stop_monitor                    stop monitor.
    monitor_heart_beat              monitor heart beat.
    monitor_data                    monitor data.

Network management (help keyword 'network') #VPC
    create_network                  create a VPC network.
    modify_network                  modify a VPC network.
    query_network_detail            query a VPC network detail information.
    start_network                   start a VPC network.
    stop_network                    stop a VPC network.
    delete_network                  delete a VPC network.
    query_network_host              query a host from VPC.
    network_attach_address          attach VPC address to host.
    network_detach_address          detach the VPC address from host.
    network_bind_port               bind a port to VPC host. 
    network_unbind_port             unbind a port from VPC host.
    
    query_operate_detail            query the VPC host operation logs detail.
    query_operate_summary           query the VPC host operation logs summary.

Port pool Management(help keyword 'port')
    create_port_pool                create a new port pool.
    delete_port_pool                delete a exist port pool.
    query_port_resource             query a port pool resource.
    add_port_resource               add a ip list to port pool.
    remove_port_resource            remove a ip list to port pool.

Rule management (help keyword 'rule')
    add_rule                        add a rule.
    remove_rule                     remove a rule.
    query_rule                      query a rule.

Server management (help keyword 'server')
    query_server                    query a server information.
    query_server_rack               query a server rack.

Service management (help keyword 'service')
    query_service                   query service status.
    query_service_detail            query the service operation logs.
    query_service_summary           query summary of service operation logs.
    modify_service
    
Snapshot management (help keyword 'snapshot')
    create_snapshot_pool 
    modify_snapshot_pool            modify an existed snapshot pool.
    delete_snapshot_pool            delete an existed snapshot pool.
    query_snapshot_node             query the node snapshot pool.
    add_snapshot_node               add snapshot node.
    remove_snapshot_node            remove snapshot node.
    query_snapshot                  query snapshot.
    create_snapshot                 create a new snapshot.
    delete_snapshot                 delete a snapshot.
    resume_snapshot                 resume a snapshot to create time.

Storage pool management(help keyword 'storage')
    query_storage_pool              query storage pool data.
    create_storage_pool             create a storage pool.
    modify_storage_pool             modify a storage pool.
    delete_storage_pool             delete a storage pool.
    query_storage_resource          query storage pool resource.
    add_storage_resource            add the data_node to storage pool.
    remove_storage_resource         remove the data_node from storage pool.
    query_storage_device            query storage device.
    add_storage_device              add a storage device.
    remove_storage_device           remove a storage device.
    enable_storage_device           enable storage device.
    disable_storage_device          disable storage device.               

"""



Address_Help = """
	Address pool Management (help keyword 'address')
    query_address_pool              query address pool data.
    create_address_pool             create a new address pool.
    delete_address_pool             delete a address pool.
    query_address_resource          query the ips of address pool.
    add_address_resource            add ips to the address pool.
    remove_address_resource         remove the ip from address pool.
"""

Bind_Help = """
Bind management(help keyword 'bind')
    bind_domain                     bind a host or balancer domain.
    unbind_domain                   unbind a host or balancer from domain.
    query_domain_name               query domain name.
    get_bound_domain                get domain name.
"""

Compute_pool_Help = """
Compute pool Management (help keyword 'compute')
    query_compute_pool              query a compute information.
    query_compute_pool_detail       query all compute pool information.
    query_compute_resource          query compute pool resource.
    create_compute_pool             create a new compute pool.
    delete_compute_pool             delete a exist compute pool.
    modify_compute_pool             modify a exist compute pool.
    add_compute_resource            add the node_client to compute pool.
    remove_compute_resource         remove a node_client from a compute pool.
"""

Device_Help = """
Device management(help keyword 'device')
    query_device                    query storage device.
    create_device                   create a new device.
    delete_device                   delete a exist device.
    modify_device                   modify a device parameter.
"""

Disk_image_Help = """
Disk image Management(help keyword 'diskimage')
    query_disk_image                query all disk images information.
    create_disk_image               create a new disk image from a exist host.
    modify_disk_image               modify a disk image.
    delete_disk_image               delete a exist disk image.
    flush_disk_image                flush a disk image.
"""

Disk_Help = """
Disk management(help keyword 'disk')
    attach_disk                     attach a disk to host.
    detach_disk                     detach a disk from host.
"""

Forwarder_Help = """    
Forwarder management(help keyword 'forwarder')
    query_forwarder                 query host forwarder.
    add_forwarder                   add a forwarder to a host.
    remove_forwarder                remove a forwarder from a host.
    set_forwarder_status            set the forwarder status.
    get_forwarder                   read the forwarder configure.
"""

Host_Help = """
Host management(help keyword 'host')
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
    backup_host                     backup a host.
    resume_host                     resume host when running.
    query_host_backup               query a host backup.
    attach_host                     attach a host to VPC.
    detach_host                     detach the host from VPC.
"""

ISO_Help = """
ISO image management(help keyword 'isoimage')
    query_iso_image                 query all iso images information.
    modify_iso_image                modify iso image parameter.
    delete_iso_image                delete a iso image.
    upload_iso_image                upload a iso image to platform.
"""

Load_balancer_Help = """
Load balancer Management(help keyword 'balancer')
    enable_load_balancer            enable a load balancer.
    disable_load_balancer           disable a load balancer.
    delete_load_balancer            delete a load balancer.
    attach_address                  attach an IP to load_balancer 
    detach_address                  detach a IP from load_balancer.
    get_load_balancer               get load balancer information.
    query_load_balancer             query load balancer information.
    query_balancer_detail           query load balancer information.
    create_load_balancer            create a load balancer.
    add_balancer_node               add a balancer node.
    remove_balancer_node            remove a balancer node.
    modify_balancer_node            modify a balancer node.
"""

Monitor_Help = """   
Monitor management(help keyword 'monitor')    
    start_monitor                   start monitor.
    stop_monitor                    stop monitor.
    monitor_heart_beat              monitor heart beat.
    monitor_data                    monitor data.
"""

Network_Help = """
Network management (help keyword 'network') #VPC
    create_network                  create a VPC network.
    modify_network                  modify a VPC network.
    query_network_detail            query a VPC network detail information.
    start_network                   start a VPC network.
    stop_network                    stop a VPC network.
    delete_network                  delete a VPC network.
    query_network_host              query a host from VPC.
    network_attach_address          attach VPC address to host.
    network_detach_address          detach the VPC address from host.
    network_bind_port               bind a port to VPC host. 
    network_unbind_port             unbind a port from VPC host.
    
    query_operate_detail            query the VPC host operation logs detail.
    query_operate_summary           query the VPC host operation logs summary.
"""

Port_pool_Help = """
Port pool Management(help keyword 'port')
    create_port_pool                create a new port pool.
    delete_port_pool                delete a exist port pool.
    query_port_resource             query a port pool resource.
    add_port_resource               add a ip list to port pool.
    remove_port_resource            remove a ip list to port pool.
"""

Rule_Help = """
Rule management (help keyword 'rule')
    add_rule                        add a rule.
    remove_rule                     remove a rule.
    query_rule                      query a rule.
"""

Server_Help = """
Server management (help keyword 'server')
    query_server                    query a server information.
    query_server_rack               query a server rack.
"""

Service_Help = """
Service management (help keyword 'service')
    query_service                   query service status.
    query_service_detail            query the service operation logs.
    query_service_summary           query summary of service operation logs.
    modify_service
"""

Snapshot_Help = """   
Snapshot management (help keyword 'snapshot')
    create_snapshot_pool 
    modify_snapshot_pool            modify an existed snapshot pool.
    delete_snapshot_pool            delete an existed snapshot pool.
    query_snapshot_node             query the node snapshot pool.
    add_snapshot_node               add snapshot node.
    remove_snapshot_node            remove snapshot node.
    query_snapshot                  query snapshot.
    create_snapshot                 create a new snapshot.
    delete_snapshot                 delete a snapshot.
    resume_snapshot                 resume a snapshot to create time.
"""

Storage_pool_Help = """
Storage pool management(help keyword 'storage')
    query_storage_pool              query storage pool data.
    create_storage_pool             create a storage pool.
    modify_storage_pool             modify a storage pool.
    delete_storage_pool             delete a storage pool.
    query_storage_resource          query storage pool resource.
    add_storage_resource            add the data_node to storage pool.
    remove_storage_resource         remove the data_node from storage pool.
    query_storage_device            query storage device.
    add_storage_device              add a storage device.
    remove_storage_device           remove a storage device.
    enable_storage_device           enable storage device.
    disable_storage_device          disable storage device.               
"""
