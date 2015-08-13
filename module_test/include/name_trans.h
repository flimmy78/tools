#ifndef NAMETRANS_H
#define NAMETRANS_H
#include <json/json.h>
#include "util/define.hpp"
#include <map>

namespace zhicloud
{

    class NameTrans
    {
        public:
            NameTrans();
            virtual ~NameTrans();

            bool init(Json::Value& node_trans);

            std::pair<bool, int> operator () (const std::string& trans_tab, const std::string& name) const;

            std::pair<bool, std::string> operator () (const std::string& trans_tab, int32_t value) const;

        protected:

        private:
            Json::Value    trans_json;

            static NameTrans    name_tran;
    };

    bool init_name_trans(Json::Value& node_trans);
    const NameTrans& get_name_trans();
}

#endif // NAMETRANS_H
