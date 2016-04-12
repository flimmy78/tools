#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class AddSnapshotNodeTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.create_host"
        BaseTask.__init__(self, task_type, RequestDefine.add_snapshot_node,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.add_snapshot_node, result_success,
                             self.onRunSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.add_snapshot_node, result_fail,
                             self.onRunFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onRunTimeout)             

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.add_snapshot_node)
        param = self.case_manager.getParam()
        control_server = param["control_server"]       
        snapshot_pool_id = param["snapshot_pool_id"]
        snapshot_pool_name = param["name"]
        
        request.setString(ParamKeyDefine.pool, snapshot_pool_id)
        request.setString(ParamKeyDefine.name, snapshot_pool_name)
       
        self.info("[%08X]request add snapshot node '%s' to snapshot pool '%s'"%
                       (session.session_id, snapshot_pool_name, snapshot_pool_id))
        session.target = snapshot_pool_name
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onRunSuccess(self, msg, session):
        self.clearTimer(session)
        uuid = msg.getString(ParamKeyDefine.uuid)
        self.info("[%08X]add snapshot node success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onRunFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]add snapshot node fail"%
                  (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onRunTimeout(self, msg, session):
        self.info("[%08X]add snapshot node timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()

   
