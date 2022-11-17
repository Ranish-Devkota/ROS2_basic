import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedStatesArray
from my_robot_interfaces.srv import SetLed


class LedPannelNode(Node):
    def __init__(self):
        super().__init__("node_name")
        self.led_states = [0, 0, 0]
        self.publisher_ = self.create_publisher(
            LedStatesArray, "led_states", 10)
        self.led_srv_ = self.create_service(
            SetLed, "set_led", self.callback_set_led)
        self.create_timer(3, self.led_states_publisher)
        self.get_logger().info("led_states node is publishing to led states")

    def led_states_publisher(self):
        status = LedStatesArray()
        status.led_states = self.led_states
        self.publisher_.publish(status)

    def callback_set_led(self, request, response):
        led_number = request.led_number
        states = request.led_states

        if led_number > len(self.led_states) or led_number <= 0:
            response.success = False
            return response

        if states not in [0, 1]:
            response.success = False
            return response

        self.led_states[led_number - 1] = states
        response.success = True
        self.led_states_publisher()
        return response


def main(args=None):
    rclpy.init(args=args)
    node = LedPannelNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
