#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class NetworkDetachAddressTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.start_host"
        BaseTask.__init__(self, task_type, RequestDefine.network_detach_address,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.network_detach_address, result_success,
                             self.onDetachSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.network_detach_address, result_fail,
                             self.onDetachFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onDetachTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.network_detach_address)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        uuid = param["id"]
        ip = param["ip"]
        iplist = ip.split(',')
        newip = []
        for rg in iplist:
            newip.append(rg)	
        request.setString(ParamKeyDefine.uuid, uuid)
        request.setStringArray(ParamKeyDefine.ip, newip)
        self.info("[%08X]request network detach address"%
                       (session.session_id))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onDetachSuccess(self, msg, session):
        self.clearTimer(session)
        
        self.info("[%08X]network detach address success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onDetachFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]network detach address fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onDetachTimeout(self, msg, session):
        self.info("[%08X]network detach address timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
