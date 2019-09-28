# research-project

## Building
1. Run `catkin_make` in the `catkin_ws` directory.
2. Run `source catkin_ws/devel/setup.sh`.
3. Run `source catkin_ws/setup.sh` script.
  * This ensures that the `catkin_ws/src/paintbot_gazebo/models` directory is part of the `$GAZEBO_MODEL_PATH`.

## Running
1. Run `roslaunch paintbot_gazebo paintbot.launch`.

## Robot
The robot used is based directly on the Kuka Youbot model available from the default model database in Gazebo.

## Known Issues
The robot's turning doesn't behave exactly as desired due to the properties of the wheels and the controller used. The properties of the wheels have been manually tweaked as a temporary work around. To fix this, two steps should be taken:
1. The differential drive controller should be replaced by a controller or set of controllers that would allow the wheels to be properly modeled as mecanum wheels.
2. The properties of the wheels should be adjusted. The original values for these can be found in `paintbot_description/urdf/model.sdf`.
