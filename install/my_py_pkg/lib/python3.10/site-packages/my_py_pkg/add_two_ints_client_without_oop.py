import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.node import Node


def main(args=None):
    rclpy.init(args=args)
    node = Node("add_two_int_without_oop")
    client = node.create_client(AddTwoInts, "add_two_ints")
    while not client.wait_for_service(1.0):
        node.get_logger().warn("client cannot get server !!!")
    request = AddTwoInts.Request()
    request.a = 3
    request.b = 5
    future= client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
    try:
        # response = AddTwoInts.Response()
        # response.sum
        response = future.result()
        # node.get_logger().info(str(response))
        node.get_logger().info(str(request.a)+" + " + str(request.b)+" = "+str(response.sum))
    except Exception as e:
        node.get_logger().error("request is failed %r", (e,))

    rclpy.shutdown()


if __name__ == "__main__":
    main()
