FROM osrf/ros:noetic-desktop-full

# RUN apt-get update
# RUN apt-get -y ros-noetic-effort_controllers ros-noetic-joint_trajectory_controllers

RUN apt-get update \
    && apt-get install -y \
        ros-noetic-gazebo-ros \
        ros-noetic-gazebo-ros-pkgs \
        ros-noetic-gazebo-ros-control \
        ros-noetic-joint-state-controller \
        ros-noetic-effort-controllers \
        ros-noetic-position-controllers \
        ros-noetic-joint-trajectory-controller \ 
        ros-noetic-ros-control

