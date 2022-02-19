# Working with ROS within Docker

This document is to make a note of how to work with ROS in docker in general, with a focus on utilizing ROS desktop applications as well.

# Building the image

The base image provided by OSRF (`osrf/ros`) has several tags. We'll be using the `noetic-desktop-full` tag so we get the current LTS version w/ desktop applications installed.

On its own, the default image may be all you need. At first, you can simply go ahead with this image and ignore this section. The base image has no controllers, however, or other important plugins that may be necessary to run your chosen ROS robot. To this end, you may find it necessary to install additional packages and create a custom variant of this image. This can be done by creating a `Dockerfile` and modifying this image.

In this example, we have a `Dockerfile` that installs joint effort, state, and position controllers, as well as some additional packages.

```
FROM osrf/ros:noetic-desktop-full

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
```

I could then build this docker file via `docker build . -t <image-name>` and then utilize the resulting image (referenced by it's tag/name) in any of the following commands in lieu of `osrf/ros:noetic-desktop-full`.

## Committing manually

If you have manually worked in a container and wish to save your current state of the container as an image you can relaunch, then note you can always use `docker commit <container-id> <image-name>` to create a new image.

# Starting a container
Typically it's best to start our ROS container with `roscore`. While `roslaunch` will take care of `roscore` typically, we'll demonstrate with `roscore`.

Typically, a simple run would be `docker run <image-name> <command>`, so in our case `docker run roscore`. This works, but we can add additional settings to this. We need to modify this command to take account of networking, access to files, and setting up for user sharing.

There is a significant amount that can be said for docker networking that is beyond the scope of what I wish to discuss here. What I will say that there is a likelihood that you will wish to run code natively outside of docker that connects to your docker container. The simplest way to achieve this is to append a `--net=host` to your command. This has the docker act as if it is running on your computer's local network, allowing easier integration without having to handle exposing specific ports.

It is likely that we wish to have the files that we are working on be accessed within the container. For a finished product we may choose to copy these files into the container via the `COPY` directive in the Dockerfile. This process can become tedious during development, however, with rapidly changing files. To this end it's likely easier to have the docker container have access to your files as if it was locally available. To this end we can mount the folder as a volume. The format for this is `host_folder:container_folder`. An example - `docker run --volume "/home/keith/projects/ros-project:/ros-project osrf/ros:noetic-desktop-full` will mount the files in the `ros-project` folder on the host machine at `/ros-project` in the container. If you wish to prevent these files from being modified, you can specify a read-only safety option by doing `--volume "/home/keith/projects/ros-project:/ros-project:ro`.

When you run a container, it is ephermeral; but you may wish to restart the container instead of creating a new one. Perhaps you want to have a more direct name for the container so you can easily refer to it. Give your container a name with `--name <name>` to reuse the container easily in the future. Thus `docker run --name=rbe550-hw1 osfr/ros:noetic-desktop-full roscore` will create a container of the name `rbe550-hw1`. If I kill this container I can simply run `docker start rbe550-hw1` and the `roscore` command in that container will start up again. `docker stop rbe550-hw1` will stop the container. Note that docker containers without mounts are ephermeral - there is no shared memory between container runs.

This finally leaves us to a useful collection of commands for our setup:

`docker run --name=rbe550-project --net=host --volume="/home/$(whoami)/projects/rbe550-project:/app" osrf/ros:noetic-desktop-full roscore`
...and later we can relaunch this with `docker start rbe550-project` - how nice and neat!

## For extreme scenarios

Depending on what you wish to do, you may wish to connect your user environment fully through to the container. I do not recommend this, but it may help you do some commands that require escalation. This does leave you at risk for the container affecting your host machine, which breaks several tenants of properly using containers. I leave this here in case you get stuck, but please consider what you're doing. The following command will connect your linux user ID to your running docker container ID, share your home directory to make use of your linux user's default settings, and inject your sudoers information in to give you admin control.

`docker run --name=<image-name> -it --net=host --user=$(id -u $USER):$(id -g $USER)  --volume="/home/$(whoami):/home/$(whoami)"  --volume="/etc/group:/etc/group:ro" --volume="/etc/passwd:/etc/passwd:ro" --volume="/etc/shadow:/etc/shadow:ro" --volume="/etc/sudoers.d:/etc/sudoers.d:ro" osrf/ros:noetic-desktop-full roscore`

# Bash

Ok, we have `roscore` running, but what if I wanted to load a bash shell to execute other ROS applications? For this section we will assume that our container has been named rbe550-project. We can execute commands on a running container via `exec`:

`docker exec rbe550-project <command>`

If we wanted a bash shell that we can control, we can utilize `-it` to create an interactive terminal:

`docker exec -it rbe550-project bash`

The `osrf/ros` image assumes that you source `/ros_entrypoint.sh` in order to utilize many ROS applications like `roslaunch` or `rostopic`. Likewise, it is annoying to have to remember to execute this program repeatedly for every terminal we create. To this end we can chain commands by cheating:

`docker exec -it rbe550-project bash -c "source /ros_entrypoint.sh; bash"`

...this will run our container, run bash, run this series of commands including our sourcing, and then finally execute bash. Taking this a step forward, let's say we had a volume setup such that our code was mounted via `--volume=/home/keith/projects/rbe550-project:/app`, we migh want to change directory to that, too. Taking this a step forward, if we had a `catkin_ws` within that we wish to source the `devel/setup.bash` for to load our custom ROS modules into as well...

`docker exec -it rbe550-project bash -c "source /ros_entrypoint.sh; cd /app; source catkin_ws/devel/setup.bash; bash"`

This can all get aliased to a simple command or shell script for ease of use.

docker exec --env="DISPLAY" --env="QT_X_NO_MITSHM=1" -it ros-with-controllers2 bash -c "source /ros_entrypoint.sh; cd $(pwd); bash"


# Graphical pass through

Not all of what we wish to use for ROS is terminal based - we need GUI'ed applications to boot! If you're in linux, this is pretty easy to get working! We can gain X11 passthrough by adding `--env="DISPLAY" --env="QT_X_NO_MITSHM=1"` to our `exec`: `docker exec --env="DISPLAY" --env="QT_X_NO_MITSHM=1" -it rbe550-project bash -c "source /ros_entrypoint.sh; cd $(pwd); bash"` ...for example.