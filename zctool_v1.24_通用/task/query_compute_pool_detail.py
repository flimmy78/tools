#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class QueryComputePoolDetailTask(BaseTask):
    operate_timeout = 10
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.query_compute_pool_detail,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_compute_pool_detail, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_compute_pool_detail, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.query_compute_pool_detail)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        
        uuid = param["uuid"]
        #print uuid
        
        request.setString(ParamKeyDefine.uuid, uuid)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onQuerySuccess(self, msg, session):
       title = []
       value = []
       title.append("name")
       value.append(msg.getString(ParamKeyDefine.name))

       title.append("network_type")
       value.append(msg.getUInt(ParamKeyDefine.network_type))
       
       title.append("network")
       value.append(msg.getString(ParamKeyDefine.network))

       title.append("disk_type")
       value.append(msg.getUInt(ParamKeyDefine.disk_type))

       title.append("disk_source")
       value.append(msg.getString(ParamKeyDefine.disk_source))

       title.append("mode")
       value.append(msg.getUIntArray(ParamKeyDefine.mode))
       
       title.append("path")
       value.append(msg.getString(ParamKeyDefine.path))
       
       title.append("crypt")
       value.append(msg.getString(ParamKeyDefine.crypt))
       self.info("[%08X]query compute pool detail success" % (session.session_id))
            
       #print_one_result(querydata)
       print_one_list(title,value)
       self.case_manager.finishTestCase(TestResultEnum.success)        
       session.finish()
        
    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query compute pool detail fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query compute pool detail timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
