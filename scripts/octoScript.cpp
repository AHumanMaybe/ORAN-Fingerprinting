#include <iostream>
#include <uhd/usrp_clock/multi_usrp_clock.hpp>
#include <vector>
#include <string>

// compile with uhd libraries
// gcc octoScript.cpp -o octoTest1 -luhd -lstdc++

int main(){

    try {
        
        //make clock object
        uhd::usrp_clock::multi_usrp_clock::sptr clock = uhd::usrp_clock::multi_usrp_clock::make("addr=192.168.10.3");
        
        //check device was found correctly
        if(!clock) {
            std::cerr << "Failed to create clock object" << std::endl;
            return -1;
        }

        //test data retrieval by getting current time on clock
        uint32_t time = clock->get_time(0);
        std::cout << "Time from octoclock: " << time << std::endl;

        //check list of sensors on device
        std::vector<std::string> names =  clock->get_sensor_names(0);

        //and output them
        for (std::string i: names){
            std::cout << i << "\n";
        }

    } catch (const uhd::runtime_error& e) {
        std::cerr << "UHD Error: " << e.what() << std::endl;
        return -1;
    } catch (const std::exception& e) {
        std::cerr << "Standard Exception: " << e.what() << std::endl;
        return -1;
    }

    return 0;
}
