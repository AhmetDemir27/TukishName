import math

def listeyi_dorde_bol(kaynak_dosya):
    try:
        # Önce tüm isimleri oku
        with open(kaynak_dosya, 'r', encoding='utf-8') as f:
            isimler = [satir.strip() for satir in f if satir.strip()]
        
        toplam_isim = len(isimler)
        # Her dosyaya düşecek yaklaşık isim sayısı
        parca_boyutu = math.ceil(toplam_isim / 4)
        
        dosya_isimleri = [
            "isim_ahmet.txt",
            "isim_bedirhan.txt",
            "isim_esma.txt",
            "isim_gizem.txt"
        ]
        
        for i in range(4):
            baslangic = i * parca_boyutu
            # Son dosyada listenin sonuna kadar gitmesi için bitisi ayarla
            bitis = (i + 1) * parca_boyutu if i < 3 else toplam_isim
            
            alt_liste = isimler[baslangic:bitis]
            
            with open(dosya_isimleri[i], 'w', encoding='utf-8') as f:
                for isim in alt_liste:
                    f.write(isim + '\n')
            
            print(f"{dosya_isimleri[i]} oluşturuldu. ({len(alt_liste)} isim)")

    except FileNotFoundError:
        print(f"Hata: '{kaynak_dosya}' dosyası bulunamadı.")

# Bir önceki adımda oluşturduğun temizlenmiş dosya adını buraya yaz
listeyi_dorde_bol('tekil_isimler_listesi.txt')