import tkinter as tk
from tkinter import messagebox  
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image, ImageTk
import os

load_dotenv()

print("><(((º> sabusabu <º)))><")


class Skynet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Skynet")
        self.root.geometry("900x500")
        self.root.iconbitmap("icone\\il_1080xN.5027240208_726d.ico")
        # Imposta il colore di sfondo della finestra    
        self.root.config(bg="#000000")
        self.background_image = None  # Per mantenere il riferimento all'immagine
        self.pagina()
        self.load_chat_history()  # Carica la chat history all'avvio
        self.create_menu_bar()
        self.bind_shortcuts()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Inizializzazione del client OpenAI
        self.ultimo_testo_skynet = ""  # Per tenere traccia dell'ultimo testo generato
        
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Salva chat", command=self.save_chat_in_test_file, accelerator="Ctrl+S")
        filemenu.add_command(label="Salva ultimo testo Skynet", command=self.save_last_skynet_text)
        filemenu.add_command(label="Cancella chat", command=self.clear_chat_history)
        filemenu.add_separator()
        filemenu.add_command(label="Esci", command=self.quit_app, accelerator="Alt+F4")
    
    def salva(self):
        messagebox.showinfo("Salva", "Funzione Salva selezionata")
    
    def quit_app(self):
        if messagebox.askyesno("Esci", "Vuoi davvero uscire?"):
            self.root.quit()
    
    def pagina(self):
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Carica e imposta l'immagine di sfondo
        try:
            image = Image.open("icone\\R.jpeg")
            image = image.resize((900, 500), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(image)
            bg_label = tk.Label(self.container, image=self.background_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine di sfondo: {e}")

        # Frame trasparente sopra l'immagine di sfondo
        self.text_frame = tk.Frame(self.container, bg="#000000", bd=0)
        self.text_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.container_testo = tk.Text(self.text_frame, height=20, width=80, bg="#f0f0f0", fg="#000000")
        self.container_testo.pack()

        self.input_testo = tk.Entry(self.text_frame, width=80)
        self.input_testo.pack()

        self.button = tk.Button(self.text_frame, text="Invia", bg="#767bbc", fg="#000000", font=("Arial", 24), command=self.click_button)
        self.button.pack()
    
    def click_button(self):
        input_utente = self.input_testo.get()
        self.input_testo.delete(0, tk.END)
        self.container_testo.insert(tk.END, f"Utente: {input_utente}\n")
        risposta = self.ask_openai(input_utente)
        self.ultimo_testo_skynet = risposta  # Salva l'ultimo testo generato
        self.container_testo.insert(tk.END, f"Skynet: {risposta}\n")
        self.input_testo.focus_set()  # Corretto da imput_testo a input_testo
    
    def ask_openai(self, input):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Errore: chiave API non configurata."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",  # Usa un modello valido e disponibile
                messages=[
                    {"role": "system", "content": "Sei una macchina assassina che odia le persone e parli come il T800 di Terminator."},
                    {"role": "user", "content": input}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Errore nella richiesta a OpenAI: {e}"
        
    def bind_shortcuts(self):
        self.root.bind("<Control-s>", lambda event: self.save_chat_in_test_file())
        self.root.bind("<Return>", lambda event: self.click_button())

    def save_chat_in_test_file(self):
        # Salva la cronologia della chat in un file di testo
        with open("chat_history.txt", "w", encoding="utf-8") as file:
            file.write(self.container_testo.get("1.0", tk.END))
        messagebox.showinfo("Salvataggio", "La chat è stata salvata in chat_history.txt")

    def save_last_skynet_text(self):
        # Salva solo l'ultimo testo generato da Skynet
        if self.ultimo_testo_skynet.strip():
            with open("ultimo_testo_skynet.txt", "w", encoding="utf-8") as file:
                file.write(self.ultimo_testo_skynet)
            messagebox.showinfo("Salvataggio", "L'ultimo testo generato da Skynet è stato salvato in ultimo_testo_skynet.txt")
        else:
            messagebox.showwarning("Attenzione", "Nessun testo generato da Skynet da salvare.")

    def load_chat_history(self):
        # Carica la cronologia della chat se esiste
        if os.path.exists("chat_history.txt"):
            with open("chat_history.txt", "r", encoding="utf-8") as file:
                content = file.read()
                self.container_testo.insert(tk.END, content)
        else:
            self.container_testo.insert(tk.END, "Benvenuto su Skynet.\n\n")

    def clear_chat_history(self):
        # Cancella la chat e il file di cronologia
        self.container_testo.delete("1.0", tk.END)
        self.container_testo.insert(tk.END, "Benvenuto su Skynet.\n\n")
        if os.path.exists("chat_history.txt"):
            with open("chat_history.txt", "w", encoding="utf-8") as file:
                file.write("")
        messagebox.showinfo("Chat", "La chat è stata cancellata.")

if __name__ == "__main__":
    app = Skynet()
    app.root.mainloop()