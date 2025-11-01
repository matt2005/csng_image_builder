1. Use RPI imager to deploy latest image to ssd/sd.
   1. Apply any customisations such as ssh keys and hostname using the imager
2. Boot wait about 10 mins. If using a raspberry pi5 ensure that you are using the genuine power supply 47w?
3. connect to the pi using vscode remote ssh.
   1. Let vscode install the server, takes about 10 mins.
4. install git
   1. sudo apt install git -y
5. Increase swap to 4GB
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```
6. AASDK
   1. Clone AASDK
```bash
git clone git@github.com:opencardev/aasdk.git -b bugfix/boost
```
   1. Switchto AASDK Src
```bash
cd aasdk
``` 
   1. Build AASDK
```bash
# Install dependencies
sudo apt update && sudo apt install -y \
    build-essential cmake git pkg-config \
    libboost-all-dev libusb-1.0-0-dev libssl-dev \
    libprotobuf-dev protobuf-compiler

# Build
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
```
   4. Create deb package for aadsk
```bash
cpack --config CPackConfig.cmake
```
   5. Install deb package
``bash
sudo dpkg -i /home/pi/aasdk/build/libaasdk-arm64_2025.10.05+git.d25e56e_arm64.deb
sudo dpkg -i /home/pi/aasdk/build/libaasdk-arm64-dev_2025.10.05+git.d25e56e_arm64.deb 
```
   6. s 
1. Openauto
   1. git clone git@github.com:opencardev/openauto.git -b crankshaft-ng_2025
   2. ./build-packages.sh --release-only