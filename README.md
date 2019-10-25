# research-project

## Installation and Building
1. Run `rosdep install paintbot_description` and `rosdep install paintbot_gazebo`. This should install all dependencies.
2. Run `catkin build` from within the `catkin_ws` directory.

## Running
1. Source the development `setup.sh` file (e.g. `source catkin_ws/devel/setup.sh`).
    * Note that this only needs to be done once at the beginning of a working session. Each separate terminal session requires this, however.
2. Run `roslaunch paintbot_gazebo paintbot.launch`.

## Robot
The robot used is based directly on the Kuka Youbot model available from the default model database in Gazebo.

## Known Issues
The robot's turning doesn't behave exactly as desired due to the properties of the wheels and the controller used. The properties of the wheels have been manually tweaked as a temporary work around. To fix this, two steps should be taken:
1. The differential drive controller should be replaced by a controller or set of controllers that would allow the wheels to be properly modeled as mecanum wheels.
2. The properties of the wheels should be adjusted. The original values for these can be found in `paintbot_description/urdf/model.sdf`.
