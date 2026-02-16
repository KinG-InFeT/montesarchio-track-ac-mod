#!/usr/bin/env python3
"""
Create the complete Assetto Corsa mod folder structure and config files
for Pista Caudina di Montesarchio.
"""

import os
import json
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
MOD_DIR = os.path.join(ROOT_DIR, "mod", "pista_caudina")

# Load track config (if available)
CONFIG_PATH = os.path.join(ROOT_DIR, "track_config.json")
_config = {}
if os.path.isfile(CONFIG_PATH):
    with open(CONFIG_PATH) as _f:
        _config = json.load(_f)
_surfaces = _config.get("surfaces", {})
_info = _config.get("info", {})


def create_directories():
    """Create the mod folder structure."""
    dirs = [
        os.path.join(MOD_DIR, "ai"),
        os.path.join(MOD_DIR, "data"),
        os.path.join(MOD_DIR, "ui"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("  Created directory structure")



def write_surfaces_ini():
    """Write data/surfaces.ini — surface physics definitions."""
    road_friction = _surfaces.get("road_friction", 0.97)
    kerb_friction = _surfaces.get("kerb_friction", 0.93)
    grass_friction = _surfaces.get("grass_friction", 0.60)

    path = os.path.join(MOD_DIR, "data", "surfaces.ini")
    content = f"""\
[SURFACE_0]
KEY=ROAD
FRICTION={road_friction}
DAMPING=0.0
WAV=
WAV_PITCH=0
FF_EFFECT=NULL
DIRT_ADDITIVE=0.0
IS_VALID_TRACK=1
IS_PITLANE=0
BLACK_FLAG_TIME=0.0
SIN_HEIGHT=0
SIN_LENGTH=0
VIBRATION_GAIN=0
VIBRATION_LENGTH=0

[SURFACE_1]
KEY=KERB
FRICTION={kerb_friction}
DAMPING=0.0
WAV=kerb
WAV_PITCH=1
FF_EFFECT=KERB
DIRT_ADDITIVE=0.0
IS_VALID_TRACK=1
IS_PITLANE=0
BLACK_FLAG_TIME=0.0
SIN_HEIGHT=0.005
SIN_LENGTH=0.15
VIBRATION_GAIN=0.5
VIBRATION_LENGTH=0.15

[SURFACE_2]
KEY=GRASS
FRICTION={grass_friction}
DAMPING=0.1
WAV=grass
WAV_PITCH=0
FF_EFFECT=GRASS
DIRT_ADDITIVE=0.5
IS_VALID_TRACK=0
IS_PITLANE=0
BLACK_FLAG_TIME=3.0
SIN_HEIGHT=0
SIN_LENGTH=0
VIBRATION_GAIN=0.2
VIBRATION_LENGTH=0.5

[SURFACE_3]
KEY=WALL
FRICTION=0.365
DAMPING=0.0
WAV=
WAV_PITCH=0
FF_EFFECT=NULL
DIRT_ADDITIVE=0.0
IS_VALID_TRACK=0
IS_PITLANE=0
BLACK_FLAG_TIME=0.0
SIN_HEIGHT=0
SIN_LENGTH=0
VIBRATION_GAIN=0.05
VIBRATION_LENGTH=0.05

[SURFACE_4]
KEY=PIT
FRICTION=0.97
DAMPING=0.0
WAV=
WAV_PITCH=0
FF_EFFECT=NULL
DIRT_ADDITIVE=0.0
IS_VALID_TRACK=1
IS_PITLANE=1
BLACK_FLAG_TIME=0.0
SIN_HEIGHT=0
SIN_LENGTH=0
VIBRATION_GAIN=0
VIBRATION_LENGTH=0

[SURFACE_5]
KEY=GROUND
FRICTION={grass_friction}
DAMPING=0.15
WAV=grass
WAV_PITCH=0
FF_EFFECT=GRASS
DIRT_ADDITIVE=0.5
IS_VALID_TRACK=0
IS_PITLANE=0
BLACK_FLAG_TIME=3.0
SIN_HEIGHT=0
SIN_LENGTH=0
VIBRATION_GAIN=0.3
VIBRATION_LENGTH=0.5
"""
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Written {path}")


def write_cameras_ini():
    """Write data/cameras.ini — 6 replay cameras around the circuit."""
    path = os.path.join(MOD_DIR, "data", "cameras.ini")
    # HEADER section required by AC
    content = """\
[HEADER]
VERSION=2
CAMERA_COUNT=6
SET_NAME=replay


[CAMERA_0]
NAME=Start/Finish
POSITION=5.0, 3.0, 0.0
FORWARD=0.0, -0.3, 1.0
FOV=56.0
NEAR=0.1
FAR=800.0
MIN_DISTANCE=3.0
MAX_DISTANCE=120.0

[CAMERA_1]
NAME=Curva 1
POSITION=-30.0, 4.0, 50.0
FORWARD=0.5, -0.3, -0.5
FOV=50.0
NEAR=0.1
FAR=800.0
MIN_DISTANCE=3.0
MAX_DISTANCE=100.0

[CAMERA_2]
NAME=Tornante Nord
POSITION=-50.0, 5.0, 100.0
FORWARD=0.7, -0.3, -0.3
FOV=48.0
NEAR=0.1
FAR=800.0
MIN_DISTANCE=3.0
MAX_DISTANCE=100.0

[CAMERA_3]
NAME=Chicane
POSITION=20.0, 3.5, 80.0
FORWARD=-0.5, -0.2, -0.5
FOV=52.0
NEAR=0.1
FAR=800.0
MIN_DISTANCE=3.0
MAX_DISTANCE=100.0

[CAMERA_4]
NAME=Curva Sud
POSITION=40.0, 4.0, -20.0
FORWARD=-0.6, -0.3, 0.4
FOV=50.0
NEAR=0.1
FAR=800.0
MIN_DISTANCE=3.0
MAX_DISTANCE=100.0

[CAMERA_5]
NAME=Panoramica
POSITION=0.0, 25.0, 50.0
FORWARD=0.0, -0.8, -0.2
FOV=70.0
NEAR=0.1
FAR=1200.0
MIN_DISTANCE=5.0
MAX_DISTANCE=200.0
"""
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Written {path}")


def write_map_ini():
    """Write data/map.ini — minimap configuration."""
    path = os.path.join(MOD_DIR, "data", "map.ini")
    content = """\
[PARAMETERS]
WIDTH=250
HEIGHT=350
MARGIN=20
SCALE_FACTOR=1.0
X_OFFSET=0.0
Z_OFFSET=0.0
DRAWING_SIZE=10
"""
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Written {path}")


def write_ui_track_json():
    """Write ui/ui_track.json — track metadata for AC UI."""
    name = _info.get("name", "Pista Caudina")
    city = _info.get("city", "Montesarchio")
    country = _info.get("country", "Italy")
    length = str(_info.get("length", "860"))
    pitboxes = str(_info.get("pitboxes", "10"))
    direction = _info.get("direction", "clockwise")
    _geo = _config.get("geometry", {})
    road_w = _geo.get("road_width", 7.5)

    path = os.path.join(MOD_DIR, "ui", "ui_track.json")
    data = {
        "name": name,
        "description": f"Circuito kart {name} di {city} (BN), Campania. "
                       f"Tracciato tecnico con 9 curve su {length} metri.",
        "tags": ["circuit", "kart", "italy", "short"],
        "geotags": ["41.0614", "14.6544"],
        "country": country,
        "city": city,
        "length": length,
        "width": f"{road_w:.0f}-{road_w + 1:.0f}",
        "pitboxes": pitboxes,
        "run": direction,
        "author": "Bros on Trucks Team",
        "version": "1.3.0"
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Written {path}")


def write_lighting_ini():
    """Write data/lighting.ini — sun position."""
    path = os.path.join(MOD_DIR, "data", "lighting.ini")
    content = """\
[LIGHTING]
SUN_PITCH_ANGLE=45
SUN_HEADING_ANGLE=45
"""
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Written {path}")


def write_groove_ini():
    """Write data/groove.ini — rubber groove config."""
    path = os.path.join(MOD_DIR, "data", "groove.ini")
    content = """\
[HEADER]
GROOVES_NUMBER=0
"""
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Written {path}")


def copy_layout_as_map():
    """Copy layout.png as map.png for the track minimap."""
    src = os.path.join(ROOT_DIR, "layout.png")
    dst = os.path.join(MOD_DIR, "map.png")
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"  Copied layout.png → map.png")

    # Copy cover.png as ui/preview.png and ui/outline.png
    cover = os.path.join(ROOT_DIR, "cover.png")
    if os.path.exists(cover):
        for name in ["outline.png", "preview.png"]:
            dst2 = os.path.join(MOD_DIR, "ui", name)
            shutil.copy2(cover, dst2)
            print(f"  Copied cover.png → ui/{name}")


def main():
    print("Setting up Assetto Corsa mod folder...")

    create_directories()
    # Note: models.ini is NOT needed - AC auto-detects KN5 by folder name
    # Working mod tracks (driftplayground, roc) don't use models.ini
    write_surfaces_ini()
    write_cameras_ini()
    write_map_ini()
    write_lighting_ini()
    write_groove_ini()
    write_ui_track_json()
    copy_layout_as_map()

    print(f"\nMod structure created at: {MOD_DIR}")


if __name__ == "__main__":
    main()
