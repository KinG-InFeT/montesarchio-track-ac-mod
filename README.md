# Pista Caudina - Mod Track per Assetto Corsa

**v1.3.0**

Circuito kart **Pista Caudina** di Montesarchio (BN), Campania.
Tracciato tecnico con 9 curve su 860 metri, larghezza 7-8m.

Mod per Assetto Corsa (versione 2019 - v1.16.x). Supporta Linux (Steam/Proton) e Windows.

## Requisiti

| Requisito | Linux | Windows |
|-----------|-------|---------|
| Python | 3.10+ | 3.10+ |
| Blender | 5.0+ (snap o PATH) | 5.0+ (installer o PATH) |
| Assetto Corsa | Steam / Proton | Steam nativo |
| Content Manager | Sostituzione launcher | Copia exe |
| CSP | dwrite.dll + extension/ | dwrite.dll + extension/ |
| Font di sistema | Necessari (ac-fonts.zip) | Gia' presenti |

### Setup Python virtualenv

**Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Manager (GUI) — modo raccomandato

Il Manager (`manager.py`) e' il punto di ingresso principale del progetto: un'applicazione PyQt5
cross-platform (Linux e Windows) che gestisce l'intero ciclo di vita della mod, dalla build
all'installazione in Assetto Corsa.

**Linux:**
```bash
source .venv/bin/activate
python manager.py
```
**Windows:**
```cmd
.venv\Scripts\activate
python manager.py
```

Il Manager ha 4 tab:

- **Preview 3D** — Viewer OpenGL integrato che mostra il KN5 della pista senza aprire AC.
  Visualizza mesh, texture, empty AC (start, pit, timing) con indicatori colorati.
  Permette di nascondere/mostrare singole mesh, salvare e caricare posizioni camera.
  All'avvio esegue automaticamente l'export KN5 per avere sempre la preview aggiornata al .blend.

- **Build** — Esegue la pipeline di build in 3 step con output in tempo reale:
  1. Export KN5 da Blender (converte la scena .blend in formato nativo AC)
  2. Setup struttura mod (genera surfaces.ini, cameras.ini, ui_track.json, ecc.)
  3. Generazione AI line (estrae la centerline dal mesh 1ROAD per fast_lane.ai)

  Il pulsante "Build All" li esegue tutti in sequenza; ogni step puo' anche essere lanciato singolarmente.
  Al termine copia il KN5 nella cartella mod e ricarica la preview 3D.

