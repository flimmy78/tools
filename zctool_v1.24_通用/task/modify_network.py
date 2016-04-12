#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class ModifyNetworkTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.modify_network,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_network, result_success,
                             self.onModifySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_network, result_fail,
                             self.onModifyFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onModifyTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.modify_network)
        #msg = getRequest(RequestDefine.modify_network)
        param = self.case_manager.getParam()
        uuid = param["uuid"]
        control_server = param["control_server"]
        description = param["description"]
        name = param["name"]
        pool = param["pool"]
        ip = param["ip"]
        iplist = ip.split(';')
        newip = []
        for rg in iplist:
            newip.append(rg.split(','))
        
        option = int(param["option"])
        request.setString(ParamKeyDefine.uuid, uuid)
        request.setString(ParamKeyDefine.name, name)
        request.setString(ParamKeyDefine.description, description)
        request.setString(ParamKeyDefine.pool, pool)
        request.setStringArrayArray(ParamKeyDefine.ip, newip)
        request.setUInt(ParamKeyDefine.option, option)
        self.info("[%08X]request modify network '%s'"%
                       (session.session_id, uuid))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onModifySuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]modify network success"%
                       (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onModifyFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]modify network fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onModifyTimeout(self, msg, session):
        self.info("[%08X]modify network timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
