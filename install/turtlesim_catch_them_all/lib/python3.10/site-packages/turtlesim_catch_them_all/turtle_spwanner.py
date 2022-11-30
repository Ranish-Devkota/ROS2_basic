import rclpy
import math
import random
from rclpy.node import Node
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from functools import partial
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle


class TurtlespwannerNode(Node):
    def __init__(self):
        super().__init__("turtle_spwanner")
        self.turtle_name_prefix = "Turtle"
        self.counter = 0
        self.alive_Turtles = []
        self.call_timer = self.create_timer(2.0, self.timer_)
        self.alive_Turtles_publisher = self.create_publisher(
            TurtleArray, "alive_turtles", 10)
        self.catch_turtle_srv = self.create_service(
            CatchTurtle, "catch_turtles", self.callback_catch_turtles)

    def callback_catch_turtles(self, request, response):
        self.call_kill_turtle(request.name)
        response.success = True
        return response

    def publish_live_turtle_poses(self):
        msg = TurtleArray()
        msg.turtles = self.alive_Turtles
        self.alive_Turtles_publisher.publish(msg)

    def timer_(self):
        self.counter += 1
        turtle_name = self.turtle_name_prefix + str(self.counter)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        self.call_spwan_turtle(turtle_name, x, y, theta)

    def call_spwan_turtle(self, turtle_name, x, y, theta):
        client = self.create_client(Spawn, "spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("client cannot get server !!!")
        request = Spawn.Request()
        request.name = turtle_name
        request.x = x
        request.y = y
        request.theta = theta
        future = client.call_async(request)
        future.add_done_callback(partial(
            self.callback_spawn_turtle, turtle_name=turtle_name, x=x, y=y, theta=theta))

    def callback_spawn_turtle(self, future, turtle_name, x, y, theta):
        try:

            response = future.result()
            if response != "":
                self.get_logger().info(turtle_name + " is spwanned")
                Turtles = Turtle()
                Turtles.name = response.name
                Turtles.x = x
                Turtles.y = y
                Turtles.theta = theta
                self.alive_Turtles.append(Turtles)
                self.publish_live_turtle_poses()
        except Exception as e:
            self.get_logger().error("request is failed %r", (e,))

    def call_kill_turtle(self, turtle_name):
        client = self.create_client(Kill, "kill")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("client cannot get server !!!")
        request = Kill.Request()
        request.name = turtle_name
        future = client.call_async(request)
        future.add_done_callback(partial(
            self.callback_kill_turtle, turtle_name=turtle_name))

    def callback_kill_turtle(self, future, turtle_name):
        try:

            future.result()
            for (i, turtle) in enumerate(self.alive_Turtles):
                if turtle.name == turtle_name:
                    del self.alive_Turtles[i]
                    self.publish_live_turtle_poses()
                    break

        except Exception as e:
            self.get_logger().error("request is failed %r", (e,))


def main(args=None):
    rclpy.init(args=args)
    node = TurtlespwannerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
