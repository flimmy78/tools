#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class QueryRuleTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        ##logger_name = "task.query_service"
        BaseTask.__init__(self, task_type, RequestDefine.query_rule,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_rule, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_rule, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.query_rule)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        target = param["target"]
        request.setString(ParamKeyDefine.target, target)
        #self.info("[%08X]request query address resource in pool'%s'to control server '%s'"%
                       #(session.session_id,pool_uuid, control_server))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onQuerySuccess(self, msg, session):
        self.clearTimer(session)
        ip = msg.getStringArrayArray(ParamKeyDefine.ip)
        mode = msg.getUIntArray(ParamKeyDefine.mode)
        port = msg.getUIntArrayArray(ParamKeyDefine.port)
        self.info("[%08X]query rule SUCCESS"%
                       (session.session_id))
        #show query result
        #nstatus = ChangeResuleStatus(status,Type_mode)
        title = ['IP','port','mode']
        print_test_result(title,ip,port,mode)
        
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query rule FAIL"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query rule TIMEOUT"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
