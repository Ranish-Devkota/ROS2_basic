from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    ld = LaunchDescription()
    Battery_node = Node(
        package="LED_system",
        executable="battery_node"

    )
    pannel_node = Node(
        package="LED_system",
        executable="pannel"
    )
    ld.add_action(Battery_node)
    ld.add_action(pannel_node)

    return ld
