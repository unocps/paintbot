#!/bin/bash

ws_dir=$(dirname $(realpath setup.sh))
export GAZEBO_MODEL_PATH="$ws_dir"/src/paintbot_gazebo/models/:$GAZEBO_MODEL_PATH