- **Install** — Installa la mod e i componenti aggiuntivi in Assetto Corsa, senza dipendenze bash.
  Rileva automaticamente il percorso di AC (Steam su Linux e Windows, multi-drive).
  Checkbox per selezionare cosa installare:
  - **Pista Caudina** — copia la cartella mod in `content/tracks/`
  - **Pulizia cache** — rimuove cache AC (ai_grids, ai_payloads, meshes_metadata) e cache CM
  - **Content Manager** — cerca/scarica zip, estrae exe; su Linux lo imposta come launcher Steam
  - **Custom Shaders Patch** — cerca/scarica zip, estrae dwrite.dll e extension/
  - **Font di sistema** — installa verdana.ttf, segoeui.ttf (solo Linux, su Windows gia' presenti)

  I download avvengono in Python puro (urllib + zipfile), senza curl/unzip.
  L'installazione gira in un thread separato per non bloccare la GUI.

- **Parametri** — Editor per i parametri della pista (geometria, AI line, superfici, info).
  Salva e carica da `track_config.json`, usato da `setup_mod_folder.py` per generare i file di configurazione.

## Workflow

Il file Blender `pista_caudina.blend` e' il sorgente principale della pista.
Tutte le modifiche alla geometria, materiali, empty e texture si fanno direttamente in Blender.

La pipeline di build ha **3 step** (gestiti dal Manager, da `build_cli.py`, o eseguibili manualmente):

1. **Export KN5** — converte la scena Blender in formato KN5 nativo di AC (senza Wine o ksEditor)
2. **Setup mod folder** — crea/aggiorna la struttura della cartella mod (data, ui, ai)
3. **AI line** — genera `fast_lane.ai` estraendo la centerline dal mesh `1ROAD` (bordi boundary inner/outer -> punti medi, direzione CW, inizio da `AC_START_0`)

### Build CLI (cross-platform)

`build_cli.py` esegue tutti e 3 gli step + copia KN5 nella mod da terminale:

```bash
python build_cli.py
```

Su Linux e' disponibile anche `build.sh` che fa la stessa cosa in bash.

### Step manuali

Se si preferisce eseguire i singoli step da terminale:

```bash
# Step 1 - Export KN5
blender --background pista_caudina.blend --python scripts/export_kn5.py

# Step 2 - Setup mod folder (Linux)
.venv/bin/python scripts/setup_mod_folder.py
# Step 2 - Setup mod folder (Windows)
.venv\Scripts\python scripts\setup_mod_folder.py

# Step 3 - AI line
blender --background pista_caudina.blend --python scripts/generate_ai_line.py

# Copia KN5 nella mod
cp pista_caudina.kn5 mod/pista_caudina/pista_caudina.kn5
```

## Installazione in Assetto Corsa

Il modo raccomandato e' usare il tab **Install** del Manager (vedi sopra).

In alternativa su Linux e' disponibile lo script bash:

```bash
bash install.sh
# oppure con percorso AC non standard:
AC_DIR=/percorso/ad/assettocorsa bash install.sh
```

### Componenti installati

- **Pista Caudina** — il circuito (copiato in `content/tracks/pista_caudina/`)
- **Content Manager** — launcher alternativo (su Linux viene impostato come launcher Steam)
- **Custom Shaders Patch** — miglioramenti grafici (dwrite.dll + extension/)
- **Font di sistema** — verdana.ttf, segoeui.ttf (solo Linux, su Windows sono gia' presenti)
- **Pulizia cache** — AC engine cache (ai_grids, ai_payloads, meshes_metadata) + CM cache

### Content Manager e CSP

Se mancano, scaricarli da:
- **Content Manager:** https://acstuff.ru/app/
- **CSP:** https://acstuff.club/patch/

Salvare i .zip in `addons/`, nella root del progetto, o in `~/Scaricati/` (`~/Downloads` su Windows).
L'installer (Manager o `install.sh`) li cerca automaticamente in queste posizioni; se non li trova, li scarica.

## Verifica

1. Avviare Assetto Corsa
2. Selezionare "Pista Caudina" dal menu
3. Verificare:
   - L'auto parte al centro della strada, in senso orario
   - La pista si carica senza cadere nel vuoto
   - I cordoli sono nelle curve
   - Le superfici hanno il comportamento fisico corretto (asfalto, erba, cordoli)

## Track Viewer 3D

Viewer 3D interattivo per visualizzare i file KN5 senza aprire Assetto Corsa.

**Linux:**
```bash
source .venv/bin/activate
python tools/track_viewer.py mod/pista_caudina/pista_caudina.kn5
```
**Windows:**
```cmd
.venv\Scripts\activate
python tools\track_viewer.py mod\pista_caudina\pista_caudina.kn5
```

Controlli camera:
- **Click sinistro + drag**: orbita attorno alla pista
- **Click destro + drag**: pan
- **Rotella mouse**: zoom
- **Tasto R**: reset camera

## Struttura del progetto

```
montesarchio-track/
├── pista_caudina.blend         # Sorgente Blender (geometria, materiali, empty)
├── pista_caudina.kn5           # Modello 3D formato AC (generato)
├── track_config.json           # Configurazione camera e parametri
├── requirements.txt            # Dipendenze Python (numpy, Pillow, PyQt5, PyOpenGL)
├── manager.py                  # Manager GUI (build, preview, installazione) - cross-platform
├── build_cli.py                # Build CLI cross-platform (alternativa a build.sh)
├── build.sh                    # Build completa da CLI (solo Linux)
├── install.sh                  # Installazione mod + addon da CLI (solo Linux)
├── layout.png                  # Immagine sorgente del tracciato (usata come map.png)
├── cover.png                   # Immagine copertina (preview + outline in AC)
├── scripts/
│   ├── export_kn5.py           # Step 1: esporta KN5 da Blender (script Blender)
│   ├── setup_mod_folder.py     # Step 2: crea struttura mod AC
│   ├── generate_ai_line.py     # Step 3: genera AI driving line (script Blender)
│   └── platform_utils.py       # Utility cross-platform (Blender, venv, path AC)
├── textures/
│   ├── asphalt.png             # Texture asfalto (1024x1024)
│   ├── curb_rw.png             # Texture cordolo rosso/bianco (256x256)
│   ├── grass.png               # Texture erba (1024x1024)
│   ├── barrier.png             # Texture barriera (512x512)
│   ├── startline.png           # Texture linea di partenza
│   └── reclama_banner.png      # Texture banner pubblicitario
├── tools/
│   └── track_viewer.py         # Viewer 3D per file KN5 (PyQt5 + OpenGL)
├── addons/                     # Componenti aggiuntivi per AC (CM, CSP, font)
│   ├── ContentManager.zip
│   ├── lights-patch-v0.2.11.zip
│   └── ac-fonts.zip
├── builds/                     # Zip distribuibili (generati da build.sh)
└── mod/pista_caudina/          # Mod finale pronta per AC
    ├── pista_caudina.kn5
    ├── map.png
    ├── ai/fast_lane.ai
    ├── data/
    │   ├── surfaces.ini        # Fisica superfici (ROAD, KERB, GRASS, WALL, PIT, GROUND)
    │   ├── cameras.ini
    │   ├── map.ini
    │   ├── lighting.ini
    │   └── groove.ini
    └── ui/
        ├── ui_track.json
        ├── preview.png
        └── outline.png
```

## Dettagli tecnici

| Parametro | Valore |
|-----------|--------|
| Lunghezza | 860 m |
| Larghezza strada | 7.5 m |
| Cordoli | 1.2 m x 8 cm (solo nelle curve) |
| Erba laterale | 4 m per lato |
| Muri | 1.5 m altezza, 1.5 m spessore |
| Griglia partenza | 10 posizioni |
| Pit boxes | 10 |
| Direzione | Orario (CW) |
| Coordinate GPS | 41.0614, 14.6544 |
| Formato KN5 | v6, exporter custom Python |
| Texture | PNG embedded (D3DX11 auto-detect) |

## Note tecniche KN5

L'exporter KN5 custom (`scripts/export_kn5.py`) gestisce:

- **Conversione coordinate** Blender Z-up -> AC Y-up: `(x, y, z)` -> `(x, z, -y)` (det=+1, nessuna inversione winding)
- **UV V-flip** OpenGL -> DirectX: `v = 1 - v` (Blender V=0 in basso, AC V=0 in alto)
- **Empty AC_** esportati come coppie dummy+mesh (box 24 verts / 36 indices)
- **Matrice KN5**: `transpose(C * T_blender)` dove C swappa row1<->row2 con segno
- **Embedding texture** PNG direttamente (senza conversione DDS)
- **Calcolo bounding sphere** per ogni mesh
- **Matching superfici** tramite substring: KEY in `surfaces.ini` cercato nel nome mesh

### Convenzione rotazione empty (Blender -> AC)

```
rotation_euler = (+pi/2, 0, pi - heading)
```

dove `heading = atan2(tx, -ty)` con `t` = tangente della direzione di marcia in Blender.

- `+pi/2` in X: converte Blender Z-up in AC Y-up per gli assi locali
- `pi - heading` in Z: compensa l'inversione dell'asse Z causata dalla rotazione X

### Requisiti collisione mesh

- **Muri e terreno** devono essere suddivisi in sub-mesh (`_SUB0`, `_SUB1`, ...) con bounding sphere ~20-30m
- Un singolo quad grande (es. 174x310m) viene ignorato dalla collision detection di AC
- Le normali devono puntare verso l'alto (Z+ in Blender) — il winding corretto e' CCW visto dall'alto

### Superfici fisiche (surfaces.ini)

| KEY | Mesh | Friction | Tipo |
|-----|------|----------|------|
| ROAD | 1ROAD | 0.97 | Pista valida |
| KERB | 1KERB_*, 2KERB_* | 0.93 | Cordoli (vibrazione) |
| GRASS | 1GRASS, 2GRASS | 0.60 | Erba (fuori pista) |
| WALL | 1WALL_SUB*, 2WALL_SUB* | 0.365 | Barriere |
| PIT | (pitlane) | 0.97 | Pit lane |
| GROUND | 1GROUND_SUB* | 0.60 | Terreno base (66 tile) |

AC non richiede `models.ini` — rileva automaticamente il KN5 dal nome della cartella.

## Risoluzione problemi

- **Auto parte fuori pista o capovolta:** Verificare la rotazione degli empty AC_START in Blender: deve essere `(+90, 0, angolo)`. Se e' `(-90, 0, angolo)` il Y-axis nel KN5 viene invertito.
- **Banner/immagini capovolte in AC:** L'exporter deve applicare il V-flip UV (`v = 1 - v`). Senza, le texture non-tileable appaiono invertite (Blender usa OpenGL V=0 basso, AC usa DirectX V=0 alto).
- **Auto cade nel vuoto:** Il terreno (GROUND) e i muri (WALL) devono essere suddivisi in sub-mesh con bounding sphere <30m. Un singolo quad grande non viene rilevato dalla collision di AC.
- **Texture nere/mancanti:** Le texture sono embedded nel KN5 come PNG. Riesportare con `export_kn5.py`.
- **AI non funziona:** Rigenerare `fast_lane.ai` con `generate_ai_line.py`.
- **Modifiche Blender non visibili in AC:** Eseguire tutti e 3 gli step di build (Manager Build All o `python build_cli.py`), poi installare dal tab Install del Manager. Verificare che i checksum dei KN5 corrispondano.

## Guida Blender — creare gli elementi della pista

Tutti gli elementi della pista sono mesh modellate direttamente in `pista_caudina.blend`.
L'exporter KN5 esporta **ogni mesh presente nella scena** senza filtri: il nome della mesh
determina quale superficie fisica AC gli assegna (substring match con le KEY in `surfaces.ini`).

### Regole generali

- **Nomenclatura**: il prefisso `1` indica il lato interno della pista, `2` il lato esterno.
  La parte centrale del nome (`ROAD`, `WALL`, `KERB`, `GRASS`, `GROUND`) e' la keyword
  che AC usa per assegnare la superficie fisica.
- **Materiali**: ogni mesh deve avere un materiale Blender con una texture (nodo `Image Texture`
  collegato al `Base Color` del `Principled BSDF`). Le custom properties AC
  (`ac_shader`, `ksAmbient`, `ksDiffuse`, `ksSpecular`, `ksSpecularEXP`) si aggiungono
  dal pannello Custom Properties del materiale.
- **Normali**: verificare sempre con Overlay > Face Orientation (blu = OK, rosso = invertite).
  Non usare "Recalculate Outside" — e' inaffidabile. Correggere manualmente con `Flip`.
- **Bounding sphere**: AC ignora la collisione di mesh con bounding sphere > ~30m.
  Qualsiasi elemento che deve avere collisione (muri, terreno) va suddiviso in segmenti.
- **Trasformazioni**: l'exporter applica `matrix_world`, quindi posizione/rotazione/scala
  dell'oggetto vengono incluse automaticamente. Si puo' modellare in qualsiasi posizione.

### Asfalto (1ROAD)

L'asfalto e' una **singola mesh** chiamata `1ROAD` che rappresenta l'intera superficie stradale.

**Come crearla:**
1. Creare un piano (`Shift+A` > Mesh > Plane)
2. In Edit Mode, estrudere e modellare la forma della strada seguendo il tracciato
3. La mesh deve avere **2 bordi boundary chiusi** (interno ed esterno) — servono a
   `generate_ai_line.py` per estrarre la centerline AI. Entrambi i loop devono avere
   lo stesso numero di vertici
4. Larghezza tipica: 7-8m, suddivisione longitudinale ogni ~1m per avere abbastanza punti AI
5. Le normali devono puntare verso l'alto (Z+ in Blender)
6. UV mapping: proiettare dall'alto (`U` > Project from View) o unwrap per controllare la scala della texture

**Materiale:** assegnare un materiale con texture `asphalt.png`, shader `ksPerPixel`.

**Nome:** `1ROAD` (obbligatorio — lo script AI line cerca esattamente questo nome).

**Superficie AC:** KEY=ROAD, friction 0.97, IS_VALID_TRACK=1.

### Cordoli (1KERB_*, 2KERB_*)

I cordoli sono mesh separate posizionate lungo i bordi della strada nelle curve.

**Come crearli:**
1. Creare un piano e modellarlo come una striscia stretta (~1.2m di larghezza)
   leggermente rialzata rispetto all'asfalto (~8cm di altezza)
2. Posizionare il cordolo adiacente al bordo della strada, nella curva desiderata
3. La mesh puo' seguire la curvatura della strada — basta estrudere i vertici lungo la curva
4. Le normali devono puntare verso l'alto
5. UV mapping: allineare le UV in modo che la texture a strisce rosse/bianche sia perpendicolare
   alla direzione di marcia

**Materiale:** assegnare un materiale con texture `curb_rw.png`, shader `ksPerPixel`.

**Nome:** `1KERB_nomecurva` (lato interno) o `2KERB_nomecurva` (lato esterno).
Esempi: `1KERB_CURVA1`, `2KERB_CHICANE`. La parte `KERB` nel nome e' quella che
attiva il match con surfaces.ini.

**Superficie AC:** KEY=KERB, friction 0.93, vibrazione attiva (SIN_HEIGHT=0.005, VIBRATION_GAIN=0.5).

### Erba (1GRASS, 2GRASS)

L'erba e' la fascia di terreno tra la strada e i muri, su ciascun lato.

**Come crearla:**
1. Creare un piano e modellarlo come una fascia che segue il bordo esterno della strada
2. Larghezza tipica: ~4m per lato
3. Il bordo interno dell'erba deve combaciare con il bordo esterno della strada (o del cordolo)
4. Le normali verso l'alto
5. L'erba non ha bisogno di suddivisione in sub-mesh (non ha collisione critica — l'auto
   ci scivola sopra con friction ridotta)

**Materiale:** assegnare un materiale con texture `grass.png`, shader `ksPerPixel`.

**Nome:** `1GRASS` (lato interno) e `2GRASS` (lato esterno).

**Superficie AC:** KEY=GRASS, friction 0.60, IS_VALID_TRACK=0, BLACK_FLAG_TIME=3.0 (penalita' fuoripista).

### Muri (1WALL_SUBxx, 2WALL_SUBxx)

I muri sono le barriere ai bordi della pista. Devono essere **suddivisi in segmenti** per la collisione.

**Come crearli:**
1. Creare un Cube (`Shift+A` > Mesh > Cube)
2. In Edit Mode, scalarlo in una lastra: ~20-30m di lunghezza, ~1.5m di altezza, ~1.5m di spessore
3. Posizionare il muro lungo il bordo esterno dell'erba
4. In Edit Mode, spostare i vertici per seguire la curvatura della strada — bastano pochi
   vertici (~10-20 per segmento), non serve alta risoluzione
5. Le normali delle facce interne (verso la pista) devono puntare verso la strada

**Perche' suddividere:** AC ignora la collisione di mesh con bounding sphere > ~30m.
Un muro unico lungo tutta la pista (~860m) avrebbe una bounding sphere enorme e l'auto
lo attraverserebbe. Ogni segmento da ~20-30m ha una bounding sphere di ~10-15m e funziona.

**Come suddividere un muro lungo:**
1. Selezionare il muro in Edit Mode
2. Selezionare un anello di edge (`Alt+Click`) nel punto dove tagliare
3. `Mesh` > `Separate` > `Selection` (`P` > Selection)
4. Rinominare i pezzi risultanti con numeri sequenziali

**Materiale:** assegnare un materiale con texture `barrier.png`, shader `ksPerPixel`.

**Nome:** `1WALL_SUB0`, `1WALL_SUB1`, ... (lato interno) e `2WALL_SUB0`, `2WALL_SUB1`, ... (lato esterno).
Il numero deve essere unico e sequenziale per lato. La parte `WALL` attiva il match con surfaces.ini.

**Superficie AC:** KEY=WALL, friction 0.365, IS_VALID_TRACK=0.

### Terreno (1GROUND_SUBxx)

Il terreno e' il piano base sotto tutta la pista. Come i muri, deve essere suddiviso in tile.

**Come crearlo:**
1. Creare un piano grande che copra l'intera area della pista
2. In Edit Mode, suddividerlo in una griglia (`Right Click` > `Subdivide`, oppure `Ctrl+R` per loop cuts)
3. Separare ogni tile: selezionare le facce di ogni quadrato e `P` > Selection
4. Ogni tile deve avere una bounding sphere < ~30m (tile da ~30x30m funzionano bene)

**Materiale:** assegnare un materiale con texture `grass.png`, shader `ksPerPixel`.

**Nome:** `1GROUND_SUB0`, `1GROUND_SUB1`, ... fino a coprire tutta l'area (es. 66 tile).

**Superficie AC:** KEY=GROUND, friction 0.60, stesse proprieta' dell'erba.

### Riepilogo nomenclatura

| Elemento | Nome mesh | Texture | Suddivisione | Note |
|----------|-----------|---------|---------------|------|
| Asfalto | `1ROAD` | asphalt.png | No (mesh unica) | 2 boundary loops per AI line |
| Cordoli | `1KERB_*`, `2KERB_*` | curb_rw.png | No | Rialzati ~8cm, solo nelle curve |
| Erba | `1GRASS`, `2GRASS` | grass.png | No | Fascia 4m tra strada e muri |
| Muri | `1WALL_SUBxx`, `2WALL_SUBxx` | barrier.png | Si (~20-30m) | Bounding sphere < 30m |
| Terreno | `1GROUND_SUBxx` | grass.png | Si (~30x30m) | 66 tile, piano base |
| Banner | `BANNE_*` | reclama_banner.png | No | Piani double-sided |
| Empty AC | `AC_START_0`, `AC_PIT_0`, ... | — | — | Tipo Empty, non mesh |
