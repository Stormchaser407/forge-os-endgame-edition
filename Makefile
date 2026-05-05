# Forge OS Endgame Edition - Complete Build System
# AI-Powered Investigation Platform with Obsidian Council

VERSION := 1.0.0-endgame
OBSIDIAN_VERSION := 1.0.0
BUILD_DIR := build
OUTPUT_DIR := output
ISO_NAME := forge-os-endgame-$(VERSION).iso

.PHONY: all clean build-all docker-build iso obsidian-council test deploy help

# Default target - build everything
all: build-all

# Build everything - OS + Obsidian Council
build-all: prepare docker-build obsidian-council

# Prepare build environment
prepare:
	@echo "🔧 Preparing Forge OS Endgame Edition build environment..."
	mkdir -p $(BUILD_DIR) $(OUTPUT_DIR)
	mkdir -p branding/{wallpapers,icons,sounds,logos}
	mkdir -p applications/{evidence-manager,osint-dashboard}
	mkdir -p obsidian-council/{agents,core,web,bin}
	mkdir -p config/{grub,plymouth-theme,gnome,kernel}

# Build Docker container for ISO creation
docker-build:
	@echo "🐳 Building Docker container..."
	docker build -t forge-os-endgame:$(VERSION) $(BUILD_DIR)

# Build Obsidian Council components
obsidian-council:
	@echo "🧠 Building Obsidian Council AI Framework..."
	cd obsidian-council && npm install && npm run build

# Create bootable ISO
iso: docker-build obsidian-council
	@echo "📀 Creating Forge OS Endgame Edition ISO..."
	docker run --cap-add=SYS_ADMIN --cap-add=MKNOD --cap-add=SYS_CHROOT \
		--name forge-os-builder \
		-v $(PWD)/scripts:/forge-os/scripts:ro \
		-v $(PWD)/config:/forge-os/config:ro \
		-v $(PWD)/branding:/forge-os/branding:ro \
		-v $(PWD)/applications:/forge-os/applications:ro \
		-v $(PWD)/obsidian-council:/forge-os/obsidian-council:ro \
		-v $(PWD)/$(OUTPUT_DIR):/forge-os/output \
		--rm \
		forge-os-endgame:$(VERSION)

# Test ISO in QEMU
test: iso
	@echo "🖥️  Testing Forge OS in QEMU..."
	qemu-system-x86_64 \
		-m 4096 \
		-enable-kvm \
		-cpu host \
		-cdrom $(OUTPUT_DIR)/$(ISO_NAME) \
		-boot d \
		-vga qxl \
		-spice port=5900,addr=127.0.0.1,disable-ticketing \
		-device virtio-serial-pci \
		-device virtserialport,chardev=spicechannel0,name=com.redhat.spice.0 \
		-chardev spicevmc,id=spicechannel0,name=vdagent

# Test with VirtualBox
test-vbox: iso
	@echo "📦 Creating VirtualBox test environment..."
	-VBoxManage unregistervm "ForgeOS-Endgame-Test" --delete 2>/dev/null
	VBoxManage createvm --name "ForgeOS-Endgame-Test" --ostype Ubuntu_64 --register
	VBoxManage modifyvm "ForgeOS-Endgame-Test" \
		--memory 4096 \
		--vram 128 \
		--cpus 2 \
		--accelerate3d on \
		--boot1 dvd \
		--boot2 disk
	VBoxManage storagectl "ForgeOS-Endgame-Test" --name "SATA" --add sata --controller IntelAHCI
	VBoxManage storageattach "ForgeOS-Endgame-Test" \
		--storagectl "SATA" \
		--port 0 \
		--device 0 \
		--type dvddrive \
		--medium $(PWD)/$(OUTPUT_DIR)/$(ISO_NAME)
	VBoxManage startvm "ForgeOS-Endgame-Test"

