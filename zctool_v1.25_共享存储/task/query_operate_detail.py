#!/usr/bin/python
import io
import os.path
import os
import logging
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class QueryOperateDetailTask(BaseTask):
    operate_timeout = 10
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.query_operate_detail,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_operate_detail, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_operate_detail, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.query_operate_detail)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        
        target = param["target"]
        level = int(param["level"])
        begin = param["begin"]
        end = param["end"]
        
        request.setString(ParamKeyDefine.target, target)
        request.setUInt(ParamKeyDefine.level, level)
        request.setString(ParamKeyDefine.begin, begin)
        request.setString(ParamKeyDefine.end, end)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onQuerySuccess(self, msg, session):
        self.clearTimer(session)
        title = []
        value = []

        title.append("server_room")
        value.append(msg.getString(ParamKeyDefine.server_room))
        title.append("computer_rack")
        value.append(msg.getString(ParamKeyDefine.computer_rack))
        title.append("node_name")
        value.append(msg.getString(ParamKeyDefine.node_name))
        title.append("cpu_count")
        value.append(msg.getUInt(ParamKeyDefine.cpu_count))        
        title.append("total_memory")
        value.append(msg.getUInt(ParamKeyDefine.total_memory))
        title.append("available_memory")
        value.append(msg.getUInt(ParamKeyDefine.available_memory))
        title.append("total_volume")
        value.append(msg.getUInt(ParamKeyDefine.total_volume))
        title.append("used_volume")
        value.append(msg.getUInt(ParamKeyDefine.used_volume))
        title.append("timestamp")
        value.append(msg.getStringArray(ParamKeyDefine.timestamp))
        title.append("actived")
        value.append(msg.getUInt(ParamKeyDefine.actived))
        title.append("total_cpu_usage")
        value.append(msg.getFloatArray(ParamKeyDefine.total_cpu_usage))             
        title.append("disk_usage")
        value.append(msg.getFloatArray(ParamKeyDefine.disk_usage))
        title.append("memory_usage")
        value.append(msg.getFloatArray(ParamKeyDefine.memory_usage))
        title.append("cpu_seconds")
        value.append(msg.getFloatArray(ParamKeyDefine.cpu_seconds))
        title.append("read_request")
        value.append(msg.getUIntArray(ParamKeyDefine.read_request))
        title.append("read_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.read_bytes))
        title.append("write_request")
        value.append(msg.getUIntArray(ParamKeyDefine.write_request))
        title.append("write_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.write_bytes))
        title.append("io_error")
        value.append(msg.getUIntArray(ParamKeyDefine.io_error))
        title.append("read_speed")
        value.append(msg.getUIntArray(ParamKeyDefine.read_speed))
        title.append("write_speed")
        value.append(msg.getUIntArray(ParamKeyDefine.write_speed))
        title.append("received_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.received_bytes))
        #title.append("received_packets")
        #value.append(msg.getUIntArray(ParamKeyDefine.received_packets))
        #title.append("received_errors")
        #value.append(msg.getUIntArray(ParamKeyDefine.received_errors))
        title.append("received_drop")
        value.append(msg.getUIntArray(ParamKeyDefine.received_drop))
        title.append("sent_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.sent_bytes))
        title.append("sent_packets")
        value.append(msg.getUIntArray(ParamKeyDefine.sent_packets))
        title.append("sent_errors")
        value.append(msg.getUIntArray(ParamKeyDefine.sent_errors))
        title.append("sent_drop")
        value.append(msg.getUIntArray(ParamKeyDefine.sent_drop))
        title.append("received_speed")
        value.append(msg.getUIntArray(ParamKeyDefine.received_speed))
        title.append("sent_speed")
        value.append(msg.getUIntArray(ParamKeyDefine.sent_speed))
        
        self.info("[%08X]query operate detail success" % (session.session_id))
             
        #print_one_result(querydata)
        print_one_list(title,value)
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query operate detail fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query operate detail timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
