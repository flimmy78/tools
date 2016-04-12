#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class MonitorDataTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.monitor_data,
                          messsage_handler, logger_name)        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.monitor_data, result_success,
                             self.onRunSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.monitor_data, result_fail,
                             self.onRunFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onRunTimeout)             

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.monitor_data)
        param = self.case_manager.getParam()
        control_server = param["control_server"]       
        #level = int(param["monitor_level"])
        task= int(param["task"])
        #request.setUInt(ParamKeyDefine.level, level)
        request.setUInt(ParamKeyDefine.task, task)
        print task
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onRunSuccess(self, msg, session):
        self.clearTimer(session)
        title = []
        value = []
        title.append("task")
        value.append(msg.getUInt(ParamKeyDefine.task))
        title.append("level")
        value.append(msg.getUInt(ParamKeyDefine.level))
        title.append("server")
        value.append(msg.getUInt(ParamKeyDefine.server))
        title.append("cpu_count")
        value.append(msg.getUInt(ParamKeyDefine.cpu_count))
        title.append("cpu_usage")
        value.append(msg.getFloat(ParamKeyDefine.cpu_usage))
        title.append("memory")
        value.append(msg.getUIntArray(ParamKeyDefine.memory))
        title.append("memory_usage")
        value.append(msg.getFloat(ParamKeyDefine.memory_usage))
        title.append("disk_volume")
        value.append(msg.getUIntArray(ParamKeyDefine.disk_volume))
        title.append("disk_usage")
        value.append(msg.getFloat(ParamKeyDefine.disk_usage))
        title.append("disk_io")
        value.append(msg.getUIntArray(ParamKeyDefine.disk_io))
        title.append("network_io")
        value.append(msg.getUIntArray(ParamKeyDefine.network_io))
        title.append("speed")
        value.append(msg.getUIntArray(ParamKeyDefine.speed))
        title.append("timestamp")
        value.append(msg.getString(ParamKeyDefine.timestamp))
        
        #self.info("[%08X]query host info success" % (session.session_id))
        self.info("[%08X]get monitor data success"%
                    (session.session_id))
        print task
        print_one_list(title,value)
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()
        

    def onRunFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]get monitor data fail"%
                  (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onRunTimeout(self, msg, session):
        self.info("[%08X]get monitor data timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()

   
