#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class StopNetworkTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.start_host"
        BaseTask.__init__(self, task_type, RequestDefine.stop_network,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.stop_network, result_success,
                             self.onStopSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.stop_network, result_fail,
                             self.onStopFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onStopTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.stop_network)
        param = self.case_manager.getParam()
        #session.target = param["host"]
        control_server = param["control_server"]
        uuid = param["id"]
        request.setString(ParamKeyDefine.uuid, uuid)
        self.info("[%08X]request stop network"%
                       (session.session_id))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onStopSuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]stop network success"%
                       (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onStopFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]stop network fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onStopTimeout(self, msg, session):
        self.info("[%08X]stop network timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
