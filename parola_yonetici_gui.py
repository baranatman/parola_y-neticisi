import hashlib
import json
import os
import re
import tkinter as tk
from tkinter import messagebox

MASTER_DOSYA = "master.db"
KASA_DOSYA = "kasa.json"

def hashle(veri):
    return hashlib.sha256(veri.encode()).hexdigest()

def guvenlik_testi(parola):
    if len(parola) < 8:
        return False
    if not re.search("[A-Z]", parola):
        return False
    if not re.search("[a-z]", parola):
        return False
    if not re.search("[0-9]", parola):
        return False
    if not re.search("[!@#$%^&*()_+-=]", parola):
        return False
    return True

def parola_puani(parola):
    puan = 0
    if len(parola) >= 8:
        puan += 20
    if len(parola) >= 12:
        puan += 20
    if re.search("[A-Z]", parola):
        puan += 15
    if re.search("[a-z]", parola):
        puan += 15
    if re.search("[0-9]", parola):
        puan += 15
    if re.search("[!@#$%^&*()_+-=]", parola):
        puan += 15
    return puan

def verileri_yukle():
    if not os.path.exists(KASA_DOSYA):
        return {}
    try:
        with open(KASA_DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def verileri_kaydet(veriler):
    with open(KASA_DOSYA, "w", encoding="utf-8") as f:
        json.dump(veriler, f, indent=4, ensure_ascii=False)

class ParolaYoneticisi:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Parola Yöneticisi")
        self.pencere.geometry("850x600")
        self.giris_hakki = 3
        self.giris_ekrani()

    def temizle(self):
        for widget in self.pencere.winfo_children():
            widget.destroy()

    def giris_ekrani(self):
        self.temizle()

        tk.Label(self.pencere, text="Parola Yöneticisi", font=("Arial", 18, "bold")).pack(pady=20)

        if not os.path.exists(MASTER_DOSYA):
            tk.Label(self.pencere, text="İlk kurulum için ana şifre belirleyin").pack()
            self.sifre_giris = tk.Entry(self.pencere, show="*", width=30)
            self.sifre_giris.pack(pady=10)
            tk.Button(self.pencere, text="Ana Şifre Oluştur", command=self.ana_sifre_olustur).pack(pady=10)
        else:
            tk.Label(self.pencere, text="Ana şifreyi girin").pack()
            self.sifre_giris = tk.Entry(self.pencere, show="*", width=30)
            self.sifre_giris.pack(pady=10)
            tk.Button(self.pencere, text="Giriş Yap", command=self.giris_yap).pack(pady=10)

    def ana_sifre_olustur(self):
        sifre = self.sifre_giris.get()

        if not guvenlik_testi(sifre):
            messagebox.showerror("Hata", "Ana şifre güçlü değil. En az 8 karakter, büyük harf, küçük harf, rakam ve özel karakter içermelidir.")
            return

        with open(MASTER_DOSYA, "w", encoding="utf-8") as f:
            f.write(hashle(sifre))

        messagebox.showinfo("Başarılı", "Ana şifre oluşturuldu.")
        self.giris_ekrani()

    def giris_yap(self):
        sifre = self.sifre_giris.get()

        with open(MASTER_DOSYA, "r", encoding="utf-8") as f:
            kayitli_hash = f.read()

        if hashle(sifre) == kayitli_hash:
            messagebox.showinfo("Başarılı", "Giriş başarılı.")
            self.ana_menu()
        else:
            self.giris_hakki -= 1
            if self.giris_hakki == 0:
                messagebox.showerror("Hata", "Giriş hakkınız bitti. Program kapanıyor.")
                self.pencere.destroy()
            else:
                messagebox.showwarning("Hatalı Şifre", f"Hatalı şifre. Kalan hak: {self.giris_hakki}")

    def ana_menu(self):
        self.temizle()

        tk.Label(self.pencere, text="Parola Yöneticisi", font=("Arial", 18, "bold")).pack(pady=10)

        form = tk.Frame(self.pencere)
        form.pack(pady=10)

        tk.Label(form, text="Site Adı:").grid(row=0, column=0, padx=5, pady=5)
        self.site_entry = tk.Entry(form, width=35)
        self.site_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Kullanıcı Adı:").grid(row=1, column=0, padx=5, pady=5)
        self.kullanici_entry = tk.Entry(form, width=35)
        self.kullanici_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Parola:").grid(row=2, column=0, padx=5, pady=5)
        self.parola_entry = tk.Entry(form, width=35, show="*")
        self.parola_entry.grid(row=2, column=1, padx=5, pady=5)

        butonlar = tk.Frame(self.pencere)
        butonlar.pack(pady=10)

        tk.Button(butonlar, text="Kayıt Ekle", width=17, command=self.kayit_ekle).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(butonlar, text="Listele", width=17, command=self.kayitlari_listele).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(butonlar, text="Güncelle", width=17, command=self.kayit_guncelle).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(butonlar, text="Sil", width=17, command=self.kayit_sil).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(butonlar, text="JSON Göster", width=17, command=self.json_goster).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(butonlar, text="Çıkış", width=17, command=self.pencere.destroy).grid(row=2, column=1, padx=5, pady=5)

        alan = tk.Frame(self.pencere)
        alan.pack(pady=10)

        self.sonuc = tk.Text(alan, width=95, height=16)
        self.sonuc.pack(side=tk.LEFT)

        kaydirma = tk.Scrollbar(alan, command=self.sonuc.yview)
        kaydirma.pack(side=tk.RIGHT, fill=tk.Y)

        self.sonuc.config(yscrollcommand=kaydirma.set)

    def alanlari_temizle(self):
        self.site_entry.delete(0, tk.END)
        self.kullanici_entry.delete(0, tk.END)
        self.parola_entry.delete(0, tk.END)

    def kayit_ekle(self):
        site = self.site_entry.get().strip()
        kullanici = self.kullanici_entry.get().strip()
        parola = self.parola_entry.get().strip()

        if site == "" or kullanici == "" or parola == "":
            messagebox.showerror("Hata", "Tüm alanları doldurun.")
            return

        veriler = verileri_yukle()

        if site in veriler:
            messagebox.showwarning("Uyarı", "Bu site zaten kayıtlı. Güncelleme yapabilirsiniz.")
            return

        if not guvenlik_testi(parola):
            messagebox.showerror("Hata", "Parola güçlü değil. En az 8 karakter, büyük harf, küçük harf, rakam ve özel karakter içermelidir.")
            return

        veriler[site] = {
            "kullanici": kullanici,
            "parola_hash": hashle(parola),
            "guvenlik_puani": parola_puani(parola)
        }

        verileri_kaydet(veriler)
        messagebox.showinfo("Başarılı", "Kayıt eklendi.")
        self.alanlari_temizle()
        self.kayitlari_listele()

    def kayitlari_listele(self):
        veriler = verileri_yukle()
        self.sonuc.delete("1.0", tk.END)

        if not veriler:
            self.sonuc.insert(tk.END, "Kayıt bulunamadı.")
            return

        for site, bilgiler in veriler.items():
            self.sonuc.insert(tk.END, f"Site: {site}\n")
            self.sonuc.insert(tk.END, f"Kullanıcı: {bilgiler.get('kullanici', '')}\n")
            self.sonuc.insert(tk.END, f"Şifre Hash: {bilgiler.get('parola_hash', '')}\n")
            self.sonuc.insert(tk.END, f"Güvenlik Puanı: {bilgiler.get('guvenlik_puani', '')}\n")
            self.sonuc.insert(tk.END, "-" * 70 + "\n")

    def kayit_guncelle(self):
        site = self.site_entry.get().strip()
        kullanici = self.kullanici_entry.get().strip()
        parola = self.parola_entry.get().strip()

        if site == "" or kullanici == "" or parola == "":
            messagebox.showerror("Hata", "Güncellemek için tüm alanları doldurun.")
            return

        veriler = verileri_yukle()

        if site not in veriler:
            messagebox.showerror("Hata", "Bu siteye ait kayıt bulunamadı.")
            return

        if not guvenlik_testi(parola):
            messagebox.showerror("Hata", "Yeni parola güçlü değil.")
            return

        veriler[site] = {
            "kullanici": kullanici,
            "parola_hash": hashle(parola),
            "guvenlik_puani": parola_puani(parola)
        }

        verileri_kaydet(veriler)
        messagebox.showinfo("Başarılı", "Kayıt güncellendi.")
        self.alanlari_temizle()
        self.kayitlari_listele()

    def kayit_sil(self):
        site = self.site_entry.get().strip()

        if site == "":
            messagebox.showerror("Hata", "Silmek için site adını girin.")
            return

        veriler = verileri_yukle()

        if site in veriler:
            del veriler[site]
            verileri_kaydet(veriler)
            messagebox.showinfo("Başarılı", "Kayıt silindi.")
            self.alanlari_temizle()
            self.kayitlari_listele()
        else:
            messagebox.showerror("Hata", "Kayıt bulunamadı.")

    def json_goster(self):
        veriler = verileri_yukle()
        self.sonuc.delete("1.0", tk.END)
        self.sonuc.insert(tk.END, json.dumps(veriler, indent=4, ensure_ascii=False))

pencere = tk.Tk()
uygulama = ParolaYoneticisi(pencere)
pencere.mainloop()