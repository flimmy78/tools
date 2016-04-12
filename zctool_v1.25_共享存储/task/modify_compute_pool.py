#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *


class ModifyComputePoolTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager

        BaseTask.__init__(self, task_type, RequestDefine.modify_compute_pool,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_compute_pool, result_success,
                             self.onModifyuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_compute_pool, result_fail,
                             self.onModifyFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onModifyTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.modify_compute_pool)
        param = self.case_manager.getParam()
        control_server = param["control_server"] 
        uuid = param["uuid"]
        name = param["name"]
        network = param["network"]
        disk_type = int(param["disk_type"])
        network_type = int(param["network_type"])
        disk_source = param["disk_source"]
        option = int(param["option"])
        path = param["path"]
        crypt = param["crypt"]
        auto_qos = param["auto_qos"]
	thin = param["thin"]
        high_available = param["high_available"]
        mode = []
        if auto_qos:
            mode.append(1)
        else:
            mode.append(0)
        if high_available:
            mode.append(1)
        else:
            mode.append(0)
	if thin:
            mode.append(1)
        else:
            mode.append(0)
        
        #modify_pool = int(param["modify_pool"])
        request.setString(ParamKeyDefine.uuid, uuid)
        request.setString(ParamKeyDefine.name, name)
        request.setUInt(ParamKeyDefine.network_type, network_type)
        request.setString(ParamKeyDefine.network,network)
        request.setUInt(ParamKeyDefine.disk_type, disk_type)
        request.setString(ParamKeyDefine.disk_source,disk_source )
        request.setUInt(ParamKeyDefine.option, option)
        request.setString(ParamKeyDefine.path,path)
        request.setString(ParamKeyDefine.crypt,crypt)
        request.setUIntArray(ParamKeyDefine.mode, mode)
        self.info("[%08X]request modify compute pool to control server '%s'"%
                        (session.session_id, control_server))
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
    def onModifyuccess(self, msg, session):
        self.clearTimer(session)

        self.info("[%08X]modify compute resource success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onModifyFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]modify compute resource fail"%
                  (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onModifyTimeout(self, msg, session):
        self.info("[%08X]modify compute resource timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
