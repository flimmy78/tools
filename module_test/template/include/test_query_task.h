#ifndef TEST_QUERY_TASK_H
#define TEST_QUERY_TASK_H
//#include "main_query_Info.h"
#include <util/define.hpp>
#include <json/json.h>
#include <transport/app_message.h>
#include <vector>
#include "util/logger.h"
#include "script_var_tab.h"

namespace zhicloud
{

    class TestQueryTask
    {
        public:
            typedef std::vector< std::pair<zhicloud::util::ParamEnum, Json::Value> > ResponeChk;
			/* BEGIN: Added by wangli, 2015/10/26 */
			enum class NextState
			{
			    request = 0,
				event = 1,
				respones = 2,
			};
			/* END:   Added by wangli, 2015/10/26   PN: */
			enum class ValueType
			{
				unknown = 0,
				uint_type=1,
				float_type,
				str_type,

				uint_array,
				float_array,
				str_array,
				uint_array_array,
				float_array_array,
				str_array_array,
			};


            //explicit TestQueryTask(const MainQueryInfo& query_info, Json::Value& test_data, const string& str_task_desc);
            explicit TestQueryTask(ScriptVarTab& vals, const Json::Value& query_desc, Json::Value& test_data, const string& str_task_desc);
            virtual ~TestQueryTask();

            bool isOK() const
            {
                return is_ok;
            }

            const std::string& getErr() const
            {
                return err_info;
            }

            const std::string& getDesc() const
            {
                return task_desc;
            }

			/* BEGIN: Added by wangli, 2015/10/26 */
			bool jumpToWaitRespones() const;
			/* END:   Added by wangli, 2015/10/26   PN: */

            bool tranRequestMsg(zhicloud::transport::AppMessage& request_msg);

            bool onRespone( zhicloud::transport::AppMessage& respone_msg, const string& sender, zhicloud::util::Logger& logger);
			
            bool onEvent( zhicloud::transport::AppMessage& event_msg, const string& sender, zhicloud::util::Logger& logger);

            static ValueType getTypeByDesc(const string& desc);

        protected:
            void action(Json::Value& act, const Json::Value& val, const string& alise_tab,  zhicloud::util::Logger& logger) throw(ExceptionDesc);

        private:
            zhicloud::util::RequestEnum request_id;
            ScriptVarTab&                    var_tabs;
            Json::Value                      js_respone_desc;
            Json::Value                      js_respone_act;     // action for onRespone
            /* BEGIN: Added by wangli, 2015/10/21 */
            Json::Value                      js_event_desc;
            /* END:   Added by wangli, 2015/10/21   PN: */
            Json::Value                      js_request_param;     // test param
            Json::Value                      js_request_param_desc;     // param desc
            ResponeChk                       respone_chk;        // for respone check , now we do nothing with this.

            std::string     task_desc;
            bool            is_ok;
            std::string     err_info;
			/* BEGIN: Added by wangli, 2015/10/26 */
			NextState next_state;
			/* END:   Added by wangli, 2015/10/26   PN: */
    };

}

#endif // TEST_QUERY_TASK_H
