#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class ModifySnapshotPoolTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.create_host"
        BaseTask.__init__(self, task_type, RequestDefine.modify_snapshot_pool,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_snapshot_pool, result_success,
                             self.onModifySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_snapshot_pool, result_fail,
                             self.onModifyFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onModifyTimeout)             

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.modify_snapshot_pool)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        snapshot_pool_id = param["snapshot_pool_id"]
        snapshot_pool_name = param["snapshot_pool_name"]

        request.setString(ParamKeyDefine.uuid, snapshot_pool_id)
        request.setString(ParamKeyDefine.name, snapshot_pool_name)
       
        self.info("[%08X]request modify storage pool '%s'('%s') to control server '%s'"%
                       (session.session_id, snapshot_pool_name,snapshot_pool_id, control_server))
        session.target = snapshot_pool_name
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onModifySuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]modify snapshot pool '%s' success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onModifyFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]modify snapshot pool '%s' fail"%
                  (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onModifyTimeout(self, msg, session):
        self.info("[%08X]modify snapshot pool '%s' timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()

   
