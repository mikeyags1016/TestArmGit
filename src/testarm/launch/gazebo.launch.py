import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node
import xacro


def generate_launch_description():
    robot_name = 'testarm'
    world_file_name = 'testarm.world'

    # Parsing URDF.XACRO
    xacro_file = os.path.join(get_package_share_directory(
        robot_name), 'urdf', 'testarm_urdf.urdf.xacro')    
    xml_arm = xacro.process_file(xacro_file).toxml()#.replace('"', '\\"')

    # Configuring RVIZ
    rviz = os.path.join(get_package_share_directory(
        robot_name), 'rviz', 'urdf.rviz')

    # Configuring RVIZ Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz, '--title', 'Test arm'],
    )

    # Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': xml_arm,
        'use_sim_time': True}]
    )

    # Configuring Gazebo
    # gazebo= ExecuteProcess(
    #     cmd=['gazebo', '-u', '--verbose',
    #          '-s', 'libgazebo_ros_factory.so',
    #          '-s', 'libgazebo_ros_init.so', '--ros-args',  
    #          ],
    #     output='screen'
    # )
    gazebo= ExecuteProcess(
        cmd=['gazebo', '-u', os.path.join(get_package_share_directory(robot_name), 'worlds', 'testarm.world'), "--verbose",
             "-s", "libgazebo_ros_factory.so",
             "-s", "libgazebo_ros_init.so", "--ros-args", "--params-file", os.path.join(get_package_share_directory(robot_name), 'config', 'params_init.yaml'),
             ],
        output='screen'
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    #          )

    # Spawning Robot Arm
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', '/robot_description',
                                '-entity', 'testarm'],
                    output='screen')

    # Joint State Broadcaster
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        parameters=["joint_state_broadcaster"]
    )
    # ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
    #          'joint_state_broadcaster'],
    #     output='screen'
    # )

    # Joint Trajectory Controller
    joint_arm_position_controller = Node(
        package="controller_manager",
        executable="spawner",
        parameters=["arm_controller"]
    )
    # ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
    #          'arm_controller'],
    #     output='screen'
    # )

    # Run the node
    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster,
        joint_arm_position_controller,
        rviz_node
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=spawn_entity,
        #         on_exit=[joint_state_broadcaster],
        #     )
        # ),
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=joint_state_broadcaster,
        #         on_exit=[joint_arm_position_controller],
        #     )
        # ),
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=joint_state_broadcaster,
        #         on_exit=[rviz_node],
        #     )
        # ),
    ])