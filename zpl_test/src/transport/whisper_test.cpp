#include "transport/whisper_test.h"
#include "transport/whisper_client_server.hpp"

WhisperTest::WhisperTest(const std::string& ip):_ip(ip)
{
    //ctor
}

WhisperTest::~WhisperTest()
{
    //dtor
}


bool WhisperTest::test(){
    try{
        bool client_server(true);

        BOOST_LOG_TRIVIAL(info) << "whisper test begin...";
        string case_name;
        if(client_server){
            case_name = "client&server";
            BOOST_LOG_TRIVIAL(info) << boost::format("test case:%s begin..") % case_name;
            WhisperClientServer test_case(_ip, 5);
            if(!test_case.test()){
                throw std::logic_error((boost::format("test case:%s failed") % case_name).str());
            }
            BOOST_LOG_TRIVIAL(info) << "test case: " << case_name << " test success";
        }

//        string filename("tmp");
//        {
//            ofstream cache;
//            cache.open(filename, ofstream::out|ofstream::binary|ofstream::trunc);
//            cache.seekp(9);
//            cache.write("world", 5);
//            cache.seekp(0);
//            cache.write("hello", 5);
//            cache.close();
//            BOOST_LOG_TRIVIAL(info) << boost::format("file '%s' written, size %d ") %filename %file_size(filename);
//        }
        return true;
    }
    catch(exception& ex){
        BOOST_LOG_TRIVIAL(error) << "whisper test exception:" << ex.what();
        return false;
    }
}
