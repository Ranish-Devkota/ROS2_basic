import rclpy
import math
from rclpy.node import Node
from functools import partial
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle
from turtlesim.srv import Kill


class TurtlesimController(Node):
    def __init__(self):
        super().__init__("controller")
        self.pose = None
        self.turtle_to_catch = None
        self.catch_closest_turtle_first = False
        

        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "turtle1/cmd_vel", 10)
        self.pose_suscriber = self.create_subscription(
            Pose, "turtle1/pose", self.pose_callback, 10)
        self.alive_turtles_subscriber = self.create_subscription(
            TurtleArray, "alive_turtles", self.callback_alive_turtle, 10)
        self.control_loop_timer = self.create_timer(0.01, self.control_loop)

    def pose_callback(self, msg):
        self.pose = msg

    def callback_alive_turtle(self,msg):
        if (len(msg.turtles)>0):
            # if self.catch_closest_turtle_first :
            #     closest_turtle = None
            #     closest_turtle_distance = None

            #     for turtle in msg.turtles:
            #         dist_x = turtle.x - self.pose.x
            #         dist_y = turtle.y - self.pose.y
            #         distance = math.sqrt(dist_x*dist_x + dist_y * dist_y)

            #         if closest_turtle == None or  closest_turtle_distance < distance :
            #             closest_turtle = turtle
            #             closest_turtle_distance = distance
                
            #     self.turtle_to_catch = closest_turtle
            
            # else:

             self.turtle_to_catch = msg.turtles[0]
             self.catch_closest_turtle_first = True

    def control_loop(self):
        if self.pose == None or self.turtle_to_catch == None:
            # do nothing  untill we get the pose of robot
            return

        dist_x = self.turtle_to_catch.x- self.pose.x
        dist_y = self.turtle_to_catch.y - self.pose.y
        # dist_x = 4
        # dist_y = 8

        dist = math.sqrt(dist_x*dist_x + dist_y * dist_y)
        self.get_logger().info(str(dist))

        msg = Twist()

        if dist > 0.5:
            msg.linear.x = 0.5*dist_x         

            # for orientation
            goal_theta = math.atan2(dist_y, dist_x)
            diff = goal_theta - self.pose.theta

            if diff > math.pi:
                diff -= 2*math.pi

            elif diff < math.pi:
                diff += 2*math.pi

            msg.angular.z = 0.25* diff
              # for linear
            
           
        else:
            #target reached
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            # target met
            self.call_catch_turtle(self.turtle_to_catch.name)
            self.get_logger().info(self.turtle_to_catch.name)
            self.turtle_to_catch = None
        self.cmd_vel_publisher_.publish(msg)

    def call_catch_turtle(self, turtle_name):
        client = self.create_client(CatchTurtle, "catch_turtles")

        while not client.wait_for_service(1.0):
            self.get_logger().warn("client cannot get server !!!")

        request =CatchTurtle.Request()
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(partial(
            self.callback_Catch_turtle, turtle_name=turtle_name))

    def callback_Catch_turtle(self, future, turtle_name):
        try:

            response = future.result()
            if not response.success:
                self.get_logger().error(str(turtle_name)+" is not caught")

        except Exception as e:
            self.get_logger().error("request is failed %r", (e,))



def main(args=None):
    rclpy.init(args=args)
    node = TurtlesimController()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
