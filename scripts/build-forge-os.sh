#!/bin/bash
# Forge OS Endgame Edition - Master Build Script

set -e

FORGE_VERSION="1.0.0-endgame"
BUILD_DIR="/forge-os/build"
CHROOT_DIR="$BUILD_DIR/chroot"
ISO_DIR="$BUILD_DIR/iso"
OUTPUT_DIR="/forge-os/output"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
AMBER='\033[0;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

section() {
    echo -e "\n${PURPLE}=========================================="
    echo -e "  $1"
    echo -e "==========================================${NC}\n"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Display banner
display_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
    ███████╗ ██████╗ ██████╗  ██████╗ ███████╗     ██████╗ ███████╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝    ██╔═══██╗██╔════╝
    █████╗  ██║   ██║██████╔╝██║  ███╗█████╗      ██║   ██║███████╗
    ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝      ██║   ██║╚════██║
    ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗    ╚██████╔╝███████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚══════╝
                                                                   
    ███████╗███╗   ██╗██████╗  ██████╗  █████╗ ███╗   ███╗███████╗
    ██╔════╝████╗  ██║██╔══██╗██╔════╝ ██╔══██╗████╗ ████║██╔════╝
    █████╗  ██╔██╗ ██║██║  ██║██║  ███╗███████║██╔████╔██║█████╗  
    ██╔══╝  ██║╚██╗██║██║  ██║██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
    ███████╗██║ ╚████║██████╔╝╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
    ╚══════╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
                                                                   
             AI-Powered Investigation Platform v${FORGE_VERSION}
             Obsidian Council - 13 Specialized AI Agents
EOF
    echo -e "${NC}\n"
}

# Step 1: Create base system
create_base_system() {
    section "Creating Ubuntu Base System"
    
    if [ -d "$CHROOT_DIR" ]; then
        log "Cleaning previous build..."
        rm -rf "$CHROOT_DIR"
    fi
    
    log "Bootstrapping Ubuntu 24.04 Noble..."
    debootstrap --arch=amd64 --variant=minbase noble "$CHROOT_DIR" http://archive.ubuntu.com/ubuntu/
    
    # Configure apt sources
    log "Configuring APT sources..."
    cat > "$CHROOT_DIR/etc/apt/sources.list" << EOF
deb http://archive.ubuntu.com/ubuntu/ noble main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ noble-updates main restricted universe multiverse  
deb http://archive.ubuntu.com/ubuntu/ noble-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ noble-backports main restricted universe multiverse
EOF

    log "Base system created successfully"
}

# Step 2: Mount filesystems
mount_filesystems() {
    section "Mounting Virtual Filesystems"
    
    mount -t proc /proc "$CHROOT_DIR/proc" || true
    mount -t sysfs /sys "$CHROOT_DIR/sys" || true
    mount -t devtmpfs /dev "$CHROOT_DIR/dev" || true
    mount -t devpts /dev/pts "$CHROOT_DIR/dev/pts" || true
    mount -t tmpfs /tmp "$CHROOT_DIR/tmp" || true
    
    # Copy resolv.conf for network access
    cp /etc/resolv.conf "$CHROOT_DIR/etc/resolv.conf"
    
    log "Virtual filesystems mounted"
}

# Step 3: Install core packages
install_core_packages() {
    section "Installing Core System Packages"
    
    log "Updating package lists..."
    chroot "$CHROOT_DIR" /bin/bash -c "apt-get update"
    
    log "Installing core system..."
    chroot "$CHROOT_DIR" /bin/bash -c "DEBIAN_FRONTEND=noninteractive apt-get install -y \
        ubuntu-minimal \
        ubuntu-standard \
        linux-generic \
        grub-pc \
        grub-efi-amd64 \
        grub-efi-amd64-signed \
        network-manager \
        systemd \
        cryptsetup \
        lvm2"
    
    log "Installing desktop environment..."
    chroot "$CHROOT_DIR" /bin/bash -c "DEBIAN_FRONTEND=noninteractive apt-get install -y \
        gnome-shell \
        gnome-session \
        gdm3 \
        gnome-terminal \
        nautilus \
        firefox \
        gedit \
        gnome-tweaks \
        gnome-control-center"
    
    log "Core packages installed"
}

