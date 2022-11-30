import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed
from functools import partial


class BatteryNode(Node):
    def __init__(self):
        super().__init__("Battery")
        self.Battery_state = "Full"
        self.last_battery_state_ = self.timer_()
        self.check_battery_ = self.create_timer(0.1, self.battery_state_check)
        self.get_logger().info("Battery node is started")

    def timer_(self):
        sec, nsec = self.get_clock().now().seconds_nanoseconds()
        return (sec+nsec/1000000000.0)

    def battery_state_check(self):
        time_now = self.timer_()
        if self.Battery_state == "Full":
            if time_now - self.last_battery_state_ >= 4.0:
                self.Battery_state = "Empty"
                self.get_logger().warn("battery is discharged !!!! Charge now")
                self.last_battery_state_ = time_now
                self.call_set_led_states(3, 1)
        else:
            if time_now - self.last_battery_state_ > 6.0:
                self.Battery_state = "Full"
                self.get_logger().info("battery is charged !!!! ")
                self.last_battery_state_ = time_now
                self.call_set_led_states(3, 0)

    def call_set_led_states(self, led_number, led_states):
        client = self.create_client(SetLed, "set_led")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("client cannot get server !!!")
        request = SetLed.Request()
        request.led_number = led_number
        request.led_states = led_states

        future = client.call_async(request)
        future.add_done_callback(partial(
            self.callback_set_led, led_number=led_number, led_states=led_states))

    def callback_set_led(self, future, led_number, led_states):
        try:

            response = future.result()
            self.get_logger().info(str(response.success))
        except Exception as e:
            self.get_logger().error("request is failed %r", (e,))


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
