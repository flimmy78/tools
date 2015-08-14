#ifndef EXCEPTIONDESC_H
#define EXCEPTIONDESC_H

#include <string>

namespace zhicloud
{
    // the only type for error desc
    class ExceptionDesc
    {
        public:
            ExceptionDesc(const std::string& info) {}
            virtual ~ExceptionDesc() {}

            const std::string& getDesc() const { return err_desc; }
        protected:
        private:
            std::string     err_desc;
    };
};

#endif // EXCEPTIONDESC_H
