#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class NetworkAttachAddressTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.start_host"
        BaseTask.__init__(self, task_type, RequestDefine.network_attach_address,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.network_attach_address, result_success,
                             self.onAttachSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.network_attach_address, result_fail,
                             self.onAttachFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onAttachTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.network_attach_address)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        uuid = param["id"]
        count = int(param["count"])
        request.setString(ParamKeyDefine.uuid, uuid)
        request.setUInt(ParamKeyDefine.count, count)
        self.info("[%08X]request network attach address"%
                       (session.session_id))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onAttachSuccess(self, msg, session):
        self.clearTimer(session)
        
        self.info("[%08X]network attach address success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onAttachFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]network attach address fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onAttachTimeout(self, msg, session):
        self.info("[%08X]network attach address timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
