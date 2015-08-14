#ifndef MODULE_TEST_SERVICE_H
#define MODULE_TEST_SERVICE_H

#include <string>
#include <vector>
#include <util/define.hpp>
#include <util/logging.h>
#include <util/define.hpp>
#include <transport/app_message.h>
#include <service/node_service.h>
#include "test_query_task.h"
#include <mutex>
#include <atomic>

namespace zhicloud
{
    class ModuleTestService: public zhicloud::service::NodeService
    {
        public:
            typedef std::vector< TestQueryTask >    TestTasks;
            typedef std::unique_lock<std::mutex>    MutexLock;

            explicit ModuleTestService( const string& service_name, zhicloud::util::ServiceType service_type, const string& domain, const string& ip, const string& group_ip, const uint16_t& group_port);

            virtual ~ModuleTestService();

            void addTestTask(TestQueryTask& query_task);

            void startTest();
        protected:
            virtual bool onStart();
            virtual void onStop();

            virtual void onChannelConnected(const string& endpoint_name, const zhicloud::util::ServiceType& service_type, const string& remote_ip, const port_type& remote_port);
            virtual void onChannelDisconnected(const string& node_name, const zhicloud::util::ServiceType& node_type);

            virtual void handleResponseMessage(zhicloud::transport::AppMessage& msg, const string& sender);

        private:
            string connect_node_name;

            TestTasks               test_tasks;
            std::mutex              test_mutex;
            std::atomic_bool    is_wait_respone;
            std::atomic_bool    is_test_error;
            std::atomic_int       test_task_idx;
    };
}
#endif // MODULE_TEST_SERVICE_H
