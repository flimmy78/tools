#ifndef SCRIPTVARTAB_H
#define SCRIPTVARTAB_H
#include "json/json.h"
#include <map>
#include <string>
#include "exception_desc.h"

namespace zhicloud
{
    class ScriptVarTab
    {
        public:
            typedef std::map< std::string, Json::Value >    VarMap;
            ScriptVarTab();
            virtual ~ScriptVarTab();

            void setValue(const std::string& value_name, const std::string& data);
            void setValue(const std::string& value_name, uint32_t data);
            void setValue(const std::string& value_name, float data);

            void setValue(const std::string& value_name, const Json::Value&  data);

            std::string getStrValue(const std::string& value_name) const throw(ExceptionDesc);
            uint32_t getUIntValue(const std::string& value_name) const throw(ExceptionDesc);
            float getFloatValue(const std::string& value_name) const throw(ExceptionDesc);

            const Json::Value& getValue(const std::string& value_name) const throw(ExceptionDesc);

        protected:
        private:
            VarMap          value_maps;
    };
};
#endif // SCRIPTVARTAB_H
