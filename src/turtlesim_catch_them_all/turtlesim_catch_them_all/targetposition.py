import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from functools import partial

from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.msg import Turtle

from my_robot_interfaces.srv import CatchTurtle


class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("Turtle_controller")
        self.declare_parameter("catch_closest_turtles_first", True)
        self.catch_closest_turtles_ = self.get_parameter(
            "catch_closest_turtles_first").value
        self.pose_ = None
        # self.target_x_ = 3.0
        # self.target_y_ = 7.0
        self.turtle_to_catch_ = None

        self.pose_publisher_ = self.create_publisher(
            Twist, "turtle1/cmd_vel", 10)
        self.pose_subscriber_ = self.create_subscription(
            Pose, "turtle1/pose", self.callback_turtle_pose, 10)
        self.alive_turtles_subscriber_ = self.create_subscription(
            TurtleArray, "alive_turtles", self.callback_alive_turtles, 10)
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)

    def callback_turtle_pose(self, msg):
        self.pose_ = msg

    def callback_alive_turtles(self, msg):
        if len(msg.turtles) > 0:
            if self.catch_closest_turtles_:
                closest_turtle = None
                closest_turtle_distance = None

                for turtle in msg.turtles:
                    dist_x = turtle.x - self.pose_.x
                    dist_y = turtle.y - self.pose_.y
                    dist = math.sqrt(dist_x*dist_x + dist_y*dist_y)

                    if closest_turtle == None or dist > closest_turtle_distance:
                        closest_turtle = turtle
                        closest_turtle_distance = dist
                self.turtle_to_catch_ = closest_turtle
            else:
                self.turtle_to_catch_ = msg.turtles[0]

    def control_loop(self):
        if self.pose_ == None or self.turtle_to_catch_ == None:
            self.get_logger().error("control loop is terminated")
            return

        distance_x = self.turtle_to_catch_.x - self.pose_.x
        distance_y = self.turtle_to_catch_.y - self.pose_.y

        distance = math.sqrt(distance_x*distance_x + distance_y*distance_y)
        msg = Twist()

        if distance > 0.5:
            msg.linear.x = 2 * distance
            angle = math.atan2(distance_y, distance_x)
            diff = angle - self.pose_.theta

            if diff > math.pi:
                diff -= 2*math.pi
            elif diff < -math.pi:
                diff += 2*math.pi

            msg.angular.z = 6*diff
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.call_catch_turtle_server(self.turtle_to_catch_.name)
            self.turtle_to_catch_ = None

        self.pose_publisher_.publish(msg)

    def call_catch_turtle_server(self, turtle_name):
        client = self.create_client(CatchTurtle, "catch_turtles")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("client cannot get server !!!")
        request = CatchTurtle.Request()
        request.name = turtle_name
        future = client.call_async(request)
        future.add_done_callback(partial(
            self.callback_catch_turtle, turtle_name=turtle_name))

    def callback_catch_turtle(self, future, turtle_name):
        try:

            response = future.result()
            if not response.success:
                self.get_logger().error(str(turtle_name)+" can not be caught")

        except Exception as e:
            self.get_logger().error("request is failed %r", (e,))


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
