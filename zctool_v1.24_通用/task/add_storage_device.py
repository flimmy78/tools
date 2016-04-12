#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class AddStorageDeviceTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.add_storage_device"
        BaseTask.__init__(self, task_type, RequestDefine.add_storage_device,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.add_storage_device, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.add_storage_device, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.add_storage_device)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        level = int(param["level"])     
        request.setUInt(ParamKeyDefine.level, level)
        target = param["target"]
        request.setString(ParamKeyDefine.target, target)
        disk_type = int(param["disk_type"])     
        request.setUInt(ParamKeyDefine.disk_type, disk_type)
        #index = param["index"]
        list = param["index"].split(',') 
	index = []
	for unit in list:
	    index.append(int(unit))	
 
        request.setUIntArray(ParamKeyDefine.index, index)
        name = param["name"]
        request.setString(ParamKeyDefine.name, name)
        path = param["path"]
        request.setString(ParamKeyDefine.path, path)
        crypt = param["crypt"]
        request.setString(ParamKeyDefine.crypt, crypt)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onQuerySuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]add storage device success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()    

    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query server rack fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query server rack tiemout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
