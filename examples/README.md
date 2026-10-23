# Configuration examples

Copy one JSON file to the project root as `config.json`, then edit it. Paths and device addresses are illustrative, not autodetected values. Never overwrite an existing configuration without keeping a backup.

- `generic.json`: all vendors, manual Android startup, automatic single-device selection.
- `android-studio.json`: SDK `emulator` must be on PATH; replace YOUR_AVD_NAME and check the emulator serial. Android image/game ABI compatibility is your responsibility.
- `mumu-windows.json`: optional MuMuManager startup; change install path, instance number and ADB port.
- `vendor-tcp.json`: BlueStacks/LDPlayer/Nox/Genymotion or another TCP-connected environment. Set the actual ADB binary and TCP port; 5555 is only an example.
- `waydroid.json`: replace the example address with your running Android container's actual ADB address. ARM compatibility and reverse forwarding must be available.
- `usb-device.json`: replace YOUR_DEVICE_SERIAL with the ID from `adb devices` and authorize USB debugging.

These examples describe ADB integration. They are not device or game-compatibility certifications.