# Deploy to USB drive
deploy-usb: iso checksums
	@echo "⚠️  WARNING: This will completely erase the target USB drive!"
	@echo "📱 Please ensure you have selected the correct device."
	@echo "🔍 Use 'lsblk' to identify your USB device"
	@read -p "Enter USB device path (e.g., /dev/sdb): " device; \
	if [ -z "$$device" ]; then echo "❌ No device specified"; exit 1; fi; \
	echo "🚀 Writing ISO to $$device..."; \
	sudo dd if=$(OUTPUT_DIR)/$(ISO_NAME) of=$$device bs=4M status=progress conv=fsync && \
	echo "✅ USB deployment complete!"

# Generate checksums
checksums: iso
	@echo "🔐 Generating checksums..."
	mkdir -p $(OUTPUT_DIR)
	cd $(OUTPUT_DIR) && sha256sum $(ISO_NAME) > $(ISO_NAME).sha256
	cd $(OUTPUT_DIR) && md5sum $(ISO_NAME) > $(ISO_NAME).md5
	@echo "✅ Checksums generated"

# Sign ISO with GPG
sign: iso
	@echo "✍️  Signing ISO with GPG..."
	mkdir -p $(OUTPUT_DIR)
	gpg --armor --detach-sign $(OUTPUT_DIR)/$(ISO_NAME)
	@echo "✅ ISO signed"

# Create distribution package
package: iso checksums sign
	@echo "📦 Creating distribution package..."
	mkdir -p $(OUTPUT_DIR)
	mkdir -p $(OUTPUT_DIR)/forge-os-endgame-$(VERSION)
	cp $(OUTPUT_DIR)/$(ISO_NAME)* $(OUTPUT_DIR)/forge-os-endgame-$(VERSION)/
	cp README.md $(OUTPUT_DIR)/forge-os-endgame-$(VERSION)/
	cp -r docs $(OUTPUT_DIR)/forge-os-endgame-$(VERSION)/ 2>/dev/null || true
	cd $(OUTPUT_DIR) && tar -czf forge-os-endgame-$(VERSION).tar.gz forge-os-endgame-$(VERSION)
	@echo "✅ Distribution package ready: $(OUTPUT_DIR)/forge-os-endgame-$(VERSION).tar.gz"

# Development environment
dev:
	@echo "🔧 Starting development environment..."
	docker run -it --cap-add=SYS_ADMIN --cap-add=MKNOD --cap-add=SYS_CHROOT \
		--name forge-os-dev \
		-v $(PWD):/forge-os \
		-w /forge-os \
		--rm \
		ubuntu:24.04 \
		/bin/bash

# Build Obsidian Council development server
dev-council:
	@echo "🧠 Starting Obsidian Council development server..."
	cd obsidian-council && npm run dev

# Run security scan
security-scan: prepare
	@echo "🔒 Running comprehensive security scan..."
	@echo "📊 Installing security tools if needed..."
	@which bandit >/dev/null 2>&1 || pip3 install bandit
	@which safety >/dev/null 2>&1 || pip3 install safety
	@echo "🔍 Running Bandit security scan on Python code..."
	@bandit -r ./obsidian-council/ -f json -o $(OUTPUT_DIR)/bandit-report.json || echo "⚠️  Bandit found security issues - check report"
	@echo "🔍 Running dependency vulnerability check..."
	@safety scan --output json > $(OUTPUT_DIR)/safety-report.json 2>&1 || echo "⚠️  Safety check completed (may have found issues)"
	@echo "🔍 Checking file permissions..."
	@find $(PWD) -type f -perm /o+w -exec echo "⚠️  World-writable file: {}" \; > $(OUTPUT_DIR)/file-permissions.txt
	@echo "🔍 Checking for potential secrets..."
	@grep -r -i "api[_-]key\|password\|secret\|token" ./obsidian-council/ --include="*.py" > $(OUTPUT_DIR)/potential-secrets.txt 2>/dev/null || echo "No obvious secrets found"
	@echo "✅ Security scan complete - reports in $(OUTPUT_DIR)/"

