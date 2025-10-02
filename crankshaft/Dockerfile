FROM --platform=linux/i386 debian:bookworm

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && \
    apt-get -y install \
        git vim parted \
        quilt coreutils qemu-user-static debootstrap zerofree zip dosfstools \
        e2fsprogs libarchive-tools libcap2-bin rsync grep udev xz-utils curl xxd file kmod bc \
        gpg pigz arch-test bmap-tools \
    && rm -rf /var/lib/apt/lists/*

COPY . /pi-gen/

VOLUME [ "/pi-gen/work", "/pi-gen/deploy"]
WORKDIR /pi-gen

USER root
