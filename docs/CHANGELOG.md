# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning where practical.

## [Unreleased]

- Add new features and fixes here.

## [2025-11-02] Initial refactor and release automation

### Added

- Stage60 to add OpenCarDev apt repository and reliability config.
- Pi-gen build workflow for lite images (armhf, arm64).
- Release workflow that triggers on successful builds, filters `-opencardev` images, computes SHA256, and publishes a GitHub Release with notes.
- Installation guide for SD card and SSD boot.

### Changed

- Build workflow updated to copy custom stage and include stage60 in STAGE_LIST.

### Removed

- N/A
