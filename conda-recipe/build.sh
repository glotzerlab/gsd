mkdir build
cd build


if [ "$(uname)" == "Darwin" ]; then

#cmake ../ \
#      -DCMAKE_OSX_DEPLOYMENT_TARGET=10.8 \
#      -DCMAKE_CXX_FLAGS="-mmacosx-version-min=10.8" \
#      -DCMAKE_INSTALL_PREFIX=${SP_DIR} \
#      -DPYTHON_EXECUTABLE=${PYTHON}
#
#make install -j ${CPU_COUNT}

cd ..
python setup.py install

else
# Linux build
cmake ../ \
      -DCMAKE_INSTALL_PREFIX=${SP_DIR} \
      -DPYTHON_EXECUTABLE=${PYTHON}

make install -j ${CPU_COUNT}
fi
