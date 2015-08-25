#include "module_test_service.h"
#include <util/define.hpp>
#include <boost/format.hpp>

using namespace zhicloud::service;
using namespace zhicloud::transport;
using namespace zhicloud::util;

namespace zhicloud
{
    ModuleTestService::ModuleTestService(const string& service_name, zhicloud::util::ServiceType service_type, const string& domain, const string& ip, const string& group_ip, const uint16_t& group_port)
                        :NodeService(service_type, service_name, domain,ip,5600,200, group_ip, group_port,"0.0" )
                        ,is_wait_respone(false)
                        ,is_test_error(false)
                        ,test_task_idx(0)
    {
        //ctor

    }

    ModuleTestService::~ModuleTestService()
    {
        //dtor
    }

    void ModuleTestService::addTestTask(TestQueryTask& query_task)
    {
            test_tasks.emplace_back(query_task);
    }

    void ModuleTestService::startTest()
    {
        if(false == start())
        {
            logger->info("test service start false!");
            cout << "test service start false!! " << "please chk log file" << endl;
            return;
        }
        logger->info("test service start ok!");
        is_test_error = false;

        int wait_count = 0;
        while(1)
        {
            {
                MutexLock lock(test_mutex);
                 if(connect_node_name.size() > 0)
                 {
                    break;
                 }
            }
            if(wait_count > 50)
            {
                logger->info("test service connect false!");
                cout << "test service connect out of time !! ";
                return;
            }
            usleep(100000);
            wait_count++;
        }

        logger->info(boost::format("test service connect on %s !") % connect_node_name);
        while(!is_test_error)
        {
            if(false == is_wait_respone)
            {
                MutexLock lock(test_mutex);
                //send a message
                if(static_cast<uint32_t>(test_task_idx) >= test_tasks.size())
                {
                        break;  // test over
                }
                cout << "========================" << endl;
               logger->info( "========================");
                logger->info(boost::format("now start [%d] test request!") % test_task_idx);
                cout << "now test for " << test_tasks[test_task_idx].getDesc() << endl;
                zhicloud::transport::AppMessage request_msg;
                if(false  == test_tasks[test_task_idx].tranRequestMsg(request_msg) )
                {
                    is_test_error = true;
                    cout << "have an error! Can not running test!" << endl;
                    break;
                }
                sendMessage(request_msg, connect_node_name);
                is_wait_respone = true;
                wait_count = 0;
            }
            else
            {
                if( wait_count > 1000)
                {
                    logger->info("there i still not receive respone in 1s");
                    cout << "receive respone out of time (more then 1s)"<< endl;
                    break;
                }
            }
            usleep(1000);   // wait for respone;
            ++wait_count;
        }
        if(is_test_error)
        {
            logger->info("test task false !!!!!");
            cout << "test task false !!!!!" << endl;
        }
        else
        {
            logger->info("test task is run over, successed!!!");
            cout << "test task is run over, successed!!!" << endl;
        }
        onStop();
        usleep(500000);
    }

    bool ModuleTestService::onStart()
    {
        logger->info("test service is onstart");
        return true;
    }

    void ModuleTestService::onStop()
    {
        zhicloud::service::NodeService::onStop();
        logger->info("test service is onstop");
        cout << "test service is stop!!" << endl;
        return;
    }

    void ModuleTestService::onChannelConnected(const string& endpoint_name, const ServiceType& service_type, const string& remote_ip, const port_type& remote_port)
    {
        MutexLock lock(test_mutex);
        connect_node_name = endpoint_name;
        logger->info(boost::format("test service now is  connected with %s")%connect_node_name);
    }

    void ModuleTestService::onChannelDisconnected(const string& node_name,  const zhicloud::util::ServiceType& node_type)
    {
    }


    void ModuleTestService::handleResponseMessage(AppMessage& msg, const string& sender)
    {
        MutexLock lock(test_mutex);
        logger->info("receive respone");


        if(static_cast<uint32_t>(test_task_idx) >= test_tasks.size())
        {
                //is_test_error = true;
                return;  // test over
        }
        if(false == test_tasks[test_task_idx].onRespone(msg, sender, *logger))
        {
            is_test_error = true;

            cout << "now test task is quit!!" << endl;
        }

        test_task_idx++;
        is_wait_respone = false;
    }

}
