import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64


class NumberCounter(Node):
    def __init__(self):
        super().__init__("Number_counter")
        self.publisher_ = self.create_publisher(Int64,"number_count", 10)
        self.subscriber_ = self.create_subscription(
            Int64, "number", self.callback_msg_count, 10)
        self.counter_ = 0
        self.get_logger().info("number_counter Subscriber is started")
        
 
    def callback_msg_count(self, msg):
        self.counter_+=msg.data
        self.get_logger().info(str(self.counter_))  
        new_msg = Int64()
        new_msg.data = self.counter_
        self.publisher_.publish(new_msg)
        

    # def publish_number(self):
    #     msg = Int64
    #     msg.data = 110
    #     self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
