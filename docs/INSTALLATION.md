# Installation Guide

This guide explains how to write the OpenCarDev Raspberry Pi image to an SD card or to an SSD and boot your Raspberry Pi. All instructions use British English and assume a Windows, macOS, or Linux host.

## What you need

- Raspberry Pi 4/5 (or 3B+ if supported by the chosen image)
- A microSD card (16GB or larger, Class 10/U3 recommended) or a USB SSD
- Image file from the release ending with `-opencardev`
- Card reader or USB-to-SATA enclosure for SSD

## Option A: Write to microSD card

1. Download the image ending with `-opencardev` and verify the SHA256 checksum provided in the release notes.
2. Use one of the following tools to flash the image:
   - Raspberry Pi Imager
   - balenaEtcher
   - `dd`/`usbimager` (advanced)
3. Safely eject the card, insert it into the Raspberry Pi, and power on.

### Raspberry Pi Imager (recommended)

1. Open Raspberry Pi Imager.
2. Choose OS > Use custom > select the downloaded image (`.img`, `.img.xz`, or `.zip`).
3. Choose Storage > select your microSD card.
4. Press Next and confirm to write.
5. After completion, remove the card safely.

### balenaEtcher

1. Open balenaEtcher.
2. Select image > choose the downloaded file.
3. Select target > your microSD card.
4. Flash and wait for verification to complete.

## Option B: Boot from USB SSD

Modern Raspberry Pi models support USB boot. Ensure your device firmware supports it:

- Raspberry Pi 4: USB boot supported with recent EEPROM. Update via Raspberry Pi Imager (Misc utility images > Bootloader > USB Boot) if needed.
- Raspberry Pi 5: USB boot supported.

### Flash the SSD

1. Connect your SSD to the host computer.
2. Use Raspberry Pi Imager or balenaEtcher to write the same `-opencardev` image to the SSD.
3. Safely eject the SSD and connect it to the Raspberry Pi’s USB 3 port (blue).
4. Power on the Raspberry Pi.

If the Pi still boots from microSD, remove the SD card to force USB boot, or set boot order in EEPROM.

## First boot

- Default hostname: `raspberrypi`
- SSH: enabled (see release notes or image defaults)
- Default user: `pi` / password: `raspberry` (change on first login)

## Verifying the image

On the host machine, run a SHA256 verification before flashing (examples):

- Windows (PowerShell):

```powershell
Get-FileHash .\image-name-opencardev.img.xz -Algorithm SHA256
```

- macOS/Linux:

```bash
sha256sum image-name-opencardev.img.xz
```

Compare the output with the checksum provided in the release notes.

## Troubleshooting

- If flashing fails, re-download the image and verify its checksum.
- Use a quality power supply (≥3A for Pi 4/5).
- Try a different USB port/cable for SSD issues.
- For Wi-Fi/Ethernet configuration, edit files in the boot partition (e.g., `wpa_supplicant.conf`) or use Raspberry Pi Imager’s OS customisation.

## Updating

When a new release is published, repeat the flashing process. For in-place updates, use standard Debian tools (`apt update && apt upgrade`) but note that core OS changes may still require re-imaging.
