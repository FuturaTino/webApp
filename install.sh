sudo conda deactivate && conda deactivate
# 更新软件包列表
sudo apt-get update
# 安装必要的软件包
sudo apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    ffmpeg \
    git \
    libatlas-base-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-program-options-dev \
    libboost-system-dev \
    libboost-test-dev \
    libhdf5-dev \
    libcgal-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libgflags-dev \
    libglew-dev \
    libgoogle-glog-dev \
    libmetis-dev \
    libprotobuf-dev \
    libqt5opengl5-dev \
    libsqlite3-dev \
    libsuitesparse-dev \
    nano \
    protobuf-compiler \
    python-is-python3 \
    # python3.10-dev \
    python3-pip \
    qtbase5-dev \
    sudo \
    vim-tiny \
    wget
# 清理缓存
sudo rm -rf /var/lib/apt/lists/*

# 克隆 glog 仓库
git clone --branch v0.6.0 https://github.com/google/glog.git --single-branch
cd glog
mkdir build
cd build
cmake ..
make -j $(nproc)
sudo make install
cd ../..
rm -rf glog
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib"

git clone --branch 2.1.0 https://ceres-solver.googlesource.com/ceres-solver.git --single-branch && \
cd ceres-solver && \
git checkout $(git describe --tags) && \
mkdir build && \
cd build && \
cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF && \
make -j `nproc` && \
make install && \
cd ../.. && \
rm -rf ceres-solver

export CUDA_ARCHITECTURES="90;89;86;80;75;70;61;52;37"
git clone --branch 3.8 https://github.com/colmap/colmap.git --single-branch && \
cd colmap && \
mkdir build && \
cd build && \
cmake .. -DCUDA_ENABLED=ON \
            -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCHITECTURES} && \
make -j $(nproc) && \
make install && \
cd ../.. && \
rm -rf colmap
