from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    ld = LaunchDescription()
    robot_names = ["Giskard", "BB8", "Daneel", "Jander", "C3PO", ]
    robot_news_station = []

    for robot in robot_names:

        robot_news_station.append(Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_"+robot.lower(),
            parameters=[{"robot_name": robot}]
        )

        )

    receivers = Node(
        package="my_py_pkg",
        executable="smartphone"
    )
    for name in robot_news_station:
        ld.add_action(name)
    ld.add_action(receivers)

    return ld