# Performance benchmarks
benchmark: iso
	@echo "📊 Running performance benchmarks..."
	@echo "💾 ISO Size: $$(du -h $(OUTPUT_DIR)/$(ISO_NAME) | cut -f1)"
	@echo "⏱️  Build Time: Check previous output"
	@echo "🎯 Target: Under 8GB, Under 60 minutes build time"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf $(BUILD_DIR)/chroot
	rm -rf $(BUILD_DIR)/iso
	-docker rmi forge-os-endgame:$(VERSION) 2>/dev/null
	-docker rm forge-os-builder 2>/dev/null
	cd obsidian-council && npm run clean 2>/dev/null || true

# Deep clean - remove everything
distclean: clean
	@echo "🗑️  Deep cleaning everything..."
	rm -rf $(BUILD_DIR)
	rm -rf $(OUTPUT_DIR)
	rm -rf obsidian-council/node_modules
	rm -rf obsidian-council/dist

# Install dependencies on host system
install-deps:
	@echo "📥 Installing build dependencies..."
	sudo apt-get update
	sudo apt-get install -y \
		docker.io \
		qemu-system-x86 \
		virtualbox \
		build-essential \
		debootstrap \
		squashfs-tools \
		xorriso \
		grub-pc-bin \
		grub-efi-amd64-bin \
		curl \
		wget \
		git \
		nodejs \
		npm
	sudo systemctl enable docker
	sudo usermod -aG docker $$USER
	@echo "✅ Dependencies installed. Please log out and back in for Docker group changes."

# Show build status
status:
	@echo "📊 Forge OS Endgame Edition Build Status"
	@echo "=========================================="
	@echo "Version: $(VERSION)"
	@echo "Obsidian Council: $(OBSIDIAN_VERSION)"
	@echo ""
	@echo "🐳 Docker Images:"
	@docker images | grep forge-os-endgame || echo "  No Forge OS images found"
	@echo ""
	@echo "📁 Build Artifacts:"
	@ls -la $(OUTPUT_DIR)/ 2>/dev/null || echo "  No build outputs found"
	@echo ""
	@echo "🧠 Obsidian Council Status:"
	@cd obsidian-council && npm list --depth=0 2>/dev/null || echo "  Dependencies not installed"

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Building agent documentation..."
	@python3 -c "import sys; sys.path.append('obsidian-council'); from agents.agent_registry import get_division_info; import json; print(json.dumps(get_division_info(), indent=2))" > docs/AGENTS.json 2>/dev/null || echo "Agent registry not available"
	@echo "✅ Documentation generated"

# Quick build for testing (no full ISO)
quick:
	@echo "⚡ Quick build for testing..."
	$(MAKE) prepare obsidian-council
	@echo "✅ Quick build complete - ready for development testing"

# Show help
help:
	@echo "🔥 Forge OS Endgame Edition Build System"
	@echo "AI-Powered Investigation Platform with Obsidian Council"
	@echo ""
	@echo "🎯 Main Targets:"
	@echo "  all          - Build complete system (default)"
	@echo "  build-all    - Build OS + Obsidian Council" 
	@echo "  iso          - Create bootable ISO"
	@echo "  quick        - Quick build for testing"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test         - Test in QEMU"
	@echo "  test-vbox    - Test in VirtualBox"
	@echo "  dev          - Start development environment"
	@echo "  dev-council  - Start Obsidian Council dev server"
	@echo ""
	@echo "📦 Distribution:"
	@echo "  deploy-usb   - Write to USB drive"
	@echo "  checksums    - Generate SHA256/MD5"
	@echo "  sign         - Sign with GPG"
	@echo "  package      - Create distribution package"
	@echo ""
	@echo "🔧 Maintenance:"
	@echo "  clean        - Clean build artifacts"
	@echo "  distclean    - Remove everything"
	@echo "  install-deps - Install build dependencies"
	@echo "  status       - Show build status"
	@echo ""
	@echo "🔒 Security:"
	@echo "  security-scan - Run security checks"
	@echo "  benchmark     - Performance metrics"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  docs         - Generate documentation"
	@echo "  help         - Show this help"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make install-deps  # Install dependencies"
	@echo "  make all          # Build everything"
	@echo "  make test         # Test the build"
	@echo ""
	@echo "⚡ For rapid development:"
	@echo "  make quick        # Quick build"
	@echo "  make dev-council  # Start Obsidian Council server"