#!/bin/bash
set -e

# Configuración
DATE=$(date +%F)
BACKUP_DIR="/home/user/.gemini/antigravity/brain/5b6f2c07-dcbe-4689-88c6-917a0b52d94b/ia"
BACKUP_FILE="/home/user/backup-ia-$DATE.tar.zst"
RCLONE_BIN="./rclone_bin"

echo "📦 Creando backup comprimido de $BACKUP_DIR..."
tar --zstd \
  --exclude="$BACKUP_DIR/venv" \
  --exclude="$BACKUP_DIR/outputs" \
  --exclude="$BACKUP_DIR/unsloth_compiled_cache" \
  -cf $BACKUP_FILE $BACKUP_DIR

echo "🚀 Subiendo a Google Drive (gdrive:vast-backups)..."
# Asegurarse de que rclone esté configurado como 'gdrive'
$RCLONE_BIN copy $BACKUP_FILE gdrive:vast-backups

echo "🧹 Limpiando archivo local..."
rm $BACKUP_FILE

echo "✅ Backup completado y subido con éxito."
