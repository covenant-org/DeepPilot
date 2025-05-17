FROM fairbrook/ros-cuda:noetic-cuda12.8

ARG REMOTE_USER
ARG REMOTE_UID
ARG REMOTE_GID

RUN addgroup --gid ${REMOTE_GID} ${REMOTE_USER}
RUN adduser --disabled-password --uid ${REMOTE_UID} --gid ${REMOTE_GID} ${REMOTE_USER}

RUN  --mount=type=cache,target=/var/lib/apt/lists,id=apt_cache,sharing=locked \
     --mount=type=cache,target=/var/cache/apt,id=apt_cache,sharing=locked  \
     apt-get update && \
     apt-get install -y python3 python3-pip \
        wget \
	unzip \
	build-essential \
	python3-rosdep \
	python3-catkin-tools \
	git \
	libusb-dev \
	python3-osrf-pycommon \
	libspnav-dev \
	libbluetooth-dev \
	libcwiid-dev \
	libgoogle-glog-dev \
	ros-noetic-mavros \
	ros-noetic-octomap-ros \
	software-properties-common && \
     add-apt-repository ppa:rock-core/qt4 && \
     apt-get update && \
     apt-get install -y qt4-default

RUN echo "%sudo	ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN usermod -aG sudo ${REMOTE_USER}

ENV HOME /home/${REMOTE_USER}
USER ${REMOTE_USER}

WORKDIR /workspace
RUN mkdir -p /workspace/src/

RUN git clone https://github.com/ethz-asl/mav_comm /workspace/src/mav_comm
RUN git clone -b noetic https://github.com/simonernst/iROS_drone /workspace/src/iROS_drone
RUN git clone -b ros1 https://github.com/ros-drivers/joystick_drivers /workspace/src/joystick_drivers

COPY ./gazebo_models/* /root/.gazebo/models
COPY ./launch/* ./src/iROS_drone/rotors_simulator/rotors_gazebo/launch
COPY ./adr_worlds ./src/iROS_drone/rotors_simulator/rotors_gazebo/adr_worlds
COPY ./keyboard ./src/keyboard
COPY DeepPilot_network ./DeepPilot_network

USER root
RUN chown ${REMOTE_USER}:${REMOTE_USER} -R /workspace
USER ${REMOTE_USER}

ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache  pip install -r requirements.txt

RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

ENTRYPOINT ["/bin/bash"]
