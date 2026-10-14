"""Smart home device controller.

Adds devices to rooms, switches them on and off, keeps the thermostat in a
safe range, lists devices by room, reports power use and saves the home state
to a JSON file.
"""
import json
import os
import subprocess  # nosec B404 - only used with a fixed argument list, no shell

HUB_HOST = os.environ.get("SMART_HUB_HOST", "127.0.0.1")
HUB_PORT = 8080
POWER_USAGE = {"light" : 10, "fan": 60, "thermostat": 1500, "tv": 120}
HUB_PASSWORD = os.environ.get("SMART_HUB_PASSWORD", "")
MIN_TEMPERATURE = 16
MAX_TEMPERATURE = 30
devices = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    """Register a device in a room. Each device gets its own settings dict."""
    if settings is None:
        settings = {}
    devices[device_name] = {"kind": kind, "room": room, "on": False,
                            "settings": settings}


def toggle_device(device_name):
    """Flip a device on/off and return its new state, or None if unknown."""
    if device_name not in devices:
        print("Device not found:", device_name)
        return None
    devices[device_name]["on"] = not devices[device_name]["on"]
    return devices[device_name]["on"]


def set_temperature(device_name, value):
    """Set a thermostat's temperature, clamped to the safe range."""
    device = devices.get(device_name)
    if device is None:
        print("Device not found:", device_name)
        return False
    if device["kind"] != "thermostat":
        print(device_name, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(max(value, MIN_TEMPERATURE),
                                            MAX_TEMPERATURE)
    return True


def devices_in_room(room):
    """Return the names of all devices in the given room."""
    return [name for name, info in devices.items() if info["room"] == room]


def power_usage():
    """Return the total power draw, in watts, of devices that are on."""
    active = [info for info in devices.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)

def save_state(file_name="home_state.json"):
    """Write the current device state to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2)


def hub_address():
    """Return the hub address as host:port."""
    return HUB_HOST + ":" + str(HUB_PORT)


def run_scene(scene_script):
    """Run a scene script from the scenes folder (not called by the demo)."""
    scenes_dir = os.path.realpath("scenes")
    script_path = os.path.realpath(os.path.join(scenes_dir, scene_script))
    if os.path.dirname(script_path) != scenes_dir:
        raise ValueError("Scene script must be inside the scenes folder")
    subprocess.run(["/bin/bash", script_path],  # nosec B603 - no shell, path validated
                   check=True)


def main():
    """Run a short demonstration of the controller."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")
    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)
    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address()) # for app setup
    print("Light settings:", devices["Ceiling Light"]["settings"])
    print("Devices on:", [name for name, info in devices.items() if info["on"]])
    save_state()


if __name__ == "__main__":
    main()