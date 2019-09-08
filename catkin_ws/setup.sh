#!/bin/bash

models_dir=$(dirname $(realpath setup.sh))
echo 'export GAZEBO_MODEL_PATH='$models_dir'/src/paintbot_gazebo/models/:$GAZEBO_MODEL_PATH' >> ~/.bashrc
