# Pista Caudina

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![AC](https://img.shields.io/badge/assetto%20corsa-mod-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

Circuito kart a Montesarchio (BN), Campania. 860 m, larghezza 7.5 m, layout CW.

## Requisiti

- Python 3.10+, Blender 5.0+, Assetto Corsa (Steam)
- [blender-assetto-corsa-track-generator](../blender-assetto-corsa-track-generator/) clonato nella stessa cartella parent

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../blender-assetto-corsa-track-generator/requirements.txt
```

## Build e installazione

```bash
cd ../blender-assetto-corsa-track-generator

# Build
TRACK_ROOT=/path/to/montesarchio-track python3 build_cli.py

# Build + install in AC
TRACK_ROOT=/path/to/montesarchio-track python3 build_cli.py --install

# Solo install (senza rebuild)
TRACK_ROOT=/path/to/montesarchio-track python3 install.py
```

## GUI Manager

```bash
cd ../blender-assetto-corsa-track-generator
source ../montesarchio-track/.venv/bin/activate
python3 manager.py
```

## Struttura

```
pista_caudina.blend   Sorgente Blender
centerline.json       Dati layout v2 (road, cordoli, muri, start, map_center)
track_config.json     Configurazione pista
textures/             Texture (asphalt, curb, grass, barrier, startline, sponsor1)
cover.png             Copertina mod
```

## Parametri

| Parametro | Valore |
|-----------|--------|
| Lunghezza | 860 m |
| Larghezza | 7.5 m |
| Pit boxes | 10 |
| Layout | CW |
| Elementi extra | Gantry startline (portale con pannello sponsor + 5 luci rosse) |
| GPS | 41.0614, 14.6544 |
