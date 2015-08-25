#include "test_query_task.h"
#include <sstream>
#include "name_trans.h"
using namespace zhicloud::util;
using namespace zhicloud::transport;

namespace zhicloud
{
    TestQueryTask::TestQueryTask(ScriptVarTab& vals, const Json::Value& query_desc, Json::Value& test_data, const string& str_task_desc)
    :request_id(RequestEnum::invalid),var_tabs(vals),task_desc(str_task_desc),is_ok(false)
    {

        //ctor
        if(false == test_data.isMember("param") || false == test_data["param"].isObject())
        {
            err_info += "query test data must has \"param\" item, and it must be object! ";
        }
        else
        {
            Json::Value& params =  test_data["param"];
            // check param is same
            request_id = static_cast<RequestEnum>(query_desc["code"].asInt());

            js_request_param_desc = query_desc["param_list"];
            // check param is okey
            for(auto& need_param : js_request_param_desc.getMemberNames())
            {
                if(js_request_param_desc.isMember("optional") && js_request_param_desc["optional"].asBool())
                {
                    continue;
                }
                if(false == params.isMember(need_param))
                {
                    err_info += "query test data miss the param of \"" + need_param + "\"!";
                    return;
                }
            }


            // record respone type
            js_respone_desc = query_desc["respone_list"];
            js_request_param = test_data["param"];
            if(test_data.isMember("respone"))
            {
                if( test_data["respone"].isObject() )
                {
                    js_respone_act = test_data["respone"];
                }
                else
                {
                    err_info = " respone define error, must be object!";
                    return;
                }
            }

            is_ok = true;
        }

    }

    TestQueryTask::~TestQueryTask()
    {
        //dtor

    }

    static inline bool chk_is_value_name(const Json::Value& value_name)
    {
        if(!value_name || false == value_name.isString())
            return false;
        string value_tmp = value_name.asString();
        if(value_tmp.size() == 0)
            return false;
        return value_tmp[0] == '$';
    }

     static Json::Value get_data_by_define(const Json::Value& set_data, const ScriptVarTab& vab_map, const string& alise_tab) throw (ExceptionDesc)
    {
        if(false == chk_is_value_name(set_data))
        {
            if(set_data.isString())
            {
                if(alise_tab.size() > 0)
                {
                    // tran item
                    auto tran_rtn = get_name_trans()(alise_tab, set_data.asString());
                    if(!tran_rtn.first)
                    {
                        cout <<  "error !! script  " << set_data.asString() << " can not trans by " << alise_tab << "!" << endl;
                        throw ExceptionDesc(string("script  ") + set_data.asString()+ " can not trans by " + alise_tab +" !");
                        return Json::Value();
                    }
                    return Json::Value(tran_rtn.second);
                }
            }
            return set_data;
        }
        else
        {
            try
            {
                const Json::Value js_rtn =vab_map.getValue(set_data.asString());
                Json::FastWriter js_writer;
                cout << "var [" << set_data.asString() << "] = " << js_writer.write(js_rtn)<< endl;
                return js_rtn;
            }
            catch( ExceptionDesc err)
            {
                cout  << "Err! var " <<  set_data.asString() << " was never set a value! use \"set\" keyword to set a respone to a var! " << endl;
                throw err;
                return Json::Value();
            }
            catch(...)
            {
                throw ExceptionDesc("unknown error!");
                return Json::Value();
            }
        }
        return Json::Value();
    }

    bool TestQueryTask::tranRequestMsg(zhicloud::transport::AppMessage& request_msg)
    {

            request_msg = AppMessage(AppMessage::message_type::REQUEST, request_id);
            // check type
            for(auto& param_name : js_request_param.getMemberNames())
            {
                if(false == js_request_param_desc.isMember(param_name))
                {
                        err_info = param_name;
                        err_info += " not found in requery desc info!";
                        cout << err_info << endl;
                        return false ;
                }
                const Json::Value& param_desc = js_request_param_desc[param_name];
                ParamEnum param_key =  static_cast<ParamEnum>(get_name_trans()("param", param_name).second);
                auto val_type = getTypeByDesc(param_desc["data_type"].asString());
                string trans_tab_name;
                if(param_desc.isMember("trans_tab"))
                {
                    trans_tab_name = param_desc["trans_tab"].asString();
                }

                Json::Value param_test;
                try
                {
                     param_test =  get_data_by_define(js_request_param[param_name],  var_tabs,  trans_tab_name) ;
                }
                catch(ExceptionDesc err)
                {
                    cout << "on " << param_name << " get value err: " << err.getDesc() << endl;
                    return false;
                }
                catch(...)
                {
                    return false;
                }
                switch(val_type)
                {
                    case ValueType::uint_type :
                        if(false == param_test.isIntegral() )
                        {
                            err_info = param_name;
                            err_info += " need uint !";
                            cout << err_info << endl;
                            return false;
                        }
                        request_msg.setUInt(param_key, param_test.asUInt());
                        break;
                    case ValueType::float_type :
                        if(false == param_test.isDouble())
                        {
                            err_info = param_name;
                            err_info += " need float";
                            cout << err_info << endl;
                            return false;
                        }
                        request_msg.setFloat(param_key, static_cast<float>(param_test.asDouble()));
                        break;
                    case ValueType::str_type :
                        if(false == param_test.isString())
                        {
                            err_info = param_name;
                            err_info += " need string";
                            cout << err_info << endl;
                            return false;
                        }
                        request_msg.setString(param_key, param_test.asString());
                        break;
                    default:
                        err_info = "\"";
                        err_info += param_name;
                        err_info += "\" current not support this param type!";
                        cout << err_info << endl;
                        return false;
                        break;
                }
            }
            return true;
    }

