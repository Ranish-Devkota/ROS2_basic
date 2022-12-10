from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    turtlesim_node = Node(
        package= "turtlesim",
        executable= "turtlesim_node"
    )
    spwanner_node = Node(
        package= "turtlesim_catch_them_all",
        executable= "spwanner",
        parameters=[
            {"spwanning_frequency": 1.5},
            {"turtle_name_prefix": "My_Turtles"}
        ]
    )
    controller_node = Node(
        package= "turtlesim_catch_them_all",
        executable= "target",
        parameters= [
            {"catch_closest_turtles_first": True}
        ]
    )


    ld.add_action(turtlesim_node)
    ld.add_action(spwanner_node)
    ld.add_action(controller_node)
    return ld