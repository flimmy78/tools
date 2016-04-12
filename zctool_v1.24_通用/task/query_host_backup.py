#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class QueryHosBackupTask(BaseTask):
    operate_timeout = 10
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.query_host_backup,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_host_backup, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_host_backup, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.query_host_backup)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        
        uuid = param["uuid"]
        #print host_id
        
        request.setString(ParamKeyDefine.uuid, uuid)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onQuerySuccess_bk(self, msg, session):
        self.clearTimer(session)
        querydata = {}        
        querydata["disk_volume"] = msg.getUIntArray(ParamKeyDefine.disk_volume)
        
        querydata["timestamp"] = msg.getStringArray(ParamKeyDefine.timestamp)
        querydata["index"] = msg.getUIntArray(ParamKeyDefine.index)
 
        self.info("[%08X]query host info success" % (session.session_id))
             
        print_one_result(querydata)
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onQuerySuccess(self, msg, session):
        self.clearTimer(session)
        title = []
        value = []

        title.append("disk_volume")
        value.append(msg.getUIntArray(ParamKeyDefine.disk_volume))

        title.append("timestamp")
        value.append(msg.getStringArray(ParamKeyDefine.timestamp))
        title.append("index")
        value.append(msg.getUIntArray(ParamKeyDefine.index))
        self.info("[%08X]query_host_backup success" % (session.session_id))
             
        #print_one_result(querydata)
        print_one_list(title,value)
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query_host_backup fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query_host_backup timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
