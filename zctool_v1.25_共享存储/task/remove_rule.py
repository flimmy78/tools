#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class RemoveRuleTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.remove_compute_resource"
        BaseTask.__init__(self, task_type, RequestDefine.remove_rule,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.remove_rule, result_success,
                             self.onRemoveSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.remove_rule, result_fail,
                             self.onRemoveFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onRemoveTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.remove_rule)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        target = param["target"]        
        mode = int(param["mode"])
        ip = param["ip"]
        port = param["port"]
        iplist = ip.split(',')
        portlist = port.split(',')
        newport = []
        for rg in portlist:
            newport.append(int(rg))
        
        request.setString(ParamKeyDefine.target, target)
        request.setUInt(ParamKeyDefine.mode, mode)        
        request.setStringArray(ParamKeyDefine.ip, iplist)
        request.setUIntArray(ParamKeyDefine.port, newport)
        self.info("[%08X]request add rule to control server"%
                       (session.session_id))
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        

    def onRemoveSuccess(self, msg, session):
        self.clearTimer(session)

        self.info("[%08X]remove rule success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onRemoveFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]remove rule fail"%
                  (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onRemoveTimeout(self, msg, session):
        self.info("[%08X]remove rule timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
