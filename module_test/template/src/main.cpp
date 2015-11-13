#include <iostream>
#include <util/logging.h>
#include <util/define.hpp>
#include <transport/app_message.h>
#include <transport/transport.hpp>
#include "boost/bind.hpp"
#include "module_test_service.h"
#include <boost/format.hpp>
#include <json/json.h>
#include <fstream>
//#include "main_query_Info.h"
#include "test_query_task.h"
#include <sstream>
#include <unistd.h>
 #include <getopt.h>
 #include "name_trans.h"

using namespace std;

// I for int, F for double, S for string, A for array, O for object
bool chk_json_data(Json::Value& oRCData, const char* strCFmt, string& strCErr)
{
	if(NULL == strCFmt) return false;
	string oTmpData = strCFmt;
	const char* pCur = strCFmt;
	while(*pCur)
	{
		const char* pNext = strstr(pCur, ";");
		int nSize = 0;
		if(nullptr == pNext)
		{
			nSize = strlen(pCur);
		}
		else
		{
			nSize = pNext-pCur+1;
		}
		const char* pMark = strstr(pCur, ":");
		if(nullptr == pMark)
            return false;
		//*pMark = '\0';
		//++pMark;
		oTmpData.clear();
		oTmpData.append(pCur, pMark - pCur);
		if(false == oRCData.isMember(oTmpData))
		{
			strCErr += "Miss param \"";
			strCErr += oTmpData;
			strCErr += "\" !!";
			return false;
		}
		pMark++;
		switch(*pMark)
		{
		case 'I':
			if(false == oRCData[oTmpData].isIntegral())
			{
				strCErr += "Bad param \"";
				strCErr += oTmpData;
				strCErr += "\" type need long";
				return false;
			}
			break;
		case 'S':
			if(false == oRCData[oTmpData].isString())
			{
				strCErr += "Bad param \"";
				strCErr += oTmpData;
				strCErr += "\" type need string!!";
				return false;
			}
			break;
		case 'F':
			if(false == oRCData[oTmpData].isDouble())
			{
				strCErr += "Bad param \"";
				strCErr += oTmpData;
				strCErr += "\" type need float!!";
				return false;
			}
			break;
        case 'A':
			if(false == oRCData[oTmpData].isArray())
			{
				strCErr += "Bad param \"";
				strCErr += oTmpData;
				strCErr += "\" type need array!!";
				return false;
			}
			break;
        case 'O':
			if(false == oRCData[oTmpData].isObject())
			{
				strCErr += "Bad param \"";
				strCErr += oTmpData;
				strCErr += "\" type need object!!";
				return false;
			}
			break;
		default:
			//TRACE0("unknow mark!!!");
			strCErr += "use unknown param type!!";
			return false;
			break;
		}
		pCur += nSize;
	}
	return true;
}

using namespace zhicloud;
using namespace zhicloud::util;


struct option opts[] = {
    {"config",  required_argument, NULL, 'f'},
    {"test",  required_argument, NULL, 't'},
    {"help",    no_argument,       NULL, 'h'},
    {"version", no_argument,       NULL, 'v'}
};

ScriptVarTab    val_map;

