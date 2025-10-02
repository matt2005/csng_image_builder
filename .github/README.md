# GitHub Actions Workflows

This directory contains GitHub Actions workflows for building the refactored crankshaft image.

## Workflows

### build-crankshaft-refactored.yml

Builds the refactored crankshaft image using the latest pi-gen structure.

#### Trigger Events

- **Manual Dispatch**: Run builds on-demand with configurable parameters
- **Push to main**: Automatic builds when crankshaft code changes
- **Pull Requests**: Validation builds for pull requests affecting crankshaft

#### Input Parameters

- **version**: Build version identifier (default: 'DEV')
- **target_arch**: Target architecture (armhf/arm64, default: armhf)
- **release**: Debian release (trixie/bookworm, default: trixie)

#### Build Process

1. **Environment Setup**
   - Ubuntu latest runner
   - QEMU for multi-architecture support
   - Docker Buildx
   - Disk space optimization

2. **Configuration**
   - Dynamic config generation based on inputs
   - Hardware feature enablement (I2C, SPI, UART)
   - Modern compression settings (xz)

3. **Build Execution**
   - Docker-based build using refactored structure
   - 8-hour timeout for complex builds
   - Comprehensive error handling

4. **Artifact Management**
   - Main image artifacts
   - Checksum files (MD5, SHA1, SHA256)
   - Build logs for debugging

5. **Release Creation** (conditional)
   - Automatic GitHub releases for 'csng' versions
   - Release notes with build information
   - All artifacts attached to release

#### Usage

##### Manual Build

```bash
# Navigate to Actions tab in GitHub
# Select "build-crankshaft-refactored" workflow
# Click "Run workflow"
# Configure parameters as needed
```

##### Automatic Build

Builds trigger automatically when:
- Code is pushed to main branch in `crankshaft/` directory
- Pull requests modify `crankshaft/` directory

#### Build Outputs

- **crankshaft-refactored-[date]-[version]**: Main build artifacts
- **build-logs-failure-[date]-[version]**: Logs if build fails

#### Configuration Files

The workflow generates a `config` file with:

```bash
IMG_NAME=crankshaft-[release]-[arch]
ENABLE_SSH=0
ARCH=[specified_architecture]
RELEASE=[specified_debian_release]
DEPLOY_COMPRESSION=xz
COMPRESSION_LEVEL=6
ENABLE_I2C=1
ENABLE_SPI=1
ENABLE_UART=1
STAGE_LIST="stage0 stage1 stage2 stage3 stage4"
```

#### Architecture Support

- **armhf**: 32-bit ARM (Raspberry Pi 2/3/4)
- **arm64**: 64-bit ARM (Raspberry Pi 4/5)

#### Security Considerations

- User credentials are commented out by default
- SSH is disabled by default
- Only essential services enabled

#### Troubleshooting

1. **Build Timeouts**: 8-hour limit for complex builds
2. **Disk Space**: Automatic cleanup of unnecessary packages
3. **Log Access**: Build logs uploaded as artifacts
4. **Version Conflicts**: Use unique version strings

#### Monitoring

The workflow includes notification steps for:
- ✅ Successful builds
- ❌ Failed builds with details

#### Related Documentation

- [Crankshaft Refactoring Notes](../crankshaft/REFACTORING_NOTES.md)
- [Build Configuration](../crankshaft/config.example)
- [Original Crankshaft Workflow](https://github.com/opencardev/crankshaft/.github/workflows/crankshaft.yml)