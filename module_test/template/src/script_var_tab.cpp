#include "script_var_tab.h"

using namespace std;

namespace zhicloud
{

    ScriptVarTab::ScriptVarTab()
    {
        //ctor
    }

    ScriptVarTab::~ScriptVarTab()
    {
        //dtor
    }


    void ScriptVarTab::setValue(const string& value_name, const string& data)
    {
        value_maps[value_name]=Json::Value(data);
    }

    void ScriptVarTab::setValue(const string& value_name, uint32_t data)
    {
        value_maps[value_name]=Json::Value(data);
    }

    void ScriptVarTab::setValue(const string& value_name, float data)
    {
        value_maps[value_name]=Json::Value(static_cast<double>(data));
    }

    void ScriptVarTab::setValue(const std::string& value_name, const Json::Value&  data)
    {
        value_maps[value_name]=data;
    }

    string ScriptVarTab::getStrValue(const string& value_name) const throw(ExceptionDesc)
    {
        try
        {
            const Json::Value& value = getValue(value_name);
            if(false == value.isString())
            {
                throw ExceptionDesc(value_name + " is not string type!");
                return string();
            }
            return value.asString();
        }
        catch(ExceptionDesc ex)
        {
            throw ex;
        }
        catch(...)
        {
            throw ExceptionDesc("unknow errors");
        }
        return string();
    }

    uint32_t ScriptVarTab::getUIntValue(const string& value_name) const throw(ExceptionDesc)
    {
        try
        {
            const Json::Value& value = getValue(value_name);
            if(false == value.isUInt())
            {
                throw ExceptionDesc(value_name + " is not uint type!");
                return 0;
            }
            return value.asUInt();
        }
        catch(ExceptionDesc ex)
        {
            throw ex;
        }
        catch(...)
        {
            throw ExceptionDesc("unknow errors");
        }
        return 0;
    }

    float ScriptVarTab::getFloatValue(const string& value_name) const throw(ExceptionDesc)
    {
        try
        {
            const Json::Value& value = getValue(value_name);
            if(false == value.isDouble())
            {
                throw ExceptionDesc(value_name + " is not float type!");
                return 0;
            }
            return static_cast<float>(value.asDouble());
        }
        catch(ExceptionDesc ex)
        {
            throw ex;
        }
        catch(...)
        {
            throw ExceptionDesc("unknow errors");
        }
        return 0;
    }

    const Json::Value& ScriptVarTab::getValue(const string& value_name) const throw(ExceptionDesc)
    {
        static Json::Value s_js_error;
        auto itor = value_maps.find(value_name);
        if(itor == value_maps.end())
        {
            throw ExceptionDesc(value_name + " not defined!");
            return s_js_error;
        }
        return itor->second;
    }
}