# Step 4: Install OSINT and Security Tools
install_osint_tools() {
    section "Installing OSINT and Security Tools"
    
    log "Installing security and forensics tools..."
    chroot "$CHROOT_DIR" /bin/bash -c "DEBIAN_FRONTEND=noninteractive apt-get install -y \
        nmap \
        wireshark \
        tcpdump \
        netcat-openbsd \
        tor \
        torbrowser-launcher \
        aircrack-ng \
        hashcat \
        john \
        sleuthkit \
        autopsy \
        volatility3 \
        yara \
        clamav \
        rkhunter \
        chkrootkit \
        binwalk \
        foremost \
        exiftool \
        steghide"
    
    log "Installing development tools..."
    chroot "$CHROOT_DIR" /bin/bash -c "DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        git \
        vim \
        curl \
        wget \
        build-essential \
        nodejs \
        npm \
        docker.io \
        postgresql \
        postgresql-client \
        redis-server"
    
    log "Installing Python OSINT libraries..."
    chroot "$CHROOT_DIR" /bin/bash -c "pip3 install \
        shodan \
        theHarvester \
        twint \
        instaloader \
        social-analyzer \
        sherlock-project \
        requests \
        beautifulsoup4 \
        selenium \
        scrapy \
        pandas \
        numpy \
        matplotlib \
        plotly \
        networkx \
        folium \
        geopy \
        phonenumbers \
        whois \
        dnspython \
        cryptography \
        pillow"
    
    log "OSINT tools installed"
}

# Step 5: Configure system
configure_system() {
    section "Configuring System Settings"
    
    # Set hostname
    echo "forge-endgame" > "$CHROOT_DIR/etc/hostname"
    
    # Configure hosts
    cat > "$CHROOT_DIR/etc/hosts" << EOF
127.0.0.1   localhost
127.0.1.1   forge-endgame
::1         localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
EOF
    
    # Create investigator user
    log "Creating investigator user..."
    chroot "$CHROOT_DIR" /bin/bash -c "useradd -m -s /bin/bash -G sudo,audio,video,dialout investigator"
    echo "investigator:forge2024!" | chroot "$CHROOT_DIR" chpasswd
    
    # Configure timezone
    chroot "$CHROOT_DIR" /bin/bash -c "ln -sf /usr/share/zoneinfo/UTC /etc/localtime"
    
    # Configure locales
    chroot "$CHROOT_DIR" /bin/bash -c "locale-gen en_US.UTF-8"
    echo "LANG=en_US.UTF-8" > "$CHROOT_DIR/etc/locale.conf"
    
    log "System configured"
}