    bool TestQueryTask::onRespone( zhicloud::transport::AppMessage& respone_msg, const string& sender,  Logger& logger)
    {
         cout << "receive respone " << endl;
        if(false == respone_msg.success)
        {
            cout << "respone false! now break test!"<< endl;
            // respone false
            err_info += (boost::format("request %s respone from %s false!") % task_desc % sender).str();
            return false;
        }
        logger.info(boost::format("request %s respone from %s success!") % task_desc % sender);
        bool has_error = false;
        string param_name;
        // trans respone message;
        for(auto& respone_name : js_respone_desc.getMemberNames())
        {
            Json::Value act_item;
            Json::Value respont_rlt;  // make respone data into json value, for easy check

            ParamEnum param_key =  static_cast<ParamEnum>(get_name_trans()("param", respone_name).second);
            std::string str_data_type = js_respone_desc[respone_name]["data_type"].asString();
            auto vtype = getTypeByDesc(str_data_type);
            string trans_tab_name;
            if(js_respone_desc[respone_name].isMember("trans_tab"))
            {
                trans_tab_name = js_respone_desc[respone_name]["trans_tab"].asString();
            }
            switch(vtype)
            {
            case ValueType::uint_type :
                {
                    uint32_t data;

                    if(false == respone_msg.getUInt(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss uint item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    string info;
                    std::pair<bool, std::string> tran_rtn(false , "");
                    if(trans_tab_name.size() > 0)
                    {
                        tran_rtn = get_name_trans()(trans_tab_name, static_cast<int>(data));
                    }
                    if(tran_rtn.first)
                    {
                        info = (boost::format("%s[%u] = %s") %respone_name% static_cast<uint32_t>(param_key) % tran_rtn.second).str();
                    }
                    else
                    {
                        info = (boost::format("%s[%u] = %u") %respone_name% static_cast<uint32_t>(param_key) % data).str();
                    }

                    logger.info(info);
                    cout << info << endl;
                    respont_rlt = Json::Value(data);
                }
                break;
            case ValueType::float_type :
                {
                    float data;
                    if(false == respone_msg.getFloat(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss float item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    string info = (boost::format("%s[%u] = %f") %respone_name% static_cast<uint32_t>(param_key) % data).str();
                    logger.info(info);
                    cout << info << endl;
                    respont_rlt = Json::Value(static_cast<double>(data));
                }
                break;
            case ValueType::str_type :
                {
                    std::string data;
                    if(false == respone_msg.getString(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss string item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    string info = (boost::format("%s[%u] = %s") %respone_name% static_cast<uint32_t>(param_key) % data).str();
                    logger.info(info);
                    cout << info << endl;
                    respont_rlt = Json::Value(data);
                }
                break;
            case ValueType::uint_array :
                {
                    AppMessage::uint_array_type data;
                    if(false == respone_msg.getUIntArray(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss uint_array item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    std::ostringstream oInfo;
                    for( auto& item : data)
                    {
                        std::pair<bool, std::string> tran_rtn(false , "");
                        if(trans_tab_name.size() > 0)
                        {
                            tran_rtn = get_name_trans()(trans_tab_name, static_cast<int>(item));
                        }
                        if(tran_rtn.first)
                        {
                            oInfo << tran_rtn.second << ",";
                        }
                        else
                        {
                            oInfo << item << ",";
                        }
                        respont_rlt.append(Json::Value(static_cast<int>(item)));
                    }
                    string info = (boost::format("%s[%u] =  [%s]") %respone_name% static_cast<uint32_t>(param_key) % oInfo.str()).str();
                    logger.info(info);
                    cout << info << endl;
                }
                break;
            case ValueType::float_array :
                {
                    AppMessage::float_array_type data;
                    if(false == respone_msg.getFloatArray(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss float_array item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    std::ostringstream oInfo;
                    for( auto& item : data)
                    {
                        oInfo << item << ",";
                        respont_rlt.append(Json::Value(static_cast<double>(item)));
                    }
                    string info = (boost::format("%s[%u] =  [%s]") %respone_name% static_cast<uint32_t>(param_key) % oInfo.str()).str();
                    logger.info(info);
                    cout << info << endl;
                }
                break;
            case ValueType::str_array :
                {
                    AppMessage::string_array_type data;
                    if(false == respone_msg.getStringArray(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss string_array item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    std::ostringstream oInfo;
                    for( auto& item : data)
                    {
                        oInfo << "\"" << item << "\",";
                        respont_rlt.append(Json::Value(item));
                    }
                    string info = (boost::format("%s[%u] =  [%s]") %respone_name% static_cast<uint32_t>(param_key) % oInfo.str()).str();
                    logger.info(info);
                    cout << info << endl;
                }
                break;
            case ValueType::uint_array_array :
                {
                    AppMessage::uint_array_array_type data;
                    if(false == respone_msg.getUIntArrayArray(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss uint_array_array item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    std::ostringstream oInfo;
                    for( auto& line : data)
                    {
                        oInfo << "[";
                        Json::Value sub;
                        for( auto& item : line)
                        {
                            std::pair<bool, std::string> tran_rtn(false , "");
                            if(trans_tab_name.size() > 0)
                            {
                                tran_rtn = get_name_trans()(trans_tab_name, static_cast<int>(item));
                            }
                            if(tran_rtn.first)
                            {
                                oInfo << tran_rtn.second << ",";
                            }
                            else
                            {
                                oInfo << item << ",";
                            }
                            sub.append(Json::Value(static_cast<int>(item)));
                        }
                        oInfo << "],";
                        respont_rlt.append(sub);
                    }
                    string info = (boost::format("%s[%u] =  [%s]") %respone_name% static_cast<uint32_t>(param_key) % oInfo.str()).str();
                    logger.info(info);
                    cout << info << endl;
                }
                break;
            case ValueType::float_array_array :
                {
                    AppMessage::float_array_array_type data;
                    if(false == respone_msg.getFloatArrayArray(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss float_array_array item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    std::ostringstream oInfo;
                    for( auto& line : data)
                    {
                        Json::Value sub;
                        oInfo << "[";
                        for( auto& item : line)
                        {
                            oInfo << item << ",";
                             sub.append(Json::Value(static_cast<double>(item)));
                        }
                        oInfo << "],";
                        respont_rlt.append(sub);
                    }
                    string info = (boost::format("%s[%u] =  [%s]") %respone_name% static_cast<uint32_t>(param_key) % oInfo.str()).str();
                    logger.info(info);
                    cout << info << endl;
                }
                break;
            case ValueType::str_array_array :
                {
                    AppMessage::string_array_array_type data;
                    if(false == respone_msg.getStringArrayArray(param_key, data))
                    {
                        string info;
                        info = (boost::format("respone miss string_array_array item %s[%u]!") % respone_name % static_cast<uint32_t>(param_key) ).str();
                        err_info += info;
                        logger.info(info);
                        cout << info << endl;
                        has_error = true;
                        break;
                    }
                    std::ostringstream oInfo;
                    for( auto& line : data)
                    {
                        Json::Value sub;
                        oInfo << "[";
                        for( auto& item : line)
                        {
                            oInfo << item << ",";
                            sub.append(Json::Value(item));
                        }
                        oInfo << "],";
                        respont_rlt.append(sub);
                    }
                    string info = (boost::format("%s[%u] =  [%s]") %respone_name% static_cast<uint32_t>(param_key) % oInfo.str()).str();
                    logger.info(info);
                    cout << info << endl;
                }
                break;
            default:
                logger.error("unknow value type, please check code!");
                cout << "!!!! type " << str_data_type << " unknown!!" << endl;
                break;

            }
            if(js_respone_act.isObject() && js_respone_act.isMember(respone_name))
            {
                act_item = js_respone_act[respone_name];
                try
                {
                    action(act_item, respont_rlt,trans_tab_name, logger);
                }
                catch(ExceptionDesc err)
                {
                    string info = respone_name + " check err: " + err.getDesc();
                    logger.error(info);
                    cout << info << endl;
                    has_error = true;
                }
                catch(...)
                {
                    string info = respone_name + " found some unknow error!";
                    logger.error(info);
                    cout << info << endl;
                    has_error = true;
                }
            }
        }
        if(has_error)
        {
            return false;
        }
        return true;
    }


    static bool value_include_check(const Json::Value& val, const Json::Value& chk_data)
    {
        if(chk_data.isArray())
        {
            for(auto& sub : chk_data)
            {
                if(value_include_check(val, sub))
                {
                    return true;
                }
            }
            return false;
        }

        if(val.isIntegral())
        {
            if(chk_data.isIntegral())
                return val.asInt() == chk_data.asInt();
            return false;
        }
        if(val.isDouble())
        {
            if(chk_data.isDouble())
                return abs(val.asDouble() - chk_data.asDouble()) <0.0000001;
            return false;
        }
        if(val.isString())
        {
            if(chk_data.isString())
            {
                return val.asString() == chk_data.asString();
            }
            return false;
        }
        if(val.isArray())
        {
            for(auto& sub : val)
            {
                if(value_include_check(sub, chk_data))
                {
                    return true;
                }
            }
            return false;
        }
        cout << "unknow type check " << endl;
        return false;
    }

    static bool value_except_check(const Json::Value& val, const Json::Value& chk_data)
    {
        return false == value_include_check(val, chk_data);
    }

    void TestQueryTask::action(Json::Value& act, const Json::Value& val, const string& alise_tab, Logger& logger) throw(ExceptionDesc)
    {
        if(act.isMember("set"))
        {
            logger.info("on \"set\" action");
            if(false == act["set"].isArray())
            {
                throw ExceptionDesc("script set item is must be array type!");
                return;
            }
            for(auto& item : act["set"])
            {
                if(false == chk_is_value_name(item))
                {
                    throw ExceptionDesc("script set item must be var array, the var must start with \"$\"!");
                    return;
                }
                Json::FastWriter jsWrite;
                var_tabs.setValue(item.asString(), val);
                logger.info(boost::format("set %s = %s")%item.asString()%jsWrite.write(val));
            }
        }
        if(act.isMember("include"))
        {
            logger.info("on \"include\" check action");
            if(false == act["include"].isArray())
            {
                throw ExceptionDesc("script include item is must be array type!");
                return;
            }
            Json::Value include = act["include"];
            std::vector< bool > inc_chk;
//            if(include.size() >0)
//            {
//                inc_chk.assign(include.size(), false);
//            }
            //for(auto item : include)
            for(int i = 0; static_cast<uint32_t>(i) <include.size(); ++i)
            {
                auto& item = include[i];
                try
                {
                    auto chk_data = get_data_by_define(item, var_tabs, alise_tab);
                    if(value_include_check(val, chk_data))
                    {
                        inc_chk.push_back(true);
                    }
                    else
                    {
                        inc_chk.push_back(false);
                    }
                }
                catch( ExceptionDesc err)
                {
                    cout << __LINE__ << " on err:" << err.getDesc() << endl;
                    throw err;
                    return;
                }
                catch(...)
                {
                    cout << __LINE__ << " on unknow err!" << endl;
                    throw ExceptionDesc("unknown error!");
                    return;
                }
            }
            for(int i = 0; static_cast<uint32_t>(i) < inc_chk.size(); ++i)
            {
                if(inc_chk[i] == false)
                {
                    logger.error(boost::format("in include check item [%d] is not include!")%i);
                    cout << "include check err:  item [ "<< i << "] is not include!" << endl;
                    throw ExceptionDesc((boost::format("the idx [%d] in include settings, is not find in responed! ")%i).str());
                    return;
                }
            }
        }
        // check expect
        if(act.isMember("except"))
        {
            logger.info("on \"except\" check action");
            if(false == act["except"].isArray())
            {
                cout << "script except item is must be array type!" << endl;
                throw ExceptionDesc("script except item is must be array type!");
                return;
            }
            for(int i = 0; static_cast<uint32_t>(i) <act["except"].size(); ++i)
            {
                auto& item = act["except"][i];
                try
                {
                    auto chk_data = get_data_by_define(item, var_tabs, alise_tab);
                    if(false == value_except_check(val, chk_data))
                    {
                        logger.error((boost::format("the idx [%d] in except settings, is find in responed! ")%i));
                        cout << "except check err: the idx [ "<< i << "] in except settings, is find in responed! " << endl;
                        throw ExceptionDesc((boost::format("the idx [%d] in except settings, is find in responed! ")%i).str());
                        return;
                    }
                }
                catch( ExceptionDesc err)
                {
                    throw err;
                    return;
                }
                catch(...)
                {
                    logger.error("unknown error!");
                    throw ExceptionDesc("unknown error!");
                    return;
                }
            }
        }
    }


    TestQueryTask::ValueType TestQueryTask::getTypeByDesc(const string& desc)
    {
        static bool     b_is_inited = false;
        static std::map< string,  TestQueryTask::ValueType >  value_type_map;
        if(!b_is_inited)
        {
            b_is_inited = true;
            value_type_map["uint"] = ValueType::uint_type;
            value_type_map["float"] = ValueType::float_type;
            value_type_map["string"] = ValueType::str_type;
            value_type_map["uint_array"] = ValueType::uint_array;
            value_type_map["float_array"] = ValueType::float_array;
            value_type_map["string_array"] = ValueType::str_array;
            value_type_map["uint_array_array"] = ValueType::uint_array_array;
            value_type_map["float_array_array"] = ValueType::float_array_array;
            value_type_map["string_array_array"] = ValueType::str_array_array;
        }
        auto itor = value_type_map.find(desc);
        if(itor == value_type_map.end())
        {
            return ValueType::unknown;
        }
        return itor->second;
    }








}
