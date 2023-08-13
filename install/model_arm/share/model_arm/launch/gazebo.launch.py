#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue  # Need master or Galactic branch for this feature

def generate_launch_description():
  use_sim_time = LaunchConfiguration('use_sim_time')
  model_path = LaunchConfiguration('model_path')
  

  return LaunchDescription([

    DeclareLaunchArgument(
      'use_sim_time',
      default_value="false",
      description='Flag to use simulation time'),   

    DeclareLaunchArgument(
      'model_path',
      default_value=os.path.join(get_package_share_directory('model_arm'),'urdf','testarm_urdf.xacro'),
      description='path to urdf'),

    Node(
      package='robot_state_publisher',
      executable='robot_state_publisher',
      name='robot_state_publisher',
      output='screen',
      parameters=[{
        'use_sim_time': use_sim_time,
        'robot_description': ParameterValue(Command(['xacro ',model_path]), value_type=str)
      }])
  ])