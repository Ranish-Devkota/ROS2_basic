#include "rclcpp/rclcpp.hpp"
using namespace rclcpp ;

int main(int argc ,char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<rclcpp::Node>("cpp_test"); //decleration of node called cpp_test
    RCLCPP_INFO(node->get_logger(), "HELLO FROM CPP NODE");
    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}