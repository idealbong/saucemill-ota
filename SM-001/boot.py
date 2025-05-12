import os
import json

DEVICE_JSON = "/device.json"
SAFE_BOOT_THRESHOLD = 3  # 최대 실패 허용 횟수
FIRMWARE_FILES = ["saucemill_firmware.mpy", "main.py", "boot.py", "manifest.json"]
BACKUP_DIR = "/backup"

def load_device_info():
    if DEVICE_JSON not in os.listdir("/"):
        return {}
    try:
        with open(DEVICE_JSON, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to read device.json: {e}")
        return {}

def save_device_info(info):
    try:
        with open(DEVICE_JSON, "w") as f:
            json.dump(info, f)
    except Exception as e:
        print(f"Failed to write device.json: {e}")
        
def rollback_firmware():
    """
    /backup 디렉토리에 저장된 모든 일반 파일을 루트 디렉토리로 복원합니다.
    """
    backup_dir = BACKUP_DIR

    try:
        files_to_restore = [
            f for f in os.listdir(backup_dir)
            if os.stat(f"{backup_dir}/{f}")[0] & 0o170000 == 0o100000  # 일반 파일만
        ]
    except Exception as e:
        print(f"⚠️ Failed to list backup dir: {e}")
        return

    for fname in files_to_restore:
        src = f"{backup_dir}/{fname}"
        dst = f"/{fname}"
        try:
            with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                while True:
                    chunk = fsrc.read(512)
                    if not chunk:
                        break
                    fdst.write(chunk)
            print(f"Rollback completed: {dst}")
        except Exception as e:
            print(f"⚠️ Rollback failed for {fname}: {e}")



def rollback_if_needed():
    info = load_device_info()
    state = info.get("boot", {})

    # ✅ 이전 부팅이 OTA 설치 후 부팅이면
    if state.get("mode") == "ota_pending":
        failures = state.get("failures", 0) + 1

        if failures >= SAFE_BOOT_THRESHOLD:
            print("⚠️ Too many failed boots after OTA. Rolling back firmware...")
            rollback_firmware()
        else:
            # 실패 횟수 기록
            state["failures"] = failures
            info["boot"] = state
            save_device_info(info)
            print(f"⚠️ OTA boot failure count: {failures}")


# 🔽 부팅 시 가장 먼저 실행
rollback_if_needed()
