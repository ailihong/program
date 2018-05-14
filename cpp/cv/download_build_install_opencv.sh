#!/bin/bash

apt-get update && apt-get install -y --no-install-recommends \
# to build and install
unzip \
build-essential cmake pkg-config \
# to work with images
libjpeg-dev libtiff-dev libjasper-dev libpng-dev \
# to work with videos
libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
libxvidcore-dev libx264-dev \
# needed by highgui tool
libgtk2.0-dev libgtk-3-dev \
# for opencv math operations
libatlas-base-dev gfortran \
# others
libtbb2 libtbb-dev python2.7-dev \
# cleanup
&& rm -rf /var/lib/apt/lists/* \
&& apt-get -y autoremove

pip install --no-cache-dir \
# OpenCV dependency
numpy \
# other usefull stuff
#ipython \
# cleanup
&& find /usr/local \
\( -type d -a -name test -o -name tests \) \
-o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
-exec rm -rf '{}' + \
&& cd / \
&& rm -rf /usr/src/python ~/.cache

# Install OpenCV
OPENCV_VERSION=3.4.0

WS_DIR=`pwd`
mkdir opencv
cd opencv

# download OpenCV and opencv_contrib
wget -O opencv.zip https://github.com/Itseez/opencv/archive/$OPENCV_VERSION.zip
unzip opencv.zip
rm -rf opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/$OPENCV_VERSION.zip
unzip opencv_contrib.zip
rm -rf opencv_contrib.zip

OPENCV_SRC_DIR=`pwd`/opencv-$OPENCV_VERSION
OPENCV_CONTRIB_MODULES_SRC_DIR=`pwd`/opencv_contrib-$OPENCV_VERSION/modules

# build and install
cd $OPENCV_SRC_DIR
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=$OPENCV_CONTRIB_MODULES_SRC_DIR \
  -D BUILD_TESTS=OFF \
  -D INSTALL_PYTHON_EXAMPLES=OFF \
  -D INSTALL_C_EXAMPLES=OFF \
  -D USE_V4L=ON \
  -D ENABLE_CXX11=ON \
  -D BUILD_EXAMPLES=OFF ..

make -j4			

make install
ldconfig

# verify the installation is successful
python -c "import cv2; print('Installed OpenCV version is: {} :)'.format(cv2.__version__))"
if [ $? -eq 0 ]; then
    echo "OpenCV installed successfully! ........................."
else
    echo "OpenCV installation failed :( ........................."
    SITE_PACKAGES_DIR=/usr/local/lib/python2.7/site-packages
    echo "$SITE_PACKAGES_DIR contents: "
    echo `ls -ltrh $SITE_PACKAGES_DIR`
    echo "Note: temporary installation dir $WS_DIR/opencv is not removed!"
    exit 1
fi

# cleanup
cd $WS_DIR
rm -rf opencv
