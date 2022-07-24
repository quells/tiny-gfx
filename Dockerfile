FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update \
    && apt install -y \
    autoconf \
    bison \
    build-essential \
    clang \
    cmake \
    curl \
    flex \
    gawk \
    git \
    gperf \
    graphviz \
    libboost-filesystem-dev \
    libboost-iostreams-dev \
    libboost-program-options-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libeigen3-dev \
    libffi-dev \
    libftdi-dev \
    libgmp-dev \
    libreadline-dev \
    mercurial \
    pkg-config \
    python \
    python3 \
    python3-pip \
    tcl-dev \
    xdot \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN git clone --depth 1 https://github.com/YosysHQ/icestorm.git icestorm \
    && cd icestorm \
    && make -j$(nproc) \
    && make install

RUN git clone --depth 1 https://github.com/YosysHQ/nextpnr.git nextpnr \
    && cd nextpnr \
    && cmake -DARCH=ice40 -DCMAKE_INSTALL_PREFIX=/usr/local . \
    && make -j$(nproc) \
    && make install

RUN git clone --depth 1 https://github.com/YosysHQ/yosys.git yosys \
    && cd yosys \
    && make -j$(nproc) \
    && make install

RUN git clone --depth 1 https://github.com/YosysHQ/SymbiYosys.git SymbiYosys \
    && cd SymbiYosys \
    && make install

RUN git clone --depth 1 https://github.com/SRI-CSL/yices2.git yices2 \
    && cd yices2 \
    && autoconf \
    && ./configure \
    && make -j$(nproc) \
    && make install

RUN git clone --depth 1 https://github.com/Z3Prover/z3.git z3 \
    && cd z3 \
    && python scripts/mk_make.py \
    && cd build \
    && make -j$(nproc) \
    && make install

RUN pip3 install wheel \
    && pip3 install git+https://gitlab.com/nmigen/nmigen.git \
    && pip3 install git+https://gitlab.com/nmigen/nmigen-boards.git

WORKDIR /opt/tiny-gfx

COPY ./data data/
COPY ./src src/

CMD [ "python3", "./src/gfx.py" ]
