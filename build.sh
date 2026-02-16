#!/bin/bash
# Pista Caudina - Build completa della mod
# Esegue la pipeline: Blender → KN5 → mod folder → AI line
# Base: pista_caudina.blend (modificabile direttamente in Blender)
# Uso: bash build.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Pista Caudina - Build mod ==="
echo ""

# --- Verifica requisiti ---
if [ ! -f "pista_caudina.blend" ]; then
    echo "Errore: pista_caudina.blend non trovato."
    exit 1
fi

if [ ! -d "textures" ] || [ -z "$(ls textures/*.png 2>/dev/null)" ]; then
    echo "Errore: cartella textures/ vuota o mancante."
    echo "Inserisci le textures (asphalt.png, grass.png, curb_rw.png, barrier.png, startline.png)"
    exit 1
fi

BLENDER="/snap/bin/blender"
if ! command -v "$BLENDER" &>/dev/null; then
    BLENDER="blender"
    if ! command -v "$BLENDER" &>/dev/null; then
        echo "Errore: Blender non trovato. Installa con: sudo snap install blender --classic"
        exit 1
    fi
fi
echo "Blender: $BLENDER"

# Virtualenv
if [ ! -d ".venv" ]; then
    echo "Creo virtualenv..."
    python3 -m venv .venv
fi
source .venv/bin/activate

# Controlla dipendenze Python
python3 -c "import numpy, PIL" 2>/dev/null || {
    echo "Installo dipendenze Python..."
    pip install -q -r requirements.txt
}
echo ""

# --- Step 1: Esportazione KN5 ---
echo "[1/3] Esportazione KN5 da Blender..."
"$BLENDER" --background pista_caudina.blend --python scripts/export_kn5.py 2>&1 | grep -E "^(  |Done|=)"
echo ""

# --- Step 2: Setup struttura mod ---
echo "[2/3] Creazione struttura mod..."
python3 scripts/setup_mod_folder.py
echo ""

# --- Step 3: Generazione AI line ---
echo "[3/3] Generazione AI line..."
python3 scripts/generate_ai_line.py
echo ""

# --- Copia KN5 nel mod ---
echo "Copia KN5 nella cartella mod..."
cp pista_caudina.kn5 mod/pista_caudina/pista_caudina.kn5
echo ""

# --- Creazione zip distribuibile ---
echo "Creazione zip distribuibile..."
mkdir -p builds
(cd mod && zip -r -q ../builds/pista_caudina.zip pista_caudina/)
echo "  builds/pista_caudina.zip  $(du -h builds/pista_caudina.zip | cut -f1)"
echo ""

# --- Riepilogo ---
echo "=== Build completata! ==="
echo ""
echo "File generati:"
echo "  pista_caudina.kn5        $(du -h pista_caudina.kn5 | cut -f1)"
echo "  mod/pista_caudina/       $(du -sh mod/pista_caudina/ | cut -f1) totale"
echo "  builds/pista_caudina.zip $(du -h builds/pista_caudina.zip | cut -f1) (distribuibile)"
echo ""
echo "Per installare in Assetto Corsa:"
echo "  bash install.sh"
echo ""
echo "Per condividere la mod:"
echo "  Invia builds/pista_caudina.zip"
echo "  Estrarre in: assettocorsa/content/tracks/"
