import os
import whisper
import yt_dlp
import re
import subprocess
from datetime import datetime

VIDEO_URL = "https://www.youtube.com/watch?v=jaaK11__MPE" 

ARANACAK_ISIMLER = [
    "mehmet", "mustafa", "ahmet", "ali", "hüseyin", "hasan", "ibrahim", "ismail", "yusuf", "osman",
    "murat", "ömer", "ramazan", "halil", "süleyman", "abdullah", "mahmut", "salih", "kemal", "recep",
    "sinan", "metin", "adem", "fatih", "hakan", "kadir", "emre", "burak", "fırat", "gökhan",
    "serkan", "uğur", "volkan", "mert", "eren", "kaan", "kerem", "arda", "polat", "deniz",
    "barış", "onur", "alper", "can", "cem", "tolga", "berk", "bora", "tunahan", "yiğit",
    "hamza", "muhammed", "enes", "furkan", "yakup", "yunus", "bilal", "cihan", "faruk", "mesut",
    "fatma", "ayşe", "emine", "hatice", "zeynep", "elif", "meryem", "şerife", "sultan", "hanife",
    "merve", "özlem", "esra", "kübra", "büşra", "seda", "gamze", "rabia", "yasemin", "songül",
    "hülya", "dilek", "sevgi", "arzu", "filiz", "tülay", "zeliha", "ayten", "gülten", "aynur",
    "selma", "leyla", "mine", "nuray", "pınar", "ebru", "burcu", "gizem", "beyza", "aslı",
    "didem", "sinem", "ece", "ezgi", "ilayda", "melis", "damla", "irem", "ceren", "selin",
    "nazlı", "hilal", "çağla", "pelinsu", "duygu", "gülşah", "betül", "nur", "melek", "aylin",
    "nurcan", "nurgül", "gülay", "fadime", "semra", "neslihan", "havva", "asiye", "sevim",
    "gülsüm", "tuğba", "tuba", "saniye", "nermin", "ayfer", "figen", "nesrin", "belgin"
]

PADDING_SEC = 0.2
OUTPUT_FOLDER = "turkce_isim_dataset"
INDIRILEN_SESLER_FOLDER = "indirilen_sesler"

MECVUT_KLASOR = os.getcwd()
FFMPEG_EXE = os.path.join(MECVUT_KLASOR, "ffmpeg.exe")

def videoyu_indir(url):
    print(f"⬇️ İndiriliyor: {url}")
    if not os.path.exists(FFMPEG_EXE):
        print(f"HATA: ffmpeg.exe dosyası {MECVUT_KLASOR} içinde bulunamadı!")
        return None
    
    if not os.path.exists(INDIRILEN_SESLER_FOLDER):
        os.makedirs(INDIRILEN_SESLER_FOLDER)
    
    zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_adi = os.path.join(INDIRILEN_SESLER_FOLDER, f"video_{zaman_damgasi}")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': MECVUT_KLASOR,
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'wav'}],
        'outtmpl': dosya_adi,
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['web', 'android']}},
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        wav_dosyasi = f"{dosya_adi}.wav"
        print(f"💾 Ses dosyası kaydedildi: {wav_dosyasi}")
        return wav_dosyasi
    except Exception as e:
        print(f"Hata: {e}")
        return None

def temizle(metin):
    degisim = str.maketrans("AAGIİOOUUŞÇÖĞÜ", "aagıioouuşçöğü") 
    text = metin.translate(degisim).lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def siradaki_dosya_ismini_bul(klasor_yolu, isim):
    i = 1
    while True:
        dosya_adi = f"{isim}_{i}.wav"
        tam_yol = os.path.join(klasor_yolu, dosya_adi)
        if not os.path.exists(tam_yol):
            return tam_yol, dosya_adi
        i += 1

def sesi_kes_ffmpeg(giris, cikis, basla, bitis):
    subprocess.run([FFMPEG_EXE, "-y", "-ss", str(basla), "-t", str(bitis-basla), "-i", giris, "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "-loglevel", "error", cikis])

def ana_islem():
    if not os.path.exists(OUTPUT_FOLDER): 
        os.makedirs(OUTPUT_FOLDER)
    
    wav_dosyasi = videoyu_indir(VIDEO_URL)
    if not wav_dosyasi: 
        return

    print("\n🚀 Yapay Zeka Başlatılıyor...")
    print("📢 İŞLEM BAŞLADI...\n")
    print("-" * 50)
    
    model = whisper.load_model("small") 
    
    # VAD kaldırıldı - standart transcribe
    result = model.transcribe(
        wav_dosyasi, 
        word_timestamps=True, 
        language="tr"
    )

    print("\n📝 WHISPER'IN BULDUĞU METİN:")
    print("=" * 70)
    for i, segment in enumerate(result['segments'], 1):
        print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text']}")
    print("=" * 70)

    print("\n🔍 İsim Taraması Başladı...")
    bulunan_sayisi = 0
    isim_sayaclari = {}

    for segment in result['segments']:
        if 'words' not in segment:
            continue
        
        kelimeler = segment['words']
        
        for idx, word_info in enumerate(kelimeler):
            ham_kelime = word_info['word']
            temiz_kelime = temizle(ham_kelime)
            
            bulunan_isim = None
            for isim in ARANACAK_ISIMLER:
                if temiz_kelime == isim:
                    bulunan_isim = isim
                    break
            
            if bulunan_isim:
                bulunan_sayisi += 1
                
                if bulunan_isim not in isim_sayaclari:
                    isim_sayaclari[bulunan_isim] = 0
                isim_sayaclari[bulunan_isim] += 1
                
                klasor = os.path.join(OUTPUT_FOLDER, bulunan_isim)
                if not os.path.exists(klasor): 
                    os.makedirs(klasor)

                # Komşu kelime kontrolü ile akıllı kesim
                if idx > 0:
                    onceki_kelime = kelimeler[idx - 1]
                    bosluk = word_info['start'] - onceki_kelime['end']
                    if bosluk > 0.1:
                        start = max(0, word_info['start'] - PADDING_SEC)
                    else:
                        start = onceki_kelime['end']
                else:
                    start = max(0, word_info['start'] - PADDING_SEC)
                
                if idx < len(kelimeler) - 1:
                    sonraki_kelime = kelimeler[idx + 1]
                    bosluk = sonraki_kelime['start'] - word_info['end']
                    if bosluk > 0.1:
                        end = word_info['end'] + PADDING_SEC
                    else:
                        end = word_info['end'] + 0.05
                else:
                    end = word_info['end'] + PADDING_SEC
                
                kelime_suresi = word_info['end'] - word_info['start']
                toplam_sure = end - start
                
                dosya_yolu, dosya_adi = siradaki_dosya_ismini_bul(klasor, bulunan_isim)
                
                sesi_kes_ffmpeg(wav_dosyasi, dosya_yolu, start, end)
                print(f"✅ [{word_info['start']:.2f}s - {word_info['end']:.2f}s] {bulunan_isim.upper()} ({kelime_suresi:.2f}s) -> {dosya_adi} | toplam: {toplam_sure:.2f}s")

    print("-" * 70)
    print(f"\n🎉 TOPLAM SONUÇ: {bulunan_sayisi} ses dosyası oluşturuldu!")
    print(f"💾 Orijinal ses dosyası saklandı: {wav_dosyasi}")
    
    if isim_sayaclari:
        print("\n📊 İSİM DAĞILIMI:")
        for isim in sorted(isim_sayaclari.keys()):
            print(f"   {isim.upper()}: {isim_sayaclari[isim]} adet")

if __name__ == "__main__":
    ana_islem()