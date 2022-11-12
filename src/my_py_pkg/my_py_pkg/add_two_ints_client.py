import rclpy
from rclpy.node import Node
from example_interfaces.srv import  AddTwoInts
from functools import partial

class AddTwoIntsClientsNode(Node):  
    def __init__(self):
        super().__init__("add_two_ints") 
        self.call_add_two_int_client(6,9)
    
    def call_add_two_int_client(self,a,b):
        client = self.create_client(AddTwoInts, "add_two_ints")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("client cannot get server !!!")
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future= client.call_async(request)
        future.add_done_callback(partial(self.callback_add_two_ints,a=a,b=b))

    def callback_add_two_ints(self,future, a, b):
        try:
       
            response = future.result()
            self.get_logger().info(str(a)+" + " + str(b)+" = "+str(response.sum))
        except Exception as e:
            self.get_logger().error("request is failed %r", (e,))


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClientsNode() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
