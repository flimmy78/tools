#!/usr/bin/python

from transaction.transaction_manager import *
from task_type import *
from task_session import *

from add_compute_resource import *
from remove_compute_resource import *
from query_compute_resource import *
from create_host import *
from modify_host import *
from delete_host import *
from start_host import *
from stop_host import *
from reset_host import *
from halt_host import *
from query_host import *
from restart_host import *

from query_iso_image import * 
from upload_iso_image import * 
from modify_iso_image import * 
from delete_iso_image import *

from insert_media import *
from change_media import *
from eject_media import *

from query_disk_image import * 
from modify_disk_image import * 
from delete_disk_image import *
from create_disk_image import *
from query_compute_pool import *
from create_compute_pool import *
from delete_compute_pool import *
from modify_compute_pool import *
from query_compute_pool_detail import *
from query_service import *
from query_service_type import *
from query_service_group import *
from query_host_info import *

#port pool
from query_port_pool import *
from create_port_pool import *
from delete_port_pool import *
from add_port_resource import *
from remove_port_resource import *
from query_port_resource import *

from query_forwarder_summary import *
from query_forwarder import *
from set_forwarder_status import *
from get_forwarder import *

from query_forwarder_group import *
from create_forwarder_group import *
from delete_forwarder_group import *
from create_forwarder import *
from delete_forwarder import *
from attach_forwarder import *
from detach_forwarder import *
from migrate_forwarder import *
# address pool
from query_address_pool import *
from create_address_pool import *
from delete_address_pool import *
from add_address_resource import *
from remove_address_resource import *
from query_address_resource import *


#bind domain
from bind_domain import *
from unbind_domain import *
from query_domain_summary import *
from query_domain_name import *
from get_bound_domain import *

from query_balancer_detail import *
from query_load_balancer import *
from query_balancer_summary import *

from add_forwarder import *
from remove_forwarder import *

#storage pool
from create_storage_pool import *
from modify_storage_pool import *
from delete_storage_pool import *
from query_storage_pool import *
from add_storage_resource import *
from remove_storage_resource import *
from query_storage_resource import *

from start_monitor import *
from stop_monitor import *
#from monitor_data import *
#from monitor_heart_beat import *

#snapshot_pool
from modify_snapshot_pool import *
from query_snapshot_pool import *
from create_snapshot_pool import *
from delete_snapshot_pool import *
from add_snapshot_node import *
from remove_snapshot_node import *
from query_snapshot_node import *

#load_balancer 
from disable_load_balancer import *
from delete_load_balancer import *
from attach_address import *
from detach_address import *
from get_load_balancer import *
from create_load_balancer import *
from add_balancer_node import *
from remove_balancer_node import *
from modify_balancer_node import *
from enable_load_balancer import *

#server
from query_server_room import *
from query_server_rack import *
from query_server import *

#disk
from attach_disk import *
from detach_disk import *

#device
from query_device import *
from create_device import *
from delete_device import *
from modify_device import *

#snapshot
from create_snapshot import *
from delete_snapshot import *
from resume_snapshot import *
from query_snapshot import *

#back up host
from flush_disk_image import *
from query_host_backup import *
from backup_host import *
from resume_host import *

#rule
from add_rule import *
from remove_rule import *
from query_rule import *
#VPC 
from query_network import *
from create_network import *
from modify_network import *
from query_network_detail import *
from start_network import *
from stop_network import *
from delete_network import *
from query_network_host import *
from attach_host import *
from detach_host import *
from network_attach_address import *
from network_detach_address import *
from network_bind_port import *
from network_unbind_port import *


from query_operate_detail import *
from query_service_detail import *
from query_service_summary import *
from query_operate_summary import *
from query_storage_device import *
from add_storage_device import *
from remove_storage_device import *
from enable_storage_device import *
from disable_storage_device import *
from modify_service import *
from enable_service import *
from disable_service import *
from migrate_host import *
#TransactionManager import from :shared\transaction

