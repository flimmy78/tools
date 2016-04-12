#!/usr/bin/python
import io
import os.path
import os
import logging
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class UploadISOImageTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.create_host"
        BaseTask.__init__(self, task_type, RequestDefine.upload_iso_image,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.upload_iso_image, result_success,
                             self.onCreateSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.upload_iso_image, result_fail,
                             self.onCreateFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onCreateTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.upload_iso_image)
        param = self.case_manager.getParam()
        control_server = param["control_server"]       
        #target = param["target"]
        name = param["name"]
        description = param["description"]
        target = param["target"]
        disk_type = int(param["disk_type"])
        uuid = param["uuid"]
        group = "system"
        user = "akumas"
        request.setString(ParamKeyDefine.name, name)
        request.setString(ParamKeyDefine.description,description)
        request.setString(ParamKeyDefine.target, target)
        request.setUInt(ParamKeyDefine.disk_type, disk_type)
        request.setString(ParamKeyDefine.uuid,uuid)
        request.setString(ParamKeyDefine.group, group)
        request.setString(ParamKeyDefine.user, user)
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
    def onCreateSuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]upload iso image success"%
                       (session.session_id))

        self.case_manager.finishTestCase(TestResultEnum.success)
        session.finish()
    def onCreateFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]upload iso image fail"%
                  (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onCreateTimeout(self, msg, session):
        self.info("[%08X]upload iso image timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()

