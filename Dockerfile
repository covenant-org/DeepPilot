ARG IMAGE="ros"
ARG TAG="noetic"

FROM fairbrook/${IMAGE}:${TAG}

ARG REMOTE_USER
ARG REMOTE_UID
ARG REMOTE_GID

RUN addgroup --gid ${REMOTE_GID} ${REMOTE_USER}
RUN adduser --disabled-password --uid ${REMOTE_UID} --gid ${REMOTE_GID} ${REMOTE_USER}

RUN  --mount=type=cache,target=/var/lib/apt/lists,id=apt_cache,sharing=locked \
     --mount=type=cache,target=/var/cache/apt,id=apt_cache,sharing=locked  \
 apt-get update && \
 apt-get install -y python3 python3-pip \
    bzr \
    openssh-client \
    subversion \
    procps \
    ca-certificates \
    gnupg \
    netbase \
    tzdata \
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
WORKDIR /workspaces

ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache  pip install -r requirements.txt

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
