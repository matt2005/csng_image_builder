# Crankshaft Refactoring Documentation

## Overview

This document outlines the refactoring of the crankshaft project to align with the latest pi-gen repository structure from the Raspberry Pi Foundation.

## Refactoring Date

October 2, 2025

## Changes Made

### 1. Base Structure Update

- **Source**: Updated from pi-gen commit hash at time of refactoring
- **Target Structure**: Aligned with latest pi-gen repository structure
- **Location**: `image_builder/crankshaft/`

### 2. Build System Improvements

#### build.sh Updates
- Added space check in BASE_DIR path to prevent debootstrap issues
- Updated to use modern DEPLOY_COMPRESSION instead of deprecated DEPLOY_ZIP
- Added support for COMPRESSION_LEVEL configuration
- Improved error handling for non-executable run scripts
- Added term() function for proper cleanup
- Updated default IMG_NAME to reflect crankshaft branding

#### Configuration Updates
- Updated config.example with crankshaft-specific defaults
- Added DEPLOY_COMPRESSION=xz for better compression
- Set appropriate stage list for automotive use case
- Added hardware interface enablement (I2C, SPI, UART)
- Updated default release to 'trixie'

### 3. Docker Environment Updates

#### Dockerfile Improvements
- Updated base image from debian:buster to debian:bookworm
- Added modern dependencies: e2fsprogs, libarchive-tools, gpg, pigz, arch-test, bmap-tools
- Replaced deprecated bsdtar with libarchive-tools
- Added explicit WORKDIR and USER directives

### 4. Stage Preservation

- **stage3**: Preserved crankshaft-specific modifications including:
  - 02-pip-installs: Python package installations
  - 03-crankshaft-base: Core crankshaft system setup
  - 04-crankshaft-bluetooth: Bluetooth configuration for automotive use
  - 05-crankshaft-x11: X11 display system setup
  - 06-crankshaft-system-ro: Read-only file system configuration

- **stage4**: Preserved crankshaft-specific modifications including:
  - 01-armv7-fixes: ARM architecture specific fixes
  - EXPORT_IMAGE and EXPORT_NOOBS configurations

### 5. Script Updates

#### scripts/common
- Preserved all core functionality from latest pi-gen
- Maintained compatibility with crankshaft-specific requirements
- Updated mount handling and bootstrap processes

### 6. Key Benefits Achieved

1. **Maintainability**: Easier to track and merge upstream pi-gen changes
2. **Compatibility**: Better compatibility with latest Raspberry Pi OS features
3. **Security**: Updated to latest Debian base with security improvements
4. **Performance**: Improved compression and build optimization
5. **Modularity**: Cleaner separation between pi-gen core and crankshaft customizations

### 7. Breaking Changes

- Configuration file format updated (DEPLOY_ZIP → DEPLOY_COMPRESSION)
- Some environment variables have new defaults
- Docker base image updated (may require rebuild)

### 8. Migration Guide

#### For Existing Configurations
1. Update `config` file to use `DEPLOY_COMPRESSION` instead of `DEPLOY_ZIP`
2. Review and update any custom environment variables
3. Rebuild Docker containers to use new base image

#### Example Config Migration
**Before:**
```bash
DEPLOY_ZIP=0
```

**After:**
```bash
DEPLOY_COMPRESSION=none
```

### 9. Testing Status

- [ ] Build verification on target platforms
- [ ] Stage execution validation
- [ ] Docker container functionality
- [ ] Output image validation
- [ ] Hardware compatibility testing

### 10. Future Maintenance

- Regular upstream sync with pi-gen repository
- Preservation of crankshaft-specific modifications in dedicated stages
- Documentation updates for configuration changes
- Testing pipeline establishment

## Files Modified

### Core Build Files
- `build.sh` - Updated with latest pi-gen improvements
- `Dockerfile` - Modernized base image and dependencies
- `config.example` - Updated for crankshaft-specific defaults
- `README.md` - Updated documentation

### Preserved Crankshaft Files
- `stage3/` - All crankshaft-specific customizations
- `stage4/` - ARM fixes and export configurations
- `build-docker.sh` - Docker build script
- `code_of_conduct.md` - Project guidelines

### Generated Files
- This documentation file

## Contact

For questions about this refactoring, refer to the crankshaft project documentation at https://getcrankshaft.com/