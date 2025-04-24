# 🔄 SauceMill OTA Repository

This repository stores **OTA (Over-The-Air) firmware update packages** for SauceMill Machines.

It is **publicly accessible**, so devices and users can download the latest firmware binaries and manifests securely and efficiently.

---

## 📦 Repository Structure

```text
/README.md                   # Project information
/Model_number                # Every Model Number has his own firmware
   ├── main.py               # MicroPython firmware main.py execution file
   ├── saucemill_firmware.mpy              # Compiled MicroPython firmware
   ├── manifest.json         # OTA metadata with version, SHA, signature

```

---

## 🚀 OTA Process Overview

1. Firmware is written and compiled using `mpy-cross`
2. `main.mpy` is signed with HMAC for integrity
3. A `manifest.json` file is generated:
   - `version` (Git tag)
   - `sha` (SHA1 hash of binary)
   - `signature` (HMAC-SHA256)
   - `timestamp`

4. Both files are committed and pushed to this repository

---

## 🔐 Security

- Firmware files are **HMAC-signed** using a machine-specific secret
- Only devices with valid secrets can verify and install OTA packages

---

## 🛠️ Publishing Workflow

Firmware maintainers should use the `publish_ota.py` script from the `saucemill-machine` repository:

```bash
python publish_ota.py
```

This will:

- Merge and compile firmware
- Generate `main.mpy` and `manifest.json`
- Push to this repository

---

## 📅 Versioning

This repository follows [semantic versioning](https://semver.org/) based on Git tags in the main firmware project.

Example:  

- Tag `v1.2.0` → `manifest.json.version = "v1.2.0"`

---

## 📄 License

This repository only contains compiled binaries.  
See the [SauceMill Machine repo](https://github.com/your-org/saucemill-machine) for source code and license.

---

🛡️ **Maintained by the SauceMill Device Team**
