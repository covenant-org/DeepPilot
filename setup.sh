#!/bin/bash

PROJECT_ROOT_DIR=$(git rev-parse --show-toplevel)
cd $PROJECT_ROOT_DIR

mkdir -p ~/.gazebo/models

ln -s ${PROJECT_ROOT_DIR}/gazebo_models/* ~/.gazebo/models/

git clone -b noetic https://github.com/simonernst/iROS_drone ${PROJECT_ROOT_DIR}/src/iROS_drone
rm -r ${PROJECT_ROOT_DIR}/src/iROS_drone/rotors_simulator/rotors_gazebo/launch/spawn_mav.launch
ln -s ${PROJECT_ROOT_DIR}/launch/* ${PROJECT_ROOT_DIR}/src/iROS_drone/rotors_simulator/rotors_gazebo/launch
mkdir ${PROJECT_ROOT_DIR}/src/iROS_drone/rotors_simulator/rotors_gazebo/adr_worlds
ln -s ${PROJECT_ROOT_DIR}/adr_worlds/* ${PROJECT_ROOT_DIR}/src/iROS_drone/rotors_simulator/rotors_gazebo/adr_worlds


git clone https://github.com/ethz-asl/mav_comm ${PROJECT_ROOT_DIR}/src/mav_comm
git clone -b ros1 https://github.com/ros-drivers/joystick_drivers ${PROJECT_ROOT_DIR}/src/joystick_drivers