# Step 6: Install Obsidian Council
install_obsidian_council() {
    section "Installing Obsidian Council AI Framework"
    
    log "Creating Obsidian Council directories..."
    mkdir -p "$CHROOT_DIR/opt/obsidian-council"
    mkdir -p "$CHROOT_DIR/opt/forge-evidence"
    mkdir -p "$CHROOT_DIR/var/lib/obsidian"
    
    # Copy Obsidian Council files
    log "Installing Obsidian Council application..."
    cp -r /forge-os/obsidian-council/* "$CHROOT_DIR/opt/obsidian-council/"
    
    # Install Evidence Management System
    log "Installing Evidence Management System..."
    cp -r /forge-os/applications/* "$CHROOT_DIR/opt/"
    
    # Set permissions
    chroot "$CHROOT_DIR" /bin/bash -c "chown -R investigator:investigator /opt/obsidian-council"
    chroot "$CHROOT_DIR" /bin/bash -c "chown -R investigator:investigator /opt/forge-evidence"
    chroot "$CHROOT_DIR" /bin/bash -c "chmod +x /opt/obsidian-council/bin/*"
    
    log "Obsidian Council installed"
}

# Step 7: Install branding and customizations
install_branding() {
    section "Installing Forge OS Branding"
    
    log "Installing custom themes and branding..."
    
    # Copy wallpapers
    mkdir -p "$CHROOT_DIR/usr/share/backgrounds/forge-os"
    cp -r /forge-os/branding/wallpapers/* "$CHROOT_DIR/usr/share/backgrounds/forge-os/"
    
    # Copy icons
    mkdir -p "$CHROOT_DIR/usr/share/icons/forge-os"
    cp -r /forge-os/branding/icons/* "$CHROOT_DIR/usr/share/icons/forge-os/"
    
    # Copy sounds
    mkdir -p "$CHROOT_DIR/usr/share/sounds/forge-os"
    cp -r /forge-os/branding/sounds/* "$CHROOT_DIR/usr/share/sounds/forge-os/"
    
    # Install GRUB theme
    mkdir -p "$CHROOT_DIR/boot/grub/themes/forge"
    cp -r /forge-os/config/grub-theme/* "$CHROOT_DIR/boot/grub/themes/forge/"
    
    # Install Plymouth theme
    mkdir -p "$CHROOT_DIR/usr/share/plymouth/themes/forge"
    cp -r /forge-os/config/plymouth-theme/* "$CHROOT_DIR/usr/share/plymouth/themes/forge/"
    
    log "Branding installed"
}

# Step 8: Configure desktop environment
configure_desktop() {
    section "Configuring GNOME Desktop"
    
    log "Installing desktop customizations..."
    
    # Copy GNOME configuration
    mkdir -p "$CHROOT_DIR/etc/dconf/db/local.d"
    cp /forge-os/config/gnome/forge-settings.dconf "$CHROOT_DIR/etc/dconf/db/local.d/"
    
    # Create desktop shortcuts
    mkdir -p "$CHROOT_DIR/usr/share/applications"
    
    # Obsidian Council desktop entry
    cat > "$CHROOT_DIR/usr/share/applications/obsidian-council.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Obsidian Council
Comment=AI-Powered Investigation Command Center
Exec=/opt/obsidian-council/bin/start-council
Icon=/usr/share/icons/forge-os/obsidian-council.png
Terminal=false
Categories=ForgeOS;Investigation;OSINT;
StartupWMClass=ObsidianCouncil
EOF
    
    # Evidence Manager desktop entry
    cat > "$CHROOT_DIR/usr/share/applications/evidence-manager.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Evidence Manager
Comment=Digital Evidence Collection and Chain of Custody
Exec=/opt/evidence-manager/evidence_manager.py
Icon=/usr/share/icons/forge-os/evidence-manager.png
Terminal=false
Categories=ForgeOS;Investigation;Security;
EOF
    
    log "Desktop configured"
}

# Step 9: Configure services
configure_services() {
    section "Configuring System Services"
    
    log "Configuring Obsidian Council services..."
    
    # Obsidian Council systemd service
    cat > "$CHROOT_DIR/etc/systemd/system/obsidian-council.service" << EOF
[Unit]
Description=Obsidian Council AI Investigation Framework
After=network.target postgresql.service redis.service

[Service]
Type=forking
User=investigator
Group=investigator
WorkingDirectory=/opt/obsidian-council
ExecStart=/opt/obsidian-council/bin/start-council --daemon
ExecStop=/opt/obsidian-council/bin/stop-council
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable services
    chroot "$CHROOT_DIR" /bin/bash -c "systemctl enable obsidian-council"
    chroot "$CHROOT_DIR" /bin/bash -c "systemctl enable postgresql"
    chroot "$CHROOT_DIR" /bin/bash -c "systemctl enable redis-server"
    chroot "$CHROOT_DIR" /bin/bash -c "systemctl enable gdm3"
    
    log "Services configured"
}

# Step 10: Create ISO
create_iso() {
    section "Creating Forge OS ISO"
    
    log "Cleaning up chroot environment..."
    chroot "$CHROOT_DIR" /bin/bash -c "apt-get clean"
    chroot "$CHROOT_DIR" /bin/bash -c "rm -rf /var/lib/apt/lists/*"
    chroot "$CHROOT_DIR" /bin/bash -c "rm -rf /tmp/*"
    chroot "$CHROOT_DIR" /bin/bash -c "rm -rf /var/tmp/*"
    
    log "Preparing ISO directory structure..."
    mkdir -p "$ISO_DIR"/{casper,isolinux,install,.disk}
    
    # Copy kernel and initrd
    log "Copying kernel and initrd..."
    cp "$CHROOT_DIR"/boot/vmlinuz-* "$ISO_DIR/casper/vmlinuz"
    cp "$CHROOT_DIR"/boot/initrd.img-* "$ISO_DIR/casper/initrd"
    
    # Create filesystem manifest
    log "Creating filesystem manifest..."
    chroot "$CHROOT_DIR" dpkg-query -W --showformat='${Package} ${Version}\n' > "$ISO_DIR/casper/filesystem.manifest"
    cp "$ISO_DIR/casper/filesystem.manifest" "$ISO_DIR/casper/filesystem.manifest-desktop"
    
    # Create squashfs filesystem
    log "Creating compressed filesystem..."
    mksquashfs "$CHROOT_DIR" "$ISO_DIR/casper/filesystem.squashfs" \
        -comp xz -e boot
    
    # Create filesystem size file
    printf $(du -sx --block-size=1 "$CHROOT_DIR" | cut -f1) > "$ISO_DIR/casper/filesystem.size"
    
    # Copy isolinux files
    log "Installing bootloader..."
    cp /usr/lib/ISOLINUX/isolinux.bin "$ISO_DIR/isolinux/"
    cp /usr/lib/syslinux/modules/bios/* "$ISO_DIR/isolinux/"
    
    # Create isolinux configuration
    cat > "$ISO_DIR/isolinux/isolinux.cfg" << EOF
DEFAULT live
LABEL live
  menu label ^Start Forge OS Endgame Edition
  kernel /casper/vmlinuz
  append initrd=/casper/initrd boot=casper quiet splash ---
LABEL persistent
  menu label ^Start Forge OS (Persistent Mode)
  kernel /casper/vmlinuz
  append initrd=/casper/initrd boot=casper persistent quiet splash ---
LABEL forensic
  menu label ^Start Forge OS (Forensic Mode)
  kernel /casper/vmlinuz
  append initrd=/casper/initrd boot=casper toram noautomount quiet splash ---
PROMPT 1
TIMEOUT 100
EOF
    
    # Create disk info
    cat > "$ISO_DIR/.disk/info" << EOF
Forge OS Endgame Edition $FORGE_VERSION - Investigation Platform
EOF
    
    # Create ISO
    log "Building final ISO image..."
    mkdir -p "$OUTPUT_DIR"
    
    xorriso -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid "FORGE_OS_ENDGAME" \
        -output "$OUTPUT_DIR/forge-os-endgame-$FORGE_VERSION.iso" \
        -eltorito-boot isolinux/isolinux.bin \
        -eltorito-catalog isolinux/boot.cat \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        -eltorito-alt-boot \
        -e EFI/boot/bootx64.efi \
        -no-emul-boot \
        "$ISO_DIR"
    
    log "ISO created: forge-os-endgame-$FORGE_VERSION.iso"
    
    # Generate checksums
    cd "$OUTPUT_DIR"
    sha256sum "forge-os-endgame-$FORGE_VERSION.iso" > "forge-os-endgame-$FORGE_VERSION.iso.sha256"
    md5sum "forge-os-endgame-$FORGE_VERSION.iso" > "forge-os-endgame-$FORGE_VERSION.iso.md5"
}

# Cleanup function
cleanup() {
    log "Cleaning up mount points..."
    umount "$CHROOT_DIR/proc" 2>/dev/null || true
    umount "$CHROOT_DIR/sys" 2>/dev/null || true
    umount "$CHROOT_DIR/dev/pts" 2>/dev/null || true
    umount "$CHROOT_DIR/dev" 2>/dev/null || true
    umount "$CHROOT_DIR/tmp" 2>/dev/null || true
}

# Set trap for cleanup
trap cleanup EXIT

# Main build process
main() {
    display_banner
    
    create_base_system
    mount_filesystems
    install_core_packages
    install_osint_tools
    configure_system
    install_obsidian_council
    install_branding
    configure_desktop
    configure_services
    create_iso
    
    section "Build Complete!"
    
    echo -e "${AMBER}📀 ISO Image: ${OUTPUT_DIR}/forge-os-endgame-$FORGE_VERSION.iso${NC}"
    echo -e "${AMBER}🔐 SHA256: $(cat ${OUTPUT_DIR}/forge-os-endgame-$FORGE_VERSION.iso.sha256 | cut -d' ' -f1)${NC}"
    echo -e "${AMBER}📱 Size: $(du -h ${OUTPUT_DIR}/forge-os-endgame-$FORGE_VERSION.iso | cut -f1)${NC}"
    echo -e "\n${GREEN}🎯 Forge OS Endgame Edition is ready for deployment!${NC}"
    echo -e "${GREEN}🧠 Obsidian Council AI agents are integrated and ready${NC}"
    echo -e "${GREEN}🔍 Missing persons and trafficking investigation platform complete${NC}\n"
}

# Run main function
main "$@"