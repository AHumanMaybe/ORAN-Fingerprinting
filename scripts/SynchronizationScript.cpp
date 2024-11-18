#include <iostream>
#include <chrono>
#include <thread>
#include <uhd/utils/thread.hpp>
#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/types/time_spec.hpp>


int main() {

    uhd::usrp::multi_usrp::sptr usrp1 = uhd::usrp::multi_usrp::make("serial=327125E"); // Example address for USRP1
    uhd::usrp::multi_usrp::sptr usrp2 = uhd::usrp::multi_usrp::make("serial=329089E"); // Example address for USRP2

    const uhd::time_spec_t last_pps_time1 = usrp1->get_time_last_pps();
    while (last_pps_time1 == usrp1->get_time_last_pps()){
        //sleep 100 milliseconds (give or take)
    }
    // This command will be processed fairly soon after the last PPS edge:
    usrp1->set_time_next_pps(uhd::time_spec_t(0.0));

    const uhd::time_spec_t last_pps_time = usrp2->get_time_last_pps();
    while (last_pps_time == usrp2->get_time_last_pps()){
        //sleep 100 milliseconds (give or take)
    }
    // This command will be processed fairly soon after the last PPS edge:
    usrp2->set_time_next_pps(uhd::time_spec_t(0.0));
    return 0;
}