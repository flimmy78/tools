#include "transport/transport_unify_test.h"
#include "transport/packet_handler_test.h"
#include "transport/transporter_test.h"
#include "transport/whisper_test.h"

#include <iostream>
#include <string>

#include <boost/log/trivial.hpp>
#include <exception>

using namespace std;

TransportUnifyTest::TransportUnifyTest()
{

}

TransportUnifyTest::~TransportUnifyTest()
{

}

bool TransportUnifyTest::test()
{
    try{
        string section_name("transport");
        BOOST_LOG_TRIVIAL(info) << "begin test section " << section_name << "...";
        bool packet_handler(false);
        bool transporter(false);
        bool whisper(true);

        string server_ip("172.16.2.174");

        if(packet_handler){
            PacketHandlerTest test(server_ip);
            if(!test.test()){
                throw std::logic_error("packet handler test fail");
            }
            BOOST_LOG_TRIVIAL(info) << "packet handler test success";
        }
        if(transporter){
            TransporterTest test(server_ip);
            if(!test.test()){
                throw std::logic_error("transporter test fail");
            }
            BOOST_LOG_TRIVIAL(info) << "transporter test success";
        }
        if(whisper){
            WhisperTest test(server_ip);
            if(!test.test()){
                throw std::logic_error("whisper test fail");
            }
            BOOST_LOG_TRIVIAL(info) << "whisper test success";
        }
        BOOST_LOG_TRIVIAL(info) << "section " << section_name << " test success";
        return true;
    }
    catch(exception& ex){
        BOOST_LOG_TRIVIAL(error) << "transport test fail:" << ex.what();
        return false;
    }
}



