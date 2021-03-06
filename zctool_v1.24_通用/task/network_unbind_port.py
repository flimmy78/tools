#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class NetworkUnbindPortTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.start_host"
        BaseTask.__init__(self, task_type, RequestDefine.network_unbind_port,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.network_unbind_port, result_success,
                             self.onDetachSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.network_unbind_port, result_fail,
                             self.onDetachFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onDetachTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.network_unbind_port)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        uuid = param["id"]
        port = param["port"]
        portlist = port.split(';')
        newport = []
        #newport = [[i for i in portlist]] 
        for rg in portlist:
            newport.append(rg.split(','))
        request.setString(ParamKeyDefine.uuid, uuid)
        request.setStringArrayArray(ParamKeyDefine.port, newport)
        #setStringArrayArray(msg, 16, [["hello", ""], ["akumas"],["zhi", "cloud"]])
        #setStringArrayArray(msg, [ParamKeyDefine.port, newport])
        self.info("[%08X]request network unbind port"%
                       (session.session_id))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
        
        
    def onDetachSuccess(self, msg, session):
        self.clearTimer(session)
        
        self.info("[%08X]network unbind port success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onDetachFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]network unbind port fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onDetachTimeout(self, msg, session):
        self.info("[%08X]network unbind port timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
