#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class MigrateHostTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.create_host"
        BaseTask.__init__(self, task_type, RequestDefine.migrate_host,
                          messsage_handler, logger_name)
        
        #stTransport = 2
        #self.addState(stTransport)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.migrate_host, result_success,
                             self.onCreateSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.migrate_host, result_fail,
                             self.onCreateFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onCreateTimeout)        
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.ack, result_any,
                             self.onCreateStart, state_initial)        
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.report, result_any,
                             self.onCreateProgress, state_initial)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.migrate_host)
        param = self.case_manager.getParam()
        control_server = param["control_server"]       
        
        ##build from image
        host = param["host"]
        type = int(param["type"])
        target = param["target"]
        request.setString(ParamKeyDefine.host, host)
        request.setUInt(ParamKeyDefine.type, type)
        request.setString(ParamKeyDefine.target, target)
        self.info("[%08X]request migrate host '%s' to control server '%s'"%
                       (session.session_id, host_name, control_server))
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onCreateSuccess(self, msg, session):
        self.clearTimer(session)

        self.info("[%08X]migrate host success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()
    def onCreateFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]migrate host fail, name '%s'"%
                  (session.session_id, session.target))
        
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onCreateTimeout(self, msg, session):
        self.info("[%08X]migrate host timeout, name '%s'"%
                  (session.session_id, session.target))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()

    def onCreateStart(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]migrate host started"%
                  (session.session_id))
        self.setTimer(session, self.operate_timeout)

    def onCreateProgress(self, msg, session):
        self.clearTimer(session)
        progress = msg.getUInt(ParamKeyDefine.level)
        self.info("[%08X]migrate host process, %d %%"%
                  (session.session_id, progress))
        self.setTimer(session, self.operate_timeout)
