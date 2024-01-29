import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition


def generate_launch_description():
    package_path = get_package_share_directory('point_lio')
    rviz_config_path = os.path.join(
        package_path, 'rviz_cfg', 'loam_livox.rviz')
    rviz_use = LaunchConfiguration('rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Use RViz to monitor results'
        ),
        Node(
            package='point_lio',
            executable='pointlio_mapping',
            name='laserMapping',
            output='screen',
            parameters=[
                {"use_imu_as_input": False},
                {"prop_at_freq_of_imu": True},
                {"check_satu": True},
                {"init_map_size": 10},
                {"point_filter_num": 1},
                {"space_down_sample": True},
                {"filter_size_surf": 0.3},
                {"filter_size_map": 0.2},
                {"cube_side_length": 2000.0},
                {"runtime_pos_log_enable": False},
                os.path.join(package_path, 'config', 'avia.yaml')
            ]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config_path],
            condition=IfCondition(rviz_use)
        )
    ])
