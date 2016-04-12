#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class QueryNetworkDetailTask(BaseTask):
    operate_timeout = 10
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.query_network_detail,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_network_detail, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_network_detail, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.query_network_detail)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        
        uuid = param["id"]
        #print uuid
        
        request.setString(ParamKeyDefine.uuid, uuid)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onQuerySuccess_bk(self, msg, session):
        self.clearTimer(session)
        name = msg.getString(ParamKeyDefine.name)
        size = msg.getUInt(ParamKeyDefine.size)
        network_address = msg.getString(ParamKeyDefine.network_address)
        netmask = msg.getUInt(ParamKeyDefine.netmask)
        description = msg.getString(ParamKeyDefine.description)
        status = msg.getUInt(ParamKeyDefine.status)
        newstatus = ChangeResuleStatus(status,Status_network)
        ip = msg.getStringArray(ParamKeyDefine.ip)
        self.info("[%08X]query_network_detail SUCCESS"%
                       (session.session_id))
        title = ['Name','Network_address','Status']
        print_test_result(title,name,network_address,newstatus)
        
        self.case_manager.finishTestCase(TestResultEnum.success)   
        session.finish()
        self.clearTimer(session)
    def onQuerySuccess(self, msg, session):
       title = []
       value = []
       title.append("name")
       value.append(msg.getString(ParamKeyDefine.name))

       title.append("size")
       value.append(msg.getUInt(ParamKeyDefine.size))
       
       title.append("network_address")
       value.append(msg.getString(ParamKeyDefine.network_address))

       title.append("netmask")
       value.append(msg.getUInt(ParamKeyDefine.netmask))

       title.append("description")
       value.append(msg.getString(ParamKeyDefine.description))

       title.append("ip")
       value.append(msg.getStringArray(ParamKeyDefine.ip))
       
       status = msg.getUInt(ParamKeyDefine.status)
       newstatus = ChangeResuleStatus(status,Status_network)
       title.append("status")
       value.append(newstatus)            
       
       self.info("[%08X]query network detail success" % (session.session_id))
            
       #print_one_result(querydata)
       print_one_list(title,value)
       self.case_manager.finishTestCase(TestResultEnum.success)        
       session.finish()
        
    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query_network_detail fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query_network_detail timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
