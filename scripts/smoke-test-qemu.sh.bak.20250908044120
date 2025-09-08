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