class TaskManager(TransactionManager):
    min_session_id = 1000
    session_count = 100
    def __init__(self, logger_name, messsage_handler,
                 case_manager, whisper_proxy):
        TransactionManager.__init__(self, logger_name, self.min_session_id,
                                    self.session_count)
        ##add task
        #print "TaskManager->addTask start"
        #add task to TransactionManager.task_map(dictionary)
        #add_compute_resource=125
        self.addTask(add_compute_resource,
                     AddComputeResourceTask(add_compute_resource,
                                            messsage_handler,
                                            case_manager,
                                            logger_name))
        
        self.addTask(remove_compute_resource,
                     RemoveComputeResourceTask(remove_compute_resource,
                                            messsage_handler,
                                            case_manager,
                                            logger_name))

        self.addTask(query_compute_resource,
                     QueryComputeResourceTask(query_compute_resource,
                                            messsage_handler,
                                            case_manager,
                                            logger_name)) 

        self.addTask(create_host,
                     CreateHostTask(create_host,
                                            messsage_handler,
                                            case_manager,
                                            logger_name))

        self.addTask(modify_host,
                     ModifyHostTask(modify_host,
                                            messsage_handler,
                                            case_manager,
                                            logger_name))
        
        self.addTask(delete_host,
                     DeleteHostTask(delete_host,
                                            messsage_handler,
                                            case_manager,
                                            logger_name)) 

        self.addTask(start_host,
                     StartHostTask(start_host,
                                   messsage_handler,
                                   case_manager,
                                   logger_name))
        self.addTask(stop_host,
                     StopHostTask(stop_host,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
		
	self.addTask(reset_host,
                     ResetHostTask(reset_host,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
        self.addTask(query_host,
                     QueryHostTask(query_host,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
        self.addTask(restart_host,
                     RestartHostTask(restart_host,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
        
        self.addTask(query_host_info,
                     QueryHostInfoTask(query_host_info,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))

        self.addTask(halt_host,
                     HaltHostTask(halt_host,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))

        self.addTask(insert_media,
                     InsertMediaTask(insert_media,
                                   messsage_handler,
                                   case_manager,
                                   logger_name))

        self.addTask(change_media,
                     ChangeMediaTask(change_media,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
        self.addTask(eject_media,
                     EjectMediaTask(eject_media,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
        self.addTask(migrate_host,
                     MigrateHostTask(migrate_host,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))

        self.addTask(query_iso_image,
                     QueryISOImageTask(query_iso_image,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
        
        self.addTask(upload_iso_image,
                     UploadISOImageTask(upload_iso_image,
                                        messsage_handler,
                                        case_manager,
                                        whisper_proxy,
                                        logger_name))

        self.addTask(modify_iso_image,
                     ModifyISOImageTask(modify_iso_image,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))

        self.addTask(delete_iso_image,
                     DeleteISOImageTask(delete_iso_image,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))

        self.addTask(query_disk_image,
                     QueryDiskImageTask(query_disk_image,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))

        self.addTask(modify_disk_image,
                     ModifyDiskImageTask(modify_disk_image,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))

        self.addTask(delete_disk_image,
                     DeleteDiskImageTask(delete_disk_image,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))        

        self.addTask(create_disk_image,
                     CreateDiskImageTask(create_disk_image,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))
        self.addTask(query_service,
                     QueryServiceTask(query_service,
                                  messsage_handler,
                                  case_manager,
                                  logger_name))

        self.addTask(query_compute_pool,
                     QueryComputePool(query_compute_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(create_compute_pool,
                     CreateComputePoolTask(create_compute_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(query_port_pool,
                     QueryPortPoolTask(query_port_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(create_port_pool,
                     CreatePortPoolTask(create_port_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(delete_port_pool,
                     DeletePortPoolTask(delete_port_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(add_port_resource,
                     AddPortRescourceTask(add_port_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(remove_port_resource,
                     RemovePortRescourceTask(remove_port_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_port_resource,
                     QueryPortRescourceTask(query_port_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_forwarder_summary,
                     QueryForWarderSummaryTask(query_forwarder_summary,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_forwarder,
                     QueryForWarderTask(query_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_forwarder_group,
                     QueryForwarderGroupTask(query_forwarder_group,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(create_forwarder_group,
                     CreateForwarderGroupTask(create_forwarder_group,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
       
        self.addTask(delete_forwarder_group,
                     DeleteForwarderGroupTask(delete_forwarder_group,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(create_forwarder,
                      CreateForwarderTask(create_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))


        self.addTask(delete_forwarder,
                     DeleteForwarderTask(delete_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(attach_forwarder,
                     AttachForwarderTask(attach_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(detach_forwarder,
                     DetachForwarderTask(detach_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
  
        self.addTask(migrate_forwarder,
                     MigrateForwarderTask(migrate_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(set_forwarder_status,
                     SetForwarderStatusTask(set_forwarder_status,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(get_forwarder,
                     GetForwarderTask(get_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))

        self.addTask(query_address_pool,
                     QueryAddressPoolTask(query_address_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(create_address_pool,
                     CreateAddressPoolTask(create_address_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(delete_address_pool,
                     DeleteAddressPoolTask(delete_address_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(add_address_resource,
                     AddAddressResourceTask(add_address_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(remove_address_resource,
                     RemoveAddressResourceTask(remove_address_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(query_address_resource,
                     QueryAddressResourceTask(query_address_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #bind domain
        self.addTask(bind_domain,
                     BindDomainTask(bind_domain,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(unbind_domain,
                     UnBindDomainTask(unbind_domain,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_domain_summary,
                     QueryDomainSummaryTask(query_domain_summary,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_domain_name,
                     QueryDomainNameTask(query_domain_name,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(get_bound_domain,
                     GetBoundDomainTask(get_bound_domain,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #computer pool
        self.addTask(delete_compute_pool,
                     DeleteComputePoolTask(delete_compute_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(modify_compute_pool,
                     ModifyComputePoolTask(modify_compute_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #balancer
        self.addTask(query_balancer_detail,
                     QueryBalancerDetailTask(query_balancer_detail,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_load_balancer,
                     QueryLoadBalancerTask(query_load_balancer,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_balancer_summary,
                     QueryBalancerSummaryTask(query_balancer_summary,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #forwarder
        self.addTask(add_forwarder,
                     AddForwarderTask(add_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(remove_forwarder,
                     RemoveForwarderTask(remove_forwarder,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #storage_pool
        self.addTask(create_storage_pool,
                     CreateStoragePoolTask(create_storage_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(modify_storage_pool,
                     ModifyStoragePoolTask(modify_storage_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #load_balancer
        self.addTask(disable_load_balancer,
                     DisableLoadBalancerTask(disable_load_balancer,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(delete_load_balancer,
                     DeleteLoadBalancerTask(delete_load_balancer,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(attach_address,
                     AttachAddressTask(attach_address,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(detach_address,
                     DetchAddressTask(detach_address,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(get_load_balancer,
                     GetLoadBalancerTask(get_load_balancer,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(create_load_balancer,
                     CreateLoadBalancerTask(create_load_balancer,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(add_balancer_node,
                     AddBalancerNodeTask(add_balancer_node,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(remove_balancer_node,
                     RemoveBalancerNodeTask(remove_balancer_node,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(modify_balancer_node,
                     ModifyBalancerNodeTask(modify_balancer_node,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(enable_load_balancer,
                     EnableLoadBalancerTask(enable_load_balancer,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #server
        self.addTask(query_server_room,
                     QueryServerRoomTask(query_server_room,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_server_rack,
                     QueryServerRackTask(query_server_rack,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))        
        
        self.addTask(query_server,
                     QueryServerTask(query_server,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #disk
        self.addTask(attach_disk,
                     AttachDiskTask(attach_disk,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(detach_disk,
                     DetachDiskTask(detach_disk,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #storage pool
        self.addTask(delete_storage_pool,
                     DeleteStoragePoolTask(delete_storage_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_storage_pool,
                     QueryStoragePoolTask(query_storage_pool,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(add_storage_resource,
                     AddStorageResourceTask(add_storage_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(remove_storage_resource,
                     RemoveStorageResourceTask(remove_storage_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_storage_resource,
                     QuerystorageResourceTask(query_storage_resource,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(start_monitor,
                     StartMonitorTask(start_monitor,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(stop_monitor,
                     StopMonitorTask(stop_monitor,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #self.addTask(monitor_heart_beat,
                     #MonitorHeartBeatTask(monitor_heart_beat,
                                      #messsage_handler,
                                      #case_manager,
                                      #logger_name))
        
	
	#self.addTask(monitor_data,
                     #MonitorDataTask(monitor_data,
                                      #messsage_handler,
                                      #case_manager,
                                      #logger_name))
        #device
        self.addTask(query_device,
                     QueryDeviceTask(query_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(create_device,
                     CreateDeviceTask(create_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(delete_device,
                     DeleteDeviceTask(delete_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(modify_device,
                     ModifyDeviceTask(modify_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        #snapshot pool
        self.addTask(create_snapshot_pool,
                    CreateSnapshotPoolTask(create_snapshot_pool,
                                        messsage_handler,
                    case_manager,
                    logger_name))
        self.addTask(delete_snapshot_pool,
            DeleteSnapshotPoolTask(delete_snapshot_pool,
                    messsage_handler,
                    case_manager,
                    logger_name))
        self.addTask(add_snapshot_node,
            AddSnapshotNodeTask(add_snapshot_node,
                    messsage_handler,
                    case_manager,
                    logger_name))
        self.addTask(remove_snapshot_node,
            RemoveSnapshotNodeTask(remove_snapshot_node,
                    messsage_handler,
                    case_manager,
                    logger_name))
        self.addTask(query_snapshot_pool,
            QuerySnapshotPoolTask(query_snapshot_pool,
                    messsage_handler,
                    case_manager,
                    logger_name))
        self.addTask(modify_snapshot_pool,
            ModifySnapshotPoolTask(modify_snapshot_pool,
                    messsage_handler,
                    case_manager,
                    logger_name))
        self.addTask(query_snapshot_node,
            QuerySnapshotNodeTask(query_snapshot_node,
                    messsage_handler,
                    case_manager,
                    logger_name))

        #snapshot
        self.addTask(create_snapshot,
                     CreateSnapShotTask(create_snapshot,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(delete_snapshot,
                     DeleteSnapShotTask(delete_snapshot,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))        
        self.addTask(resume_snapshot,
                     ResumeSnapShotTask(resume_snapshot,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(query_snapshot,
                     QuerySnapShotTask(query_snapshot,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(flush_disk_image,
                     FlushDiskimageTask(flush_disk_image,
                                      messsage_handler,
                                      case_manager,
                                      logger_name)) 
                                       
        self.addTask(query_host_backup,
                    QueryHosBackupTask(query_host_backup,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(backup_host,
                    BackupHostTask(backup_host,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(resume_host,
                    ResumeHostTask(resume_host,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(add_rule,
                    AddRuleTask(add_rule,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))

        
        self.addTask(remove_rule,
                    RemoveRuleTask(remove_rule,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        
        self.addTask(query_rule,
                    QueryRuleTask(query_rule,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        
                                    
        self.addTask(query_network,
                    QueryNetworkTask(query_network,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(create_network,
                    CreateNetworkTask(create_network,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        
        self.addTask(query_network_detail,
                    QueryNetworkDetailTask(query_network_detail,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(start_network,
                    StartNetworkTask(start_network,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(stop_network,
                    StopNetworkTask(stop_network,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(delete_network,
                    DeleteNetworkTask(delete_network,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(query_network_host,
                    QueryNetworkHostTask(query_network_host,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(attach_host,
                    AttachHostTask(attach_host,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(detach_host,
                    DetachHostTask(detach_host,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(network_attach_address,
                    NetworkAttachAddressTask(network_attach_address,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(network_detach_address,
                    NetworkDetachAddressTask(network_detach_address,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(network_bind_port,
                    NetworkBindPortTask(network_bind_port,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        self.addTask(network_unbind_port,
                    NetworkUnbindPortTask(network_unbind_port,
                                     messsage_handler,
                                     case_manager,
                                     logger_name))
        
        self.addTask(modify_network,
                    ModifyNetworkTask(modify_network,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
                                    
        self.addTask(query_operate_detail,
                    QueryOperateDetailTask(query_operate_detail,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(query_operate_summary,
                    QueryOperateSummaryTask(query_operate_summary,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(query_service_summary,
                    QueryServiceSummaryTask(query_service_summary,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(query_service_detail,
                    QueryServiceDetailTask(query_service_detail,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))

        self.addTask(query_compute_pool_detail,
                    QueryComputePoolDetailTask(query_compute_pool_detail,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(query_storage_device,
                    QueryStorageDeviceTask(query_storage_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))

        self.addTask(add_storage_device,
                    AddStorageDeviceTask(add_storage_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(remove_storage_device,
                    RemoveStorageDeviceTask(remove_storage_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))

        self.addTask(enable_storage_device,
                    EnableStorageDeviceTask(enable_storage_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(disable_storage_device,
                    DisableStorageDeviceTask(disable_storage_device,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        
        self.addTask(modify_service,
                    ModifyServiceTask(modify_service,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(enable_service,
                    EnableServiceTask(enable_service,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
        self.addTask(disable_service,
                    DisableServiceTask(disable_service,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))
       
        self.addTask(query_service_type,
                    QueryServiceTypeTask(query_service_type,
                                      messsage_handler,
                                      case_manager,
                                      logger_name)) 
        
        self.addTask(query_service_group,
                    QueryServiceGroupTask(query_service_group,
                                      messsage_handler,
                                      case_manager,
                                      logger_name))

    def startTransaction(self, session_id, msg):
      
        if self.session_map.has_key(session_id):
            session = self.session_map[session_id]
    
            #if not session.tasktype:
               # print "start trans fail, session %d not allocated"%(session_id)
               # return
            task_type = session.task_type
     
            if not self.task_map.has_key(task_type):
                print "start trans fail, invalid task %d for session %d"%(
                    task_type, session_id)
                return
            task = self.task_map[task_type]
            task.initialSession(msg, session)
            task.invokeSession(session)
            if session.isFinished():
              self.deallocTransaction(session_id)
    def processMessage(self, session_id, msg):
        if self.session_map.has_key(session_id):
            session = self.session_map[session_id]
            task_type = session.task_type
            #if not self.task_map.has_key(task_type):
             #   self.warn("process trans fail, invalid task %d for session %d"%(
              #      task_type, session_id))
               # return
            task = self.task_map[task_type]
            task.processMessage(msg, session)
            if session.isFinished():
                self.deallocTransaction(session_id)
	
            

	
def createSession(self, session_id):
        """
        create session instance, override by inherited class if necessary
        """
        session = TaskSession(session_id)
        return sessioni
