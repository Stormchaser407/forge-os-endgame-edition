#!/usr/bin/env bash
# claude_setup.sh
# Creates config/package-lists, hooks, build scripts, CI, smoke test, pi notes,
# commits to branch `claude/setup` and pushes. Run from repo root in WSL.

set -euo pipefail
BRANCH="claude/setup"
NOW="$(date +%Y%m%d%H%M%S)"

# helper: backup existing file if present
backup_if_exists() {
  if [ -e "$1" ]; then
    mv "$1" "$1.bak.${NOW}"
    echo "Backed up existing $1 -> $1.bak.${NOW}"
  fi
}

# ensure we're inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not in a git repo. cd into the repo root and re-run."
  exit 2
fi

# create branch or switch to it
if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  git checkout "${BRANCH}"
else
  git checkout -b "${BRANCH}"
fi

# make directories
mkdir -p config/package-lists config/hooks .github/workflows scripts pi

# 1) package list
PACKAGE_FILE="config/package-lists/forge.list.chroot"
backup_if_exists "${PACKAGE_FILE}"
cat > "${PACKAGE_FILE}" <<'EOF'
# ForgeOS authoritative package list (adjust as needed)
# Desktop essentials
xfce4
lightdm
network-manager
pulseaudio

# security & utils
openssh-server
ufw
cryptsetup
lvm2

# dev & tooling
build-essential
git
python3
python3-pip
curl
wget
jq

# Note: larger Python-based OSINT tools are installed in hooks (pip)
EOF
chmod 644 "${PACKAGE_FILE}"
echo "Wrote ${PACKAGE_FILE}"

# 2) chroot hook
HOOK_FILE="config/hooks/99-install-recon.sh"
backup_if_exists "${HOOK_FILE}"
cat > "${HOOK_FILE}" <<'EOF'
#!/bin/bash
set -e
# Runs inside the live-build chroot. No secrets here.
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip
# example pip installs. Tidy and minimal; change to suit your tool choices
pip3 install --no-cache-dir sherlock
# PhoneInfoga / PeopleDataLabs / Dehashed require API keys - leave installers as placeholders.
# Example placeholder (do not put keys here):
# /usr/local/bin/install_phoneinfoga.sh || true
EOF
chmod +x "${HOOK_FILE}"
echo "Wrote ${HOOK_FILE}"

# 3) build.sh (WSL-friendly)
BUILD_SH="build.sh"
backup_if_exists "${BUILD_SH}"
cat > "${BUILD_SH}" <<'EOF'
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
EOF
chmod +x "${BUILD_SH}"
echo "Wrote ${BUILD_SH}"

# 4) QEMU smoke test
SMOKE="scripts/smoke-test-qemu.sh"
backup_if_exists "${SMOKE}"
cat > "${SMOKE}" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
ISO="${1:-forgeos-custom.iso}"
IMG="forgeos-test.qcow2"

if [ ! -f "${ISO}" ]; then
  echo "ISO ${ISO} not found in repo root. Build it first."
  exit 1
fi

qemu-img create -f qcow2 "${IMG}" 40G || true

# Boot ISO; forward host port 2222 to guest 22 (if sshd enabled in live image)
qemu-system-x86_64 -m 4G -smp 2 \
  -cdrom "${ISO}" -boot d \
  -drive file="${IMG}",if=virtio,cache=writeback \
  -net nic -net user,hostfwd=tcp::2222-:22 \
  -serial mon:stdio -display none &
QEMU_PID=$!

echo "[smoke-test] QEMU PID: ${QEMU_PID}. Waiting 60s for boot..."
sleep 60

if nc -z localhost 2222 >/dev/null 2>&1; then
  echo "[smoke-test] SSH reachable on 2222; running quick diagnostics (requires live image enabling ssh)"
  ssh -oStrictHostKeyChecking=no -p 2222 liveuser@localhost "hostname; ip a; systemctl --no-pager --failed || true; journalctl -b -n 200 --no-pager | tail -n 50" || true
else
  echo "[smoke-test] SSH not reachable. Check console output above for boot logs."
fi

kill ${QEMU_PID} || true
wait ${QEMU_PID} 2>/dev/null || true
EOF
chmod +x "${SMOKE}"
echo "Wrote ${SMOKE}"

