from functools import partial

import rclpy
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool
from rclpy.node import Node


class NumberCounter(Node):
    def __init__(self):
        super().__init__("Number_counter")
        
        self.publisher_ = self.create_publisher(Int64, "number_count", 10)

        self.subscriber_ = self.create_subscription(
            Int64, "number", self.callback_msg_count, 10)
        self.counter_ = 0
        self.get_logger().info("number_counter Subscriber is started")
        self.reset_counter_service = self.create_service(
            SetBool, "reset_counter", self.reset_counter)
        self.get_logger().info("Service is created to reset")

    def callback_msg_count(self, msg):
        self.counter_ += msg.data
        self.get_logger().info(str(self.counter_))
        new_msg = Int64()
        new_msg.data = self.counter_
        self.publisher_.publish(new_msg)

    def reset_counter(self,request,response):
        # request = SetBool()
        # response = SetBool()
        if request.data:
            self.counter_ = 0
            response.success = True
            response.message = "counter is resetted"
        else:
            response.success = False
            response.message = "counter isn't resetted"

        return response

        # data.cond=self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
