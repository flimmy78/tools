#include "name_trans.h"

namespace zhicloud
{

    NameTrans::NameTrans()
    {
        //ctor
    }

    NameTrans::~NameTrans()
    {
        //dtor
    }

    bool NameTrans::init(Json::Value& node_trans)
    {
        trans_json = node_trans;
        if(false == trans_json.isMember("param"))
        {
            return false;
        }
        return true;
    }

    std::pair<bool, int> NameTrans::operator () (const std::string& trans_tab, const std::string& name) const
    {
        std::pair<bool, int> rtn(false, 0);
        if( trans_json.isObject() && trans_json.isMember(trans_tab))
        {
                const Json::Value& js_tab = trans_json[trans_tab];
                if(js_tab.isObject() && js_tab.isMember(name))
                {
                       if(js_tab[name].isIntegral())
                       {
                            rtn.first = true;
                            rtn.second = js_tab[name].asInt();
                       }
                }
        }
        return rtn;
    }

    std::pair<bool, std::string> NameTrans::operator () (const std::string& trans_tab, int32_t value) const
    {
         std::pair<bool, std::string> rtn(false, std::string());
        if( trans_json.isObject() && trans_json.isMember(trans_tab))
        {
                const Json::Value& js_tab = trans_json[trans_tab];
                if(js_tab.isObject() )
                {
                    for (auto& item : js_tab.getMemberNames() )
                    {
                       if(js_tab[item].isIntegral() && value ==  js_tab[item].asInt())
                       {
                            rtn.first = true;
                            rtn.second = item;
                            return rtn;
                       }
                    }
                }
        }
        return rtn;
    }

    static NameTrans    globle_name_trans;

    bool init_name_trans(Json::Value& node_trans)
    {
        return globle_name_trans.init(node_trans);
    }

    const NameTrans& get_name_trans()
    {
        return globle_name_trans;
    }

}