int main(int argc, char** argv)
{
    string  str_config_file = "module_test.conf";
    string  str_module_test_file;
    int32_t opt = 0;
    while ((opt = getopt_long(argc, argv, "f:t:hv", opts, NULL)) != -1) {
        switch (opt) {
        case 'f':
            str_config_file = optarg;
            break;
        case 't':
            str_module_test_file = optarg;
            break;
        case 'h':
            cout <<"Usage: ./module_test -hv | [-f configure_file] -t test_file" << endl;
            cout <<" -f --config     configure file default value is \"module_test.conf\""<< endl;
            cout <<" -t --test         module test file"<< endl;
            cout <<" -h --help       help information"<< endl;
            cout <<" -v --version    help information" << endl;
            return 0;
        case 'v':
            cout << "version 1.0.0"<<endl;
            return 0;
        default:
            cout <<"Usage: ./module_test -hv | [-f configure_file] -t test_file" << endl;
            cout <<" -f --config     configure file default value is \"module_test.conf\""<< endl;
            cout <<" -t --test         module test file"<< endl;
            cout <<" -h --help       help information"<< endl;
            cout <<" -v --version    help information" << endl;
            return -1;
        }
    }

    if(str_module_test_file.size() == 0)
    {
        cout << "operator error, must use -t or --test to define module test file!"<<endl;
        return 0;
    }

    ifstream config_file(str_config_file, std::ifstream::in);
    if(!config_file)
    {
        cout << "configure file " << str_config_file << " open false !" << endl;
        return 0;
    }
    Json::Reader jsRead(Json::Features::strictMode());
    Json::Value config_root;
    if(false == jsRead.parse(config_file,config_root))
    {
            cout<< str_config_file << "  json parse err!" << endl;
            cout << jsRead.getFormatedErrorMessages() << endl;
            return 0;
    }


    ifstream module_test_file(str_module_test_file, std::ifstream::in);
    if(!module_test_file)
    {
        cout << "module test file " << str_module_test_file << " open false !" << endl;
        return 0;
    }
    Json::Value test_root;
    if(false == jsRead.parse(module_test_file,test_root))
    {
            cout<< str_module_test_file << "  json parse err!" << endl;
            cout << jsRead.getFormatedErrorMessages() << endl;
            return 0;
    }

    initialLogging();
    addFileAppender("/var/zhicloud/log", "module_test_info", 4096000);
    // check json menber
    if(false == config_root.isMember("locale") || false == config_root["locale"].isObject())
    {
        cout<< "miss \"locale\" item in json!" << endl;
        cout<< "you must configure like \"locale\":{\"ip\":\"192.168.0.100\",\"domain\":\"zhiyun\", \"group_ip\":\"224.6.6.6\",\"group_port\":5666} !" << endl;
        return 0;
    }
    Json::Value& locale_node = config_root["locale"];


    string ip, domain, group_ip;
    int group_port;
    string err_info;
    if(false == chk_json_data(locale_node,"ip:S;domain:S;group_ip:S;group_port:I;test_service_type:S", err_info))
    {
        cout<< "\"locale\" item error:" << err_info << endl;
        return 0;
    }

    std::string test_service_type = locale_node["test_service_type"].asString();
    ip = locale_node["ip"].asString();
    domain = locale_node["domain"].asString();
    group_ip = locale_node["group_ip"].asString();
    group_port = locale_node["group_port"].asInt();

    if(false == config_root.isMember("trans") || false == config_root["trans"].isObject())
    {
         cout<< "\"trans\" item must be configure, need \"param\" item to trans vaule" << endl;
         return 0;
    }
    init_name_trans(config_root["trans"]);
    auto test_service_trans = get_name_trans()("service", test_service_type);
    if(false == test_service_trans.first)
    {
        cout << " in configure file, not found \"" << test_service_type << "\" in trans/service item!";
        return false;
    }

    if(false == config_root.isMember("request_desc") || false == config_root["request_desc"].isObject())
    {
         cout<< "\"request_desc\" item must be configure, need \"request_desc\" item to trans test task" << endl;
         return 0;
    }

    Json::Value& js_request_desc = config_root["request_desc"];
    // check all desc
    for(auto& name : js_request_desc.getMemberNames())
    {
        Json::Value& js_item = js_request_desc[name];
        if(false == chk_json_data(js_item,"code:I;param_list:O;respone_list:O", err_info))
        {
            cout<< "qurey  "<<  name << "desc  error:" << err_info << endl;
            cout << "please check " << config_file << endl;
            return 0;
        }
        for(auto& list_name : js_item.getMemberNames())
        {

			//cout<<"wangli test list_name is "<<list_name<<endl;
            if(list_name != "param_list" && list_name != "respone_list" && list_name != "event_list")
            {
            	//cout<<"wangli test 2     !!!!!"<<endl;
                continue;
            }
            Json::Value& js_params = js_item[list_name];

			//cout<<"wangli test 55555!!!!!"<<endl;
            for(auto& param_name : js_params.getMemberNames())
            {
                auto rtn = get_name_trans()("param", param_name);
                if(rtn.first == false)
                {
                    cout<< "qurey "<<  name << " param " << param_name << "  not found!" << endl;
                    cout << "please check " << config_file << endl;
                    return 0;
                }
                Json::Value& js_param_item = js_params[param_name];
                if(false == chk_json_data(js_param_item,"data_type:S", err_info))
                {
                    cout<< "qurey "<<  name << " param " << param_name << "  err :" << err_info << endl;
                    cout << "please check " << config_file << endl;
                    return 0;
                }
                auto vtype = TestQueryTask::getTypeByDesc(js_param_item["data_type"].asString());
                if(vtype == TestQueryTask::ValueType::unknown)
                {
                    cout<< "qurey "<<  name << " param " << param_name << "  data_type not supply!" << endl;
                    cout << "please check " << config_file << endl;
                    return 0;
                }
                if(js_param_item.isMember("trans_tab") )
                {
                    if(false == js_param_item["trans_tab"].isString())
                    {
                        cout<< "qurey "<<  name << " param " << param_name << "  trans_tab must be string" << endl;
                        cout << "please check " << config_file << endl;
                        return 0;
                    }
                    if(false == config_root["trans"].isMember( js_param_item["trans_tab"].asString()))
                    {
                        cout<< "qurey "<<  name << " param " << param_name << "  trans_tab "  << js_param_item["trans_tab"].asString() << " not found in trans" << endl;
                        cout << "please check " << config_file << endl;
                        return 0;
                    }
                }
				/* BEGIN: Added by wangli, 2015/10/22 */
				if (js_param_item.isMember("optional"))
				{
					//cout<<"wangli optional !!!!!"<<endl;
				    if(false == js_param_item["optional"].isString())
                    {
                        cout<< "qurey "<<  name << " param " << param_name << "  optional must be string" << endl;
                        cout << "please check " << config_file << endl;
                        return 0;
                    }
				}
				/* END:   Added by wangli, 2015/10/22   PN: */
            }
        }
    }

    //make a unique name
    struct timeval timeCur;
    gettimeofday(&timeCur, 0);
    srand(timeCur.tv_usec);
    string service_name = (boost::format("T%d_%d_%04d") %static_cast<int>(timeCur.tv_sec&0xffff) %static_cast<int>(timeCur.tv_usec&0xffff) % (rand()&0xffff)).str();

	if(false == test_root.isMember("test_task"))
	{
		cout << "not found \"test_task\" item in " << str_module_test_file <<", there has nothing to do!" << endl;
		return 0;
	}
    Json::Value& test_task = test_root["test_task"];
    if(false == test_task.isArray())
    {
        cout << "\"test_task\" item, must be array for query test task!" << endl;
        return 0;
    }

    zhicloud::ModuleTestService oTest(service_name, static_cast<zhicloud::util::ServiceType>(test_service_trans.second),domain,ip,group_ip,group_port);

    for(auto& query_item : test_task)
    {
        //cout << query_item["request"].asString() << endl;
        if(false == chk_json_data(query_item,"request:S;param:O", err_info))
        {
            cout<< "request  task data error:" << err_info << endl;
            return 0;
        }
        //auto itor = MainQueryInfo::GetQuerys().find(query_item["request"].asString());
        if(false == js_request_desc.isMember(query_item["request"].asString()))
        {
            cout<< "request task " << query_item["request"].asString() << " not describe in configure file!" << endl;
            return 0;
        }

        Json::Value& js_query = js_request_desc[query_item["request"].asString()];
        std::ostringstream desc;
        desc << query_item["request"].asString()  << " : ";
        Json::FastWriter writer;
        desc << writer.write(query_item["param"]);
        TestQueryTask test_task(val_map, js_query, query_item, desc.str());

        if(test_task.isOK() == false)
        {
            cout<< "request  " <<  desc.str() << " error :"  << test_task.getErr()<< endl;
            return 0;
        }

        oTest.addTestTask(test_task);
    }


    //ofstream of("out.log");
    //streambuf* coutBuf = cout.rdbuf();
    //cout.rdbuf(of.rdbuf());

    // loop analyse node
    oTest.startTest();

    finishLogging();

    return 0;
}
