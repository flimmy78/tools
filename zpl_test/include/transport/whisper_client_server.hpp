#ifndef WHISPER_CLIENT_SERVER_HPP_INCLUDED
#define WHISPER_CLIENT_SERVER_HPP_INCLUDED

#include <string>
#include <transport/whisper.h>
#include <boost/log/trivial.hpp>
#include <boost/filesystem.hpp>

using std::string;
using namespace zhicloud::transport;
using namespace boost::filesystem;

class Observer{
public:
    Observer():_result(false){
    }
    void onTaskStart(const uint32_t& task_id, const uint16_t& task_type){
        BOOST_LOG_TRIVIAL(info) << boost::format("task %d started, type %d") %task_id %task_type;
    }
    void onTaskProgress(const uint32_t& task_id, const uint16_t& task_type, const uint64_t& current,
                                        const uint64_t& total, const uint64_t& speed)
    {
        double percent = double(current)*100/total;
        BOOST_LOG_TRIVIAL(info) << boost::format("on progress, task %d, %d / %d, %.1f %%, %.2f MiB/s")
                                                            %task_id %current %total %percent %(double(speed)/1048576);
    }
    void onTaskSuccess(const uint32_t& task_id, const uint16_t& task_type, const string& file_id){

        lock_type lock(_mutex);
        BOOST_LOG_TRIVIAL(info) << boost::format("task %d success, file id '%s'") %task_id %file_id;
        _file_id = file_id;
        _result = true;
        finish_event.notify_all();
    }
    void onTaskFail(const uint32_t& task_id, const uint16_t& task_type){
        lock_type lock(_mutex);
        BOOST_LOG_TRIVIAL(info) << boost::format("task %d fail") %task_id;
        _result = false;
        finish_event.notify_all();
    }
    bool waitFinish(){
        lock_type lock(_mutex);
        finish_event.wait(lock);
        return _result;
    }
    const string& getFileID(){
        return _file_id;
    }
private:
    bool _result;
    string _file_id;
    std::mutex _mutex;
    typedef std::unique_lock< std::mutex > lock_type;
    condition_variable finish_event;
};


class WhisperClientServer{
public:
    WhisperClientServer(const string& ip, const size_t& channel):_ip(ip), _channel(channel)
    {

    }

    ~WhisperClientServer(){
    }
    bool test(){
        Whisper server(_ip, _channel, "./server");
        Whisper client(_ip, _channel, "./client");
        try{

            if(!server.start()){
                BOOST_LOG_TRIVIAL(info) << boost::format("start whisper server at '%s' fail") %_ip;
                return false;
            }
            BOOST_LOG_TRIVIAL(info) << boost::format("whisper server started, service address '%s:%d'") %_ip %server.control_port();

            Observer observer;
            client.bindObserver(&observer);
             if(!client.start()){
                BOOST_LOG_TRIVIAL(info) << boost::format("start whisper client at '%s' fail") %_ip;
                return false;
            }
            BOOST_LOG_TRIVIAL(info) << boost::format("whisper client started, service address '%s:%d'") %_ip %client.control_port();
            uint64_t total_size(0);
            uint64_t write_speed(0), read_speed(0);
            //write first
            {
    //            string filename("/home/develop/zpl_test/tiny");
    //            string filename("/home/develop/zpl_test/small");
                string filename("/home/develop/zpl_test/normal");
//                string filename("/home/develop/zpl_test/big");
    //            string filename("/home/develop/zpl_test/lion_king.mkv");
                if(!exists(filename)){
                    throw logic_error((boost::format("target file '%s' not exists")%filename).str());
                }
                total_size = file_size(filename);

                string file_id;
                client.attachFile(filename, file_id);
                BOOST_LOG_TRIVIAL(info) << boost::format("send file '%s' attached as '%s'") %filename %file_id;
                uint32_t task_id(0);
                chrono::time_point< std::chrono::high_resolution_clock > begin_time = chrono::high_resolution_clock::now();
                client.beginWrite(file_id, EndpointAddress(_ip, server.control_port()), task_id);
                BOOST_LOG_TRIVIAL(info) << boost::format("write task %d started") %task_id;
                bool result = observer.waitFinish();
                if(!result){
                    throw logic_error("write file fail");
                }
                chrono::time_point< std::chrono::high_resolution_clock > end_time = chrono::high_resolution_clock::now();
                uint64_t elapsed = chrono::duration_cast< chrono::seconds >( end_time - begin_time).count();
                if(0 != elapsed){
                    write_speed = total_size/elapsed;
                }
                BOOST_LOG_TRIVIAL(info) << boost::format("write task %d success") %task_id;
            }
            {
                //read test
                string remote_file_id = observer.getFileID();
                uint32_t task_id(0);
                chrono::time_point< std::chrono::high_resolution_clock > begin_time = chrono::high_resolution_clock::now();
                client.beginRead(remote_file_id, EndpointAddress(_ip, server.control_port()), task_id);
                BOOST_LOG_TRIVIAL(info) << boost::format("read file '%s' from '%s:%d' started, task id %d") %remote_file_id %_ip %server.control_port() %task_id;
                bool result = observer.waitFinish();
                if(!result){
                    throw logic_error("read file fail");
                }
                chrono::time_point< std::chrono::high_resolution_clock > end_time = chrono::high_resolution_clock::now();
                uint64_t elapsed = chrono::duration_cast< chrono::seconds >( end_time - begin_time).count();
                if(0 != elapsed){
                    read_speed = total_size/elapsed;
                }
                BOOST_LOG_TRIVIAL(info) << boost::format("read task %d success") %task_id;
                string local_file_id = observer.getFileID();
                string filename("read_result");
                client.fetchFile(local_file_id, filename);
                BOOST_LOG_TRIVIAL(info) << boost::format("file '%s' fetched into '%s'") %local_file_id %filename;
            }
            BOOST_LOG_TRIVIAL(info) << boost::format("average write speed %d MiB/s") %(write_speed/1048576);
            BOOST_LOG_TRIVIAL(info) << boost::format("average read speed %d MiB/s") %(read_speed/1048576);
            client.stop();
            server.stop();
            return true;
        }
        catch(exception& ex){
            BOOST_LOG_TRIVIAL(error) << "whipser test exception, message:" << ex.what();
            return false;
        }
    //    zhicloud::util::finishLogging();

    }
private:
    string _ip;
    size_t _channel;

};

#endif // WHISPER_CLIENT_SERVER_HPP_INCLUDED
