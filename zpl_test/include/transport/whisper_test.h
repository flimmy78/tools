#ifndef WHISPER_TEST_H
#define WHISPER_TEST_H

#include <string>

class WhisperTest
{
    public:
        WhisperTest(const std::string& ip);
        virtual ~WhisperTest();
        bool test();
    private:
        std::string _ip;
};

#endif // WHISPER_TEST_H
