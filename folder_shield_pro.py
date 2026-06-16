import os
import json
import base64
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
import hashlib

# --- Παλέτα Χρωμάτων (Dark Mode) ---
XROMATA = {
    "fonto": "#1e1e2e",        # Σκούρο μπλε φόντο
    "karta": "#2b2b3b",        # Χρώμα πάνελ
    "keimeno": "#cdd6f4",      # Ανοιχτό γκρι
    "tonismos": "#89b4fa",     # Μπλε κουμπιά
    "tonismos_hover": "#b4befe",
    "kindynos": "#f38ba8"      # Κόκκινο για διαγραφή/reset
}

def krypto_kodikos(kodikos):
    # Μετατροπή του κωδικού σε hash για ασφαλή αποθήκευση
    return hashlib.sha256(kodikos.encode()).hexdigest()

def fortosi_rythmiseon():
    # Φόρτωση του αρχείου ρυθμίσεων αν υπάρχει
    if not os.path.exists('config.json'):
        return {"password": None}
    with open('config.json', "r") as f:
        return json.load(f)

class MetatropasAsfaleias(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ασπίδα Φακέλων Pro")
        self.geometry("500x550")
        self.configure(bg=XROMATA["fonto"])
        
        self.dedomena_config = fortosi_rythmiseon()
        self.hash_kodikoy = self.dedomena_config.get("password")
        
        self.stisimo_grafikon()

    def stisimo_grafikon(self):
        # Κεντρικό Πάνελ (Στυλ κάρτας)
        self.karta = tk.Frame(self, bg=XROMATA["karta"], padx=30, pady=30, relief="flat")
        self.karta.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)

        # Επικεφαλίδα και Εικονίδιο
        tk.Label(self.karta, text="🛡️", font=("Arial", 40), bg=XROMATA["karta"], fg=XROMATA["tonismos"]).pack()
        tk.Label(self.karta, text="Folder Shield", font=("Segoe UI", 20, "bold"), 
                 bg=XROMATA["karta"], fg=XROMATA["keimeno"]).pack(pady=(0, 10))
        tk.Label(self.karta, text="Κρυπτογράφηση AES-256", font=("Segoe UI", 9), 
                 bg=XROMATA["karta"], fg="#a6adc8").pack(pady=(0, 30))

        # Κουμπιά Λειτουργιών
        self.ftiaxe_koympi("🔒 ΚΛΕΙΔΩΜΑ ΦΑΚΕΛΟΥ", self.energeia_kleidomatos, XROMATA["tonismos"])
        self.ftiaxe_koympi("🔓 ΞΕΚΛΕΙΔΩΜΑ ΦΑΚΕΛΟΥ", self.energeia_xekleidomatos, XROMATA["tonismos"])
        
        # Κενός χώρος
        tk.Label(self.karta, bg=XROMATA["karta"]).pack(pady=10)
        
        # Κουμπί Επαναφοράς
        self.ftiaxe_koympi("🔄 RESET ΚΩΔΙΚΟΥ", self.epanaphora_kodikoy, XROMATA["kindynos"])

    def ftiaxe_koympi(self, keimeno, entoli, xroma):
        koympi = tk.Button(self.karta, text=keimeno, command=entoli, 
                           bg=xroma, fg=XROMATA["fonto"], font=("Segoe UI", 10, "bold"),
                           relief="flat", cursor="hand2", width=25, height=2)
        koympi.pack(pady=8)
        
        # Εφέ όταν περνάει το ποντίκι από πάνω (Hover)
        koympi.bind("<Enter>", lambda e: koympi.configure(bg="#ffffff"))
        koympi.bind("<Leave>", lambda e: koympi.configure(bg=xroma))

    def paragogi_kleidioy(self, kodikos):
        # Δημιουργία κλειδιού Fernet από τον κωδικό του χρήστη
        return base64.urlsafe_b64encode(hashlib.sha256(kodikos.encode()).digest())

    def energeia_kleidomatos(self):
        if not self.exasfalisi_kodikoy(): return
        path = filedialog.askdirectory(title="Επίλεξε φάκελο για κλείδωμα")
        if not path: return

        kod = self.zita_kodiko("Δώσε κωδικό για κλείδωμα")
        if not kod or not self.epalitheysi_kodikoy(kod):
            messagebox.showerror("Σφάλμα", "Άρνηση Πρόσβασης: Λάθος Κωδικός")
            return

        try:
            kleidi = self.paragogi_kleidioy(kod)
            zip_prosorino = path + ".tmp"
            # Μετατροπή φακέλου σε zip
            shutil.make_archive(zip_prosorino, 'zip', path)
            
            with open(zip_prosorino + ".zip", "rb") as f:
                dedomena = f.read()
                kryptografimena = Fernet(kleidi).encrypt(dedomena)
            
            # Αποθήκευση σε νέο αρχείο .locked
            with open(path + ".locked", "wb") as f:
                f.write(kryptografimena)

            # Διαγραφή αρχικού φακέλου και zip
            shutil.rmtree(path)
            os.remove(zip_prosorino + ".zip")
            messagebox.showinfo("Επιτυχία", f"Ο φάκελος '{os.path.basename(path)}' κλειδώθηκε με ασφάλεια.")
        except Exception as e:
            messagebox.showerror("Σφάλμα Συστήματος", str(e))

    def energeia_xekleidomatos(self):
        path = filedialog.askopenfilename(filetypes=[("Κλειδωμένοι Φάκελοι", "*.locked")])
        if not path: return

        kod = self.zita_kodiko("Δώσε κωδικό για ξεκλείδωμα")
        if not kod or not self.epalitheysi_kodikoy(kod):
            messagebox.showerror("Σφάλμα", "Άρνηση Πρόσβασης")
            return

        try:
            kleidi = self.paragogi_kleidioy(kod)
            with open(path, "rb") as f:
                apokryptografimena = Fernet(kleidi).decrypt(f.read())
            
            prosorino_zip = path.replace(".locked", ".zip")
            with open(prosorino_zip, "wb") as f:
                f.write(apokryptografimena)

            fakelos_proorismoy = path.replace(".locked", "")
            shutil.unpack_archive(prosorino_zip, fakelos_proorismoy, 'zip')
            
            # Καθαρισμός αρχείων
            os.remove(prosorino_zip)
            os.remove(path)
            messagebox.showinfo("Επιτυχία", "Η πρόσβαση στον φάκελο αποκαταστάθηκε.")
        except InvalidToken:
            messagebox.showerror("Σφάλμα", "Λάθος Κλειδί: Τα δεδομένα παραμένουν κλειδωμένα.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))

    def epanaphora_kodikoy(self):
        erotisi = "ΠΡΟΣΟΧΗ: Η επαναφορά θα καταστήσει τους ήδη κλειδωμένους φακέλους ΜΟΝΙΜΑ μη προσβάσιμους. Συνέχεια;"
        if messagebox.askyesno("Επιβεβαίωση", erotisi):
            if os.path.exists('config.json'):
                os.remove('config.json')
            self.hash_kodikoy = None
            messagebox.showinfo("Reset", "Το σύστημα επανήλθε. Κάνε επανεκκίνηση για νέο κωδικό.")
            self.destroy()

    def zita_kodiko(self, titlos):
        return simpledialog.askstring("Έλεγχος Ασφαλείας", titlos, show="*")

    def epalitheysi_kodikoy(self, kod):
        return krypto_kodikos(kod) == self.hash_kodikoy

    def exasfalisi_kodikoy(self):
        # Αν δεν υπάρχει κωδικός, ζητάμε από τον χρήστη να ορίσει έναν Master Password
        if not self.hash_kodikoy:
            k = self.zita_kodiko("Ορίστε έναν νέο Master Password")
            if not k: return False
            self.hash_kodikoy = krypto_kodikos(k)
            with open('config.json', "w") as f:
                json.dump({"password": self.hash_kodikoy}, f)
        return True

if __name__ == "__main__":
    efarmogi = MetatropasAsfaleias()
    efarmogi.mainloop()