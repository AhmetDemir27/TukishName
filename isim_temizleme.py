def isimleri_tamamen_ayristir(dosya_yolu):
    try:
        benzersiz_kelimeler = set()

        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            for satir in f:
                # Satırı kelimelere ayır (boşluklara göre)
                kelimeler = satir.strip().split()
                for kelime in kelimeler:
                    # Kelimeyi temizle ve sete ekle (tekrarı önler)
                    if kelime:
                        benzersiz_kelimeler.add(kelime.upper())

        # Alfabetik sırala
        sirali_liste = sorted(list(benzersiz_kelimeler))

        # Yeni dosyaya kaydet
        with open('tekil_isimler_listesi.txt', 'w', encoding='utf-8') as f:
            for isim in sirali_liste:
                f.write(isim + '\n')
        
        print(f"İşlem tamam! Toplam {len(sirali_liste)} adet tekil isim bulundu.")
        print("Sonuçlar 'tekil_isimler_listesi.txt' dosyasına kaydedildi.")

    except FileNotFoundError:
        print("Hata: 'isimler.txt' dosyası bulunamadı.")

# Çalıştır
isimleri_tamamen_ayristir('isimler.txt')