import rclpy
from rclpy.node import Node

class MyCustomNode(Node): # modify_name 
    def __init__(self):
        super().__init__("node_name") # modify_name


def main(args=None):
    rclpy.init(args=args)
    node = MyCustomNode() # modify_name
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
