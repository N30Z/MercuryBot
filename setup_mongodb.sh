#!/bin/bash

# MercuryBot - MongoDB Local Setup Script
# Interaktives Setup für lokale MongoDB Installation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║        MercuryBot - MongoDB Setup Assistant           ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "Dieses Script sollte NICHT als root ausgeführt werden!"
        print_info "Bitte führe es als normaler User aus. sudo wird automatisch verwendet wo nötig."
        exit 1
    fi
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
            VER=$VERSION_ID
        else
            print_error "Kann OS nicht erkennen!"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        print_error "Nicht unterstütztes Betriebssystem: $OSTYPE"
        print_info "Bitte folge der manuellen Anleitung in MONGODB_LOCAL.md"
        exit 1
    fi
}

# Check if MongoDB is already installed
check_mongodb_installed() {
    if command -v mongod &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Install MongoDB on Ubuntu/Debian
install_mongodb_ubuntu() {
    print_info "Installiere MongoDB für Ubuntu/Debian..."

    # Import MongoDB public GPG Key
    print_info "Importiere MongoDB GPG Key..."
    wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

    # Create list file
    print_info "Füge MongoDB Repository hinzu..."
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

    # Update package database
    print_info "Aktualisiere Paketliste..."
    sudo apt-get update

    # Install MongoDB
    print_info "Installiere MongoDB Community Edition..."
    sudo apt-get install -y mongodb-org

    # Start MongoDB
    print_info "Starte MongoDB..."
    sudo systemctl start mongod
    sudo systemctl enable mongod

    print_success "MongoDB erfolgreich installiert!"
}

# Install MongoDB on macOS
install_mongodb_macos() {
    print_info "Installiere MongoDB für macOS..."

    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew ist nicht installiert!"
        print_info "Installiere Homebrew zuerst:"
        print_info '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        exit 1
    fi

    print_info "Füge MongoDB tap hinzu..."
    brew tap mongodb/brew

    print_info "Installiere MongoDB Community..."
    brew install mongodb-community@7.0

    print_info "Starte MongoDB..."
    brew services start mongodb-community@7.0

    print_success "MongoDB erfolgreich installiert!"
}

# Create MongoDB admin user
create_admin_user() {
    print_info "Erstelle MongoDB Admin-User..."

    echo ""
    echo -e "${YELLOW}Admin-User Konfiguration:${NC}"
    read -p "Admin Username [admin]: " ADMIN_USER
    ADMIN_USER=${ADMIN_USER:-admin}

    read -s -p "Admin Passwort: " ADMIN_PASS
    echo ""

    if [ -z "$ADMIN_PASS" ]; then
        print_error "Passwort darf nicht leer sein!"
        return 1
    fi

    mongosh --eval "
        use admin;
        db.createUser({
            user: '$ADMIN_USER',
            pwd: '$ADMIN_PASS',
            roles: [
                { role: 'userAdminAnyDatabase', db: 'admin' },
                { role: 'readWriteAnyDatabase', db: 'admin' }
            ]
        });
    " > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        print_success "Admin-User '$ADMIN_USER' erstellt!"
        return 0
    else
        print_error "Fehler beim Erstellen des Admin-Users!"
        return 1
    fi
}

# Create MercuryBot database and user
create_bot_user() {
    print_info "Erstelle MercuryBot Datenbank und User..."

    echo ""
    echo -e "${YELLOW}Bot-User Konfiguration:${NC}"
    read -p "Bot Username [mercurybot]: " BOT_USER
    BOT_USER=${BOT_USER:-mercurybot}

    read -s -p "Bot Passwort: " BOT_PASS
    echo ""

    if [ -z "$BOT_PASS" ]; then
        print_error "Passwort darf nicht leer sein!"
        return 1
    fi

    read -p "Datenbank Name [mercurybot]: " DB_NAME
    DB_NAME=${DB_NAME:-mercurybot}

    mongosh --eval "
        use $DB_NAME;
        db.createUser({
            user: '$BOT_USER',
            pwd: '$BOT_PASS',
            roles: [
                { role: 'readWrite', db: '$DB_NAME' }
            ]
        });
    " > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        print_success "Bot-User '$BOT_USER' für Datenbank '$DB_NAME' erstellt!"

        # Save connection string
        CONNECTION_STRING="mongodb://$BOT_USER:$BOT_PASS@localhost:27017/$DB_NAME"
        export CONNECTION_STRING
        export DB_NAME
        return 0
    else
        print_error "Fehler beim Erstellen des Bot-Users!"
        return 1
    fi
}

# Enable authentication
enable_authentication() {
    print_info "Aktiviere MongoDB Authentication..."

    if [[ "$OS" == "macos" ]]; then
        CONFIG_FILE="/usr/local/etc/mongod.conf"
    else
        CONFIG_FILE="/etc/mongod.conf"
    fi

    # Backup config file
    sudo cp $CONFIG_FILE ${CONFIG_FILE}.backup

    # Check if security section exists
    if grep -q "^security:" $CONFIG_FILE; then
        print_warning "Security-Sektion existiert bereits"
    else
        # Add security section
        echo "" | sudo tee -a $CONFIG_FILE > /dev/null
        echo "security:" | sudo tee -a $CONFIG_FILE > /dev/null
        echo "  authorization: enabled" | sudo tee -a $CONFIG_FILE > /dev/null
        print_success "Authentication aktiviert"
    fi

    # Restart MongoDB
    print_info "Starte MongoDB neu..."
    if [[ "$OS" == "macos" ]]; then
        brew services restart mongodb-community@7.0
    else
        sudo systemctl restart mongod
    fi

    sleep 3
    print_success "MongoDB wurde neu gestartet"
}

# Update .env file
update_env_file() {
    print_info "Aktualisiere .env Datei..."

    ENV_FILE=".env"

    if [ ! -f "$ENV_FILE" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_info ".env von .env.example erstellt"
        else
            print_error ".env oder .env.example nicht gefunden!"
            print_info "Bitte erstelle manuell eine .env Datei"
            return 1
        fi
    fi

    # Update or add connection string
    if grep -q "^DB_CONNECTION_STRING=" $ENV_FILE; then
        # Replace existing
        sed -i.bak "s|^DB_CONNECTION_STRING=.*|DB_CONNECTION_STRING=$CONNECTION_STRING|" $ENV_FILE
        print_success "DB_CONNECTION_STRING in .env aktualisiert"
    else
        # Add new
        echo "" >> $ENV_FILE
        echo "# MongoDB Connection" >> $ENV_FILE
        echo "DB_CONNECTION_STRING=$CONNECTION_STRING" >> $ENV_FILE
        print_success "DB_CONNECTION_STRING zu .env hinzugefügt"
    fi

    print_success ".env Datei aktualisiert!"
    echo ""
    print_info "Connection String: $CONNECTION_STRING"
}

# Test MongoDB connection
test_connection() {
    print_info "Teste MongoDB Verbindung..."

    mongosh "$CONNECTION_STRING" --eval "db.runCommand({ ping: 1 })" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        print_success "Verbindung erfolgreich!"
        return 0
    else
        print_error "Verbindung fehlgeschlagen!"
        print_info "Prüfe Credentials und MongoDB Status"
        return 1
    fi
}

# Create indexes for better performance
create_indexes() {
    print_info "Erstelle Datenbank-Indizes für bessere Performance..."

    mongosh "$CONNECTION_STRING" --eval "
        use $DB_NAME;
        db.discord.createIndex({ 'server': 1 });
        print('✓ Index für discord.server erstellt');
    " > /dev/null 2>&1

    print_success "Indizes erstellt!"
}

# Main menu
show_menu() {
    echo ""
    echo -e "${BLUE}Was möchtest du tun?${NC}"
    echo "1) Komplettes Setup (empfohlen)"
    echo "2) Nur MongoDB installieren"
    echo "3) Nur User und DB erstellen"
    echo "4) .env Datei aktualisieren"
    echo "5) Verbindung testen"
    echo "6) Abbrechen"
    echo ""
    read -p "Wähle eine Option [1-6]: " choice

    case $choice in
        1) full_setup ;;
        2) install_mongodb ;;
        3) setup_users ;;
        4) update_env_file ;;
        5) test_connection ;;
        6) print_info "Setup abgebrochen"; exit 0 ;;
        *) print_error "Ungültige Auswahl!"; show_menu ;;
    esac
}

