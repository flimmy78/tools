#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class ChangeMediaTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        logger_name = "task.change_media"
        BaseTask.__init__(self, task_type, RequestDefine.change_media,
                          messsage_handler, logger_name)
        #stTransport = 2
        #self.addState(stTransport)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.change_media, result_success,
                             self.onDeleteSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.change_media, result_fail,
                             self.onDeleteFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onDeleteTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.change_media)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        uuid = param["uuid"]
        image = param["image"]
        request.setString(ParamKeyDefine.uuid, uuid)
        request.setString(ParamKeyDefine.image, image)
        self.info("[%08X]request  insert media to control server '%s'"%
                        (session.session_id, control_server))
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onDeleteSuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]change media success"%
                       (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onDeleteFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]change media fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onDeleteTimeout(self, msg, session):
        self.info("[%08X]change media timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
