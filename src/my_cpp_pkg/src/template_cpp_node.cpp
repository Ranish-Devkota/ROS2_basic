#include "rclcpp/rclcpp.hpp"

class MyCustomNode :public rclcpp::Node //modifyname
{
	public:
		MyCustomNode() :Node("node_name") //modify name
		{
		}
	private:
};

int main(int argc, char **argv)
{
	rclcpp::init(argc,argv);
	auto node = std::make_shared<MyCustomNode>(); //Modify name
	rclcpp::spin(node);
	rclcpp::shutdown();
	return 0;
}
