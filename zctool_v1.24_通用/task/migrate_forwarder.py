#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class MigrateForwarderTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.add_storage_device"
        BaseTask.__init__(self, task_type, RequestDefine.migrate_forwarder,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.migrate_forwarder, result_success,
                             self.onCreateSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.migrate_forwarder, result_fail,
                             self.onCreateFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onCreateTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.migrate_forwarder)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        uuid = param["uuid"]
        request.setString(ParamKeyDefine.uuid,uuid)
        target = param["target"]
        request.setString(ParamKeyDefine.target,target)
        ip = param["ip"].split(',')
        request.setStringArray(ParamKeyDefine.ip,ip)
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onCreateSuccess(self, msg, session):
        self.clearTimer(session)
        uuid = msg.getString(ParamKeyDefine.uuid)
        self.info("[%08X]migrate_forwarder success"%
                       (session.session_id,uuid))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()    

    def onCreateFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]migrate_forwarder fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onCreateTimeout(self, msg, session):
        self.info("[%08X]migrate_forwarder tiemout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
