import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus


class HardwareStatusPublisherNode(Node):
    def __init__(self):
        super().__init__("Hw_status_publisher")
        self.hw_status_publisher = self.create_publisher(
            HardwareStatus, "Hardware_status", 10)
        self.timer_ = self.create_timer(1.00, self.callback_hw_status)
        self.get_logger().info("Hardware status will be published")

    def callback_hw_status(self):
        msg = HardwareStatus()
        msg.temperature = 45
        msg.are_motors_ready = False
        msg.debug_message = "well i've managed to use my_own interface nothin' much to say"
        self.hw_status_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
