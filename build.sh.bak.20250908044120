#!/usr/bin/env bash
set -euo pipefail
LB_DIR=live-build-dir
ISO_NAME=forgeos-custom.iso

echo "[build.sh] Ensure live-build and deps are installed (use apt on host)"
sudo apt-get update
sudo apt-get install -y live-build debootstrap qemu-user-static binfmt-support xz-utils || true

rm -rf "\${LB_DIR}"
mkdir -p "\${LB_DIR}"
cd "\${LB_DIR}"

# change --distribution to kali-rolling if you target Kali base (and preload its keyring)
lb config \
  --distribution bullseye \
  --archive-areas "main contrib non-free" \
  --binary-images iso-hybrid \
  --apt-indices false \
  --debian-installer false \
  --bootappend-live "boot=live components splash" \
  --linux-packages "linux-image-amd64" \
  --chroot-filesystem squashfs

# copy package lists and hooks from repo root
if [ -d ../config/package-lists ]; then
  mkdir -p config/package-lists
  cp -r ../config/package-lists/* config/package-lists/
fi

if [ -d ../config/hooks ]; then
  mkdir -p config/hooks
  cp -r ../config/hooks/* config/hooks/
  chmod +x config/hooks/*
fi

echo "[build.sh] Starting live-build (this can take a while)"
sudo lb build

if [ -f live-image-amd64.hybrid.iso ]; then
  mv live-image-amd64.hybrid.iso ../\${ISO_NAME}
  echo "Built ../\${ISO_NAME}"
else
  echo "Build finished but iso not found. Check live-build logs."
  exit 2
fi