# Install MongoDB based on OS
install_mongodb() {
    if check_mongodb_installed; then
        print_warning "MongoDB ist bereits installiert!"
        mongod --version | head -n 1
        read -p "Möchtest du trotzdem fortfahren? (j/N): " continue
        if [[ ! $continue =~ ^[Jj]$ ]]; then
            return 0
        fi
    fi

    detect_os

    case $OS in
        ubuntu|debian)
            install_mongodb_ubuntu
            ;;
        macos)
            install_mongodb_macos
            ;;
        *)
            print_error "Automatische Installation für $OS nicht verfügbar"
            print_info "Bitte folge der manuellen Anleitung in MONGODB_LOCAL.md"
            exit 1
            ;;
    esac
}

# Setup users and database
setup_users() {
    if ! check_mongodb_installed; then
        print_error "MongoDB ist nicht installiert!"
        print_info "Bitte installiere zuerst MongoDB"
        return 1
    fi

    # Check if MongoDB is running
    if ! pgrep -x mongod > /dev/null; then
        print_error "MongoDB läuft nicht!"
        print_info "Starte MongoDB mit: sudo systemctl start mongod"
        return 1
    fi

    create_admin_user
    create_bot_user
    enable_authentication
}

# Full setup
full_setup() {
    print_header

    print_info "Starte komplettes MongoDB Setup..."
    echo ""

    # Step 1: Install MongoDB
    print_info "Schritt 1/5: MongoDB Installation"
    install_mongodb
    sleep 2

    # Step 2: Create users
    print_info "Schritt 2/5: User-Erstellung"
    echo ""
    create_admin_user
    create_bot_user

    # Step 3: Enable auth
    print_info "Schritt 3/5: Authentication aktivieren"
    enable_authentication

    # Step 4: Update .env
    print_info "Schritt 4/5: .env aktualisieren"
    update_env_file

    # Step 5: Test connection
    print_info "Schritt 5/5: Verbindung testen"
    test_connection

    # Optional: Create indexes
    read -p "Möchtest du Performance-Indizes erstellen? (J/n): " create_idx
    if [[ ! $create_idx =~ ^[Nn]$ ]]; then
        create_indexes
    fi

    # Summary
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              Setup erfolgreich abgeschlossen!          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    print_success "MongoDB läuft und ist konfiguriert"
    print_success ".env Datei wurde aktualisiert"
    print_success "MercuryBot kann jetzt gestartet werden!"
    echo ""
    print_info "Starte den Bot mit: python main.py"
    echo ""
    print_warning "WICHTIG: Sichere diese Credentials!"
    echo "Connection String: $CONNECTION_STRING"
    echo ""
}

# Main script execution
main() {
    check_root

    # Check if mongosh is available
    if ! command -v mongosh &> /dev/null; then
        print_warning "mongosh (MongoDB Shell) ist nicht installiert"
        print_info "Wird automatisch mit MongoDB installiert"
    fi

    print_header

    # Check for command line argument
    if [ "$1" == "--auto" ]; then
        full_setup
    else
        show_menu
    fi
}

# Run main function
main "$@"
