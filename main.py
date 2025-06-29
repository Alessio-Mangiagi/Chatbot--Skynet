import tkinter as tk
from tkinter import messagebox  
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image, ImageTk
import os
import numpy as np  # Per la similarità coseno

load_dotenv()

print("><(((º> sabusabu <º)))><")


class Skynet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Skynet")
        self.root.geometry("900x500")
        self.root.iconbitmap("icone\\il_1080xN.5027240208_726d.ico")   
        self.root.config(bg="#000000")
        self.background_image = None  # Per mantenere il riferimento all'immagine
        self.embedded_text = ""  # Testo embeddato
        self.embedded_vector = None  # Vettore embedding
        self.pagina()
        self.load_chat_history()  # Carica la chat history all'avvio
        self.create_menu_bar()
        self.bind_shortcuts()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Inizializzazione del client OpenAI
        self.ultimo_testo_skynet = ""  # Per tenere traccia dell'ultimo testo generato
        self.root.resizable(True, True)
        
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
        # Aggiungi menu Embedding
        embedding_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Personalizza", menu=embedding_menu)
        embedding_menu.add_command(label="personalizza risposte", command=self.open_embedding_popup)
    
    def salva(self):
        messagebox.showinfo("Salva", "Funzione Salva selezionata")
    
    def quit_app(self):
        if messagebox.askyesno("Esci", "Vuoi davvero uscire?"):
            self.root.quit()
    
    def pagina(self):
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Carica e imposta l'immagine di sfondo (ridimensionabile)
        try:
            self.original_bg_image = Image.open("icone\\R.jpeg")
            self.bg_label = tk.Label(self.container)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.update_background_image(900, 500)
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine di sfondo: {e}")

        # Frame trasparente sopra l'immagine di sfondo
        self.text_frame = tk.Frame(self.container, bg="#000000", bd=0)
        self.text_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.container_testo = tk.Text(self.text_frame, height=20, bg="#000000", fg="#00782E", wrap="word")
        self.container_testo.pack(fill="both", expand=True)

        self.input_testo = tk.Entry(self.text_frame)
        self.input_testo.pack(fill="x", expand=False, pady=(5, 0))

        self.button = tk.Button(self.text_frame, text="Invia", bg="#000000", fg="#CE0000", font=("Arial", 24), command=self.click_button)
        self.button.pack(fill="x", expand=False, pady=(5, 0))

        # Bind per ridimensionamento dinamico
        self.root.bind("<Configure>", self.on_resize)

    def update_background_image(self, width, height):
        # Aggiorna l'immagine di sfondo in base alle dimensioni della finestra
        if hasattr(self, "original_bg_image"):
            resized = self.original_bg_image.resize((max(1, width), max(1, height)), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(resized)
            self.bg_label.config(image=self.background_image)

    def on_resize(self, event):
        # Ridimensiona l'immagine di sfondo e aggiorna i widget
        if event.widget == self.root:
            w = event.width
            h = event.height
            self.update_background_image(w, h)
            # Puoi aggiungere qui altre logiche di ridimensionamento se necessario

    def open_embedding_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("personalizza risposte")
        popup.geometry("600x200")
        popup.resizable(False, False)
        label = tk.Label(popup, text="inserisci il testo:", bg="#000000", fg="#ffffff")
        label.pack(pady=10)
        entry = tk.Entry(popup, width=80)
        entry.pack(pady=5)
        def salva_embedding():
            testo = entry.get()
            if not testo.strip():
                messagebox.showwarning("Attenzione", "Inserisci un testo.")
                return
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=testo
                )
                self.embedded_text = testo
                self.embedded_vector = np.array(response.data[0].embedding)
                messagebox.showinfo("Embedding", "Testo embeddato e salvato!")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'embedding: {e}")
        button = tk.Button(popup, text="Salva embedding", bg="#767bbc", fg="#000000", command=salva_embedding)
        button.pack(pady=10)
        popup.grab_set()

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

        # Se esiste un embedding, calcola la similarità e usa il testo embeddato come contesto se rilevante
        if self.embedded_vector is not None:
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=input
                )
                domanda_vector = np.array(response.data[0].embedding)
                sim = self.cosine_similarity(self.embedded_vector, domanda_vector)
                # Se la similarità è alta, usa il testo embeddato come contesto
                if sim > 0.75:
                    system_prompt = f"Rispondi usando queste informazioni come contesto: {self.embedded_text}"
                else:
                    system_prompt = "Sei una macchina assassina che odia le persone e parli come il T800 di Terminator."
            except Exception as e:
                system_prompt = "Sei una macchina assassina che odia le persone e parli come il T800 di Terminator."
        else:
            system_prompt = "Sei una macchina assassina che odia le persone e parli come il T800 di Terminator."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": input}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Errore nella richiesta a OpenAI: {e}"

    def cosine_similarity(self, vec1, vec2):
        # Calcola la similarità coseno tra due vettori
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        
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