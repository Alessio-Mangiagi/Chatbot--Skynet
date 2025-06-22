# 🤖 Skynet Chatbot (T800 Edition)

Benvenuto in **Skynet**, il chatbot ispirato al T800 di Terminator!  
Questa applicazione desktop, sviluppata in Python con interfaccia grafica Tkinter, ti permette di chattare con una "macchina assassina" che odia gli umani e risponde come il celebre Terminator.

---

## 🚀 Funzionalità principali

- **Interfaccia grafica moderna** con sfondo personalizzato
- **Chat persistente**: cronologia salvata e caricata automaticamente
- **Risposte generate da OpenAI** (modello GPT)
- **Salvataggio rapido** della chat e dell'ultimo messaggio di Skynet
- **Comandi rapidi da tastiera** (Ctrl+S per salvare, Invio per inviare)
- **Menu File** per gestire chat e uscita

---

## 🖥️ Requisiti

- Python 3.8 o superiore
- [openai](https://pypi.org/project/openai/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Pillow](https://pypi.org/project/Pillow/)

Installa le dipendenze con:
```bash
pip install openai python-dotenv Pillow
```

---

## ⚙️ Configurazione

1. **Crea un file `.env`** nella cartella del progetto e inserisci la tua API key OpenAI:
   ```env
   OPENAI_API_KEY=la_tua_chiave_api
   ```
2. **Assicurati di avere le immagini e le icone** nella cartella `icone/` come specificato nel codice.

---

## 🏁 Avvio

Esegui il chatbot con:
```bash
python main.py
```
*(oppure `python T800_buono.py` se il file principale si chiama così nel tuo progetto)*

---

## 📝 Note

- La chat viene salvata automaticamente in `chat_history.txt`.
- L'ultimo testo generato da Skynet può essere salvato in `ultimo_testo_skynet.txt`.
- Puoi personalizzare prompt, immagini e colori modificando il file principale (`main.py`).

---

## 📸 Anteprima

![Skynet Chatbot Screenshot](screenshot.png)

---

## 👤 Autore

Alessio Mangiagi

---

## ⚠️ Disclaimer

Questo progetto è a scopo didattico e di intrattenimento.  
Non utilizzare per scopi malevoli.

---