# 5) GitHub Actions workflows
CI_FILE=".github/workflows/ci-build-and-security.yml"
backup_if_exists "${CI_FILE}"
cat > "${CI_FILE}" <<'EOF'
name: CI - security + build (light)

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  security:
    runs-on: ubuntu-latest
    outputs:
      security_pass: ${{ steps.check.outputs.passed || 'false' }}
    steps:
      - uses: actions/checkout@v4
      - name: Install Python deps
        run: |
          python3 -m pip install --user bandit safety || true
      - name: Run bandit
        run: |
          python3 -m pip show bandit >/dev/null 2>&1 && bandit -r . -f json -o bandit_report.json || true
      - name: Run safety
        run: |
          if [ -f requirements.txt ]; then python3 -m pip install --user -r requirements.txt || true; fi
          python3 -m pip show safety >/dev/null 2>&1 && safety check --json > safety_report.json || true
      - name: Upload reports
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: |
            bandit_report.json
            safety_report.json

  build:
    needs: security
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup apt deps
        run: |
          sudo apt-get update
          sudo apt-get install -y live-build debootstrap qemu-user-static xz-utils || true
      - name: Run build.sh
        run: |
          chmod +x ./build.sh
          ./build.sh
      - name: Upload ISO
        uses: actions/upload-artifact@v4
        with:
          name: forgeos-iso
          path: forgeos-custom.iso
EOF
chmod 644 "${CI_FILE}"
echo "Wrote ${CI_FILE}"

SECRET_SCAN_FILE=".github/workflows/secret-scan.yml"
backup_if_exists "${SECRET_SCAN_FILE}"
cat > "${SECRET_SCAN_FILE}" <<'EOF'
name: Secret Scan

on:
  pull_request:
    branches: [ main ]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install truffleHog
        run: |
          python3 -m pip install --user truffleHog || true
      - name: Run trufflehog
        run: |
          python3 -m pip show truffleHog >/dev/null 2>&1 || true
          trufflehog filesystem --json . > truffle_report.json || true
      - name: Upload
        uses: actions/upload-artifact@v4
        with:
          name: secret-scan
          path: truffle_report.json
      - name: Fail on findings
        run: |
          if [ -s truffle_report.json ]; then echo "Secrets detected"; jq '.results | length' truffle_report.json; exit 1; fi
EOF
chmod 644 "${SECRET_SCAN_FILE}"
echo "Wrote ${SECRET_SCAN_FILE}"

# 6) Pi README skeleton
PI_README="pi/PI_README.md"
backup_if_exists "${PI_README}"
cat > "${PI_README}" <<'EOF'
Raspberry Pi 5 / Aegis build notes
- Use pi-gen (Debian) or Kali's ARM build pipeline; do NOT reuse amd64 live-build profile.
- Keep ARM profiles separate to avoid firmware/kernel mismatches.
- Include non-free firmware blobs for Wi-Fi/Broadcom and test in qemu-user/aarch64 before flashing.
EOF
chmod 644 "${PI_README}"
echo "Wrote ${PI_README}"

# 7) add files to git, commit
git add -A
git commit -m "chore(claude): add live-build config, hooks, build+smoke scripts, CI and pi notes" || true

# 8) push branch
echo "Attempting git push to origin/${BRANCH}..."
if git remote | grep -q origin; then
  set +e
  git push -u origin "${BRANCH}"
  PUSH_RC=$?
  set -e
  if [ ${PUSH_RC} -ne 0 ]; then
    echo "git push failed (probably auth). Please run: git push -u origin ${BRANCH}"
  else
    echo "Pushed branch ${BRANCH} to origin."
  fi
else
  echo "No 'origin' remote configured. Add your remote and push branch ${BRANCH} manually."
fi

echo "Done. Suggested next steps:"
echo " - open a PR from ${BRANCH} to main"
echo " - run ./build.sh locally (or on your self-hosted runner)"
echo " - run scripts/smoke-test-qemu.sh forgeos-custom.iso once ISO exists"
echo
echo "WARNING: do NOT add API keys or secrets to the repo. Use GitHub Secrets or runner-level protected files."
