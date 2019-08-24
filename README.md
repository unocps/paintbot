# research-project

## Setup
1. Run the `catkin_ws/setup.sh` script.
  * This ensures that the `catkin_ws/src/bricklayer_gazebo/models` directory is part of the `$GAZEBO_MODEL_PATH` by adding the appropriate export command to your `.bashrc`.
  * Remember to `source ~/.bashrc` after you run this command the first time.

## Building
1. Run `catkin_make` in the `catkin_ws` directory.
2. Run `source devel/setup.sh`.

## Running
1. Run `roslaunch bricklayer_gazebo bricklayer.launch`.
