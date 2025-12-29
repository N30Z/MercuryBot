#!/usr/bin/env python3
"""
MercuryBot - MongoDB Setup Assistant (Python Version)
Plattformübergreifendes interaktives Setup-Script
Unterstützt: Windows, Linux, macOS
"""

import os
import sys
import platform
import subprocess
import getpass
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def disable():
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.END = ''
        Colors.BOLD = ''

# Disable colors on Windows if not supported
if platform.system() == 'Windows':
    try:
        import colorama
        colorama.init()
    except ImportError:
        Colors.disable()


def print_header():
    """Print script header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}   MercuryBot - MongoDB Setup Assistant   {Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {message}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")


def run_command(command, shell=False, check=True):
    """Run a system command"""
    try:
        if isinstance(command, str):
            command = command.split() if not shell else command

        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {e}")
        return None


def check_mongodb_installed():
    """Check if MongoDB is installed"""
    try:
        result = run_command(['mongod', '--version'], check=False)
        if result and result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False


def check_mongosh_installed():
    """Check if MongoDB Shell is installed"""
    try:
        result = run_command(['mongosh', '--version'], check=False)
        if result and result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False


def test_connection(connection_string):
    """Test MongoDB connection"""
    print_info("Teste MongoDB Verbindung...")

    try:
        result = run_command(
            ['mongosh', connection_string, '--eval', 'db.runCommand({ ping: 1 })'],
            check=False
        )

        if result and result.returncode == 0:
            print_success("Verbindung erfolgreich!")
            return True
        else:
            print_error("Verbindung fehlgeschlagen!")
            if result:
                print_error(result.stderr)
            return False
    except Exception as e:
        print_error(f"Fehler beim Testen der Verbindung: {e}")
        return False


def create_admin_user():
    """Create MongoDB admin user"""
    print_info("Erstelle MongoDB Admin-User...")

    print(f"\n{Colors.YELLOW}Admin-User Konfiguration:{Colors.END}")
    admin_user = input("Admin Username [admin]: ").strip() or "admin"
    admin_pass = getpass.getpass("Admin Passwort: ")

    if not admin_pass:
        print_error("Passwort darf nicht leer sein!")
        return None

    script = f"""
    use admin;
    db.createUser({{
        user: '{admin_user}',
        pwd: '{admin_pass}',
        roles: [
            {{ role: 'userAdminAnyDatabase', db: 'admin' }},
            {{ role: 'readWriteAnyDatabase', db: 'admin' }}
        ]
    }});
    """

    result = run_command(
        ['mongosh', '--eval', script],
        check=False
    )

    if result and result.returncode == 0:
        print_success(f"Admin-User '{admin_user}' erstellt!")
        return {'username': admin_user, 'password': admin_pass}
    else:
        print_error("Fehler beim Erstellen des Admin-Users!")
        if result:
            print_error(result.stderr)
        return None


def create_bot_user():
    """Create MercuryBot database and user"""
    print_info("Erstelle MercuryBot Datenbank und User...")

    print(f"\n{Colors.YELLOW}Bot-User Konfiguration:{Colors.END}")
    bot_user = input("Bot Username [mercurybot]: ").strip() or "mercurybot"
    bot_pass = getpass.getpass("Bot Passwort: ")
    db_name = input("Datenbank Name [mercurybot]: ").strip() or "mercurybot"

    if not bot_pass:
        print_error("Passwort darf nicht leer sein!")
        return None

    script = f"""
    use {db_name};
    db.createUser({{
        user: '{bot_user}',
        pwd: '{bot_pass}',
        roles: [
            {{ role: 'readWrite', db: '{db_name}' }}
        ]
    }});
    """

    result = run_command(
        ['mongosh', '--eval', script],
        check=False
    )

    if result and result.returncode == 0:
        print_success(f"Bot-User '{bot_user}' für Datenbank '{db_name}' erstellt!")
        connection_string = f"mongodb://{bot_user}:{bot_pass}@localhost:27017/{db_name}"
        return {
            'username': bot_user,
            'password': bot_pass,
            'database': db_name,
            'connection_string': connection_string
        }
    else:
        print_error("Fehler beim Erstellen des Bot-Users!")
        if result:
            print_error(result.stderr)
        return None


def enable_authentication():
    """Enable MongoDB authentication"""
    print_info("Authentication muss manuell aktiviert werden.")
    print()
    print_warning("Folge diesen Schritten:")
    print()

    system = platform.system()

    if system == 'Windows':
        config_file = r"C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg"
        print("1. Öffne die Datei:")
        print(f"   {config_file}")
        print("2. Füge folgende Zeilen hinzu oder ändere sie:")
        print("   security:")
        print("     authorization: enabled")
        print("3. Starte MongoDB-Service neu:")
        print("   services.msc → MongoDB Server → Neu starten")
    elif system == 'Darwin':  # macOS
        config_file = "/usr/local/etc/mongod.conf"
        print("1. Bearbeite die Konfigurationsdatei:")
        print(f"   sudo nano {config_file}")
        print("2. Füge folgende Zeilen hinzu:")
        print("   security:")
        print("     authorization: enabled")
        print("3. Starte MongoDB neu:")
        print("   brew services restart mongodb-community@7.0")
    else:  # Linux
        config_file = "/etc/mongod.conf"
        print("1. Bearbeite die Konfigurationsdatei:")
        print(f"   sudo nano {config_file}")
        print("2. Füge folgende Zeilen hinzu:")
        print("   security:")
        print("     authorization: enabled")
        print("3. Starte MongoDB neu:")
        print("   sudo systemctl restart mongod")

    print()
    input("Drücke Enter wenn du fertig bist...")


def update_env_file(connection_string):
    """Update .env file with connection string"""
    print_info("Aktualisiere .env Datei...")

    env_file = Path(".env")
    env_example = Path(".env.example")

    # Create .env from .env.example if it doesn't exist
    if not env_file.exists():
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print_info(".env von .env.example erstellt")
        else:
            print_error(".env oder .env.example nicht gefunden!")
            print_info("Bitte erstelle manuell eine .env Datei")
            return False

    # Read current content
    content = env_file.read_text()

    # Update or add connection string
    if 'DB_CONNECTION_STRING=' in content:
        # Replace existing
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('DB_CONNECTION_STRING='):
                new_lines.append(f'DB_CONNECTION_STRING={connection_string}')
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)
        print_success("DB_CONNECTION_STRING in .env aktualisiert")
    else:
        # Add new
        content += f"\n\n# MongoDB Connection\nDB_CONNECTION_STRING={connection_string}\n"
        print_success("DB_CONNECTION_STRING zu .env hinzugefügt")

    # Write back
    env_file.write_text(content)
    print_success(".env Datei aktualisiert!")
    print()
    print_info(f"Connection String: {connection_string}")
    return True


def create_indexes(connection_string, db_name):
    """Create database indexes for better performance"""
    print_info("Erstelle Datenbank-Indizes...")

    script = f"""
    use {db_name};
    db.discord.createIndex({{ 'server': 1 }});
    print('Index erstellt');
    """

    result = run_command(
        ['mongosh', connection_string, '--eval', script],
        check=False
    )

    if result and result.returncode == 0:
        print_success("Indizes erstellt!")
        return True
    else:
        print_warning("Konnte Indizes nicht erstellen")
        return False


def install_instructions():
    """Show installation instructions for current OS"""
    system = platform.system()

    print()
    print(f"{Colors.YELLOW}MongoDB Installation:{Colors.END}")
    print()

    if system == 'Windows':
        print("1. Gehe zu: https://www.mongodb.com/try/download/community")
        print("2. Wähle Windows und MSI Installer")
        print("3. Lade herunter und führe den Installer aus")
        print("4. Wähle 'Complete' Installation")
        print("5. Installiere als Windows Service")
    elif system == 'Darwin':  # macOS
        print("1. Installiere Homebrew (falls nicht vorhanden):")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print()
        print("2. Installiere MongoDB:")
        print("   brew tap mongodb/brew")
        print("   brew install mongodb-community@7.0")
        print()
        print("3. Starte MongoDB:")
        print("   brew services start mongodb-community@7.0")
    else:  # Linux
        print("Für Ubuntu/Debian:")
        print()
        print("1. Importiere GPG Key:")
        print("   wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -")
        print()
        print("2. Füge Repository hinzu:")
        print("   echo \"deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse\" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list")
        print()
        print("3. Installiere MongoDB:")
        print("   sudo apt update")
        print("   sudo apt install -y mongodb-org")
        print()
        print("4. Starte MongoDB:")
        print("   sudo systemctl start mongod")
        print("   sudo systemctl enable mongod")

    print()
    print(f"{Colors.BLUE}Ausführliche Anleitung: MONGODB_LOCAL.md{Colors.END}")
    print()


def main_menu():
    """Show main menu and handle user choice"""
    while True:
        print()
        print(f"{Colors.BLUE}Was möchtest du tun?{Colors.END}")
        print("1) Komplettes Setup (User + DB erstellen)")
        print("2) Nur User und DB erstellen")
        print("3) .env Datei aktualisieren")
        print("4) Verbindung testen")
        print("5) Installation-Anleitung anzeigen")
        print("6) Beenden")
        print()

        choice = input("Wähle eine Option [1-6]: ").strip()

        if choice == '1':
            full_setup()
        elif choice == '2':
            setup_users()
        elif choice == '3':
            conn_str = input("Connection String: ").strip()
            if conn_str:
                update_env_file(conn_str)
        elif choice == '4':
            conn_str = input("Connection String: ").strip()
            if conn_str:
                test_connection(conn_str)
        elif choice == '5':
            install_instructions()
        elif choice == '6':
            print_info("Setup beendet")
            break
        else:
            print_error("Ungültige Auswahl!")


def setup_users():
    """Setup MongoDB users"""
    if not check_mongosh_installed():
        print_error("mongosh (MongoDB Shell) ist nicht installiert!")
        print_info("Bitte installiere MongoDB zuerst")
        return

    print()
    admin_result = create_admin_user()
    bot_result = create_bot_user()

    if bot_result:
        print()
        enable_authentication()
        print()
        update_env_file(bot_result['connection_string'])

        print()
        choice = input("Möchtest du Performance-Indizes erstellen? (J/n): ").strip().lower()
        if choice != 'n':
            create_indexes(bot_result['connection_string'], bot_result['database'])


def full_setup():
    """Full setup process"""
    print_header()

    # Check if MongoDB is installed
    if not check_mongodb_installed():
        print_error("MongoDB ist nicht installiert!")
        print()
        install_instructions()
        return

    if not check_mongosh_installed():
        print_error("mongosh (MongoDB Shell) ist nicht installiert!")
        print_info("Wird normalerweise mit MongoDB installiert")
        return

    print_success("MongoDB ist installiert")
    print()

    # Create users
    print_info("Schritt 1/4: User-Erstellung")
    admin_result = create_admin_user()
    bot_result = create_bot_user()

    if not bot_result:
        print_error("Setup fehlgeschlagen!")
        return

    # Enable authentication
    print()
    print_info("Schritt 2/4: Authentication aktivieren")
    enable_authentication()

    # Update .env
    print()
    print_info("Schritt 3/4: .env aktualisieren")
    update_env_file(bot_result['connection_string'])

    # Test connection
    print()
    print_info("Schritt 4/4: Verbindung testen")

    print_warning("Bitte starte MongoDB neu bevor du die Verbindung testest!")
    choice = input("MongoDB neu gestartet? Verbindung testen? (J/n): ").strip().lower()
    if choice != 'n':
        test_connection(bot_result['connection_string'])

    # Create indexes
    print()
    choice = input("Möchtest du Performance-Indizes erstellen? (J/n): ").strip().lower()
    if choice != 'n':
        create_indexes(bot_result['connection_string'], bot_result['database'])

    # Summary
    print()
    print(f"{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}Setup erfolgreich abgeschlossen!{Colors.END}")
    print(f"{Colors.GREEN}{'='*60}{Colors.END}")
    print()
    print_success("MongoDB läuft und ist konfiguriert")
    print_success(".env Datei wurde aktualisiert")
    print_success("MercuryBot kann jetzt gestartet werden!")
    print()
    print_info("Starte den Bot mit: python main.py")
    print()
    print_warning("WICHTIG: Sichere diese Credentials!")
    print(f"Connection String: {bot_result['connection_string']}")
    print()


def main():
    """Main entry point"""
    print_header()

    # Check if running as admin/root (not recommended)
    if os.geteuid() == 0 if hasattr(os, 'geteuid') else False:
        print_warning("Dieses Script als root auszuführen wird nicht empfohlen!")
        print()

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        full_setup()
    else:
        main_menu()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_info("Setup abgebrochen")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"Unerwarteter Fehler: {e}")
        sys.exit(1)
