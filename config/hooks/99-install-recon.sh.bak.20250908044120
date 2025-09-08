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
