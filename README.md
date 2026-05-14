# Lumen — Online Kurs Platformu

PyQt5 ile modern, koyu temalı bir online kurs yönetim uygulaması.

## Gereksinimler

```bash
pip install PyQt5
```

## Çalıştırma

```bash
cd kurs_platformu
python main.py
```

İlk açılışta otomatik olarak `data/platform.json` dosyası örnek verilerle oluşturulur. Tüm değişiklikler bu dosyaya otomatik kaydedilir.

## Proje Yapısı

```
kurs_platformu/
├── main.py                    # Uygulama giriş noktası
├── backend/                   # İş mantığı katmanı (UI'dan bağımsız)
│   ├── models.py              # Kurs, Öğrenci, Eğitmen sınıfları
│   └── service.py             # PlatformService - veri yönetimi + JSON persistence
├── frontend/                  # GUI katmanı
│   ├── styles.py              # Renk paleti + QSS stilleri
│   ├── widgets.py             # StatCard, KursCard, OgrenciCard
│   ├── dialogs.py             # Yeni kayıt / detay pencereleri
│   └── main_window.py         # Ana pencere (sidebar + 3 sayfa)
└── data/
    └── platform.json          # Otomatik üretilir
```

## Sınıflar (proje şartnamesine göre)

### `Egitmen`
- `ad`
- `uzmanlik`

### `Ogrenci`
- `ogrenci_id`, `ad`, `email`, `kayitli_kurslar`
- `kurs_listesi(tum_kurslar)` → öğrencinin kayıtlı olduğu kursları döner

### `Kurs`
- `kurs_id`, `kurs_adi`, `egitmen`, `kontenjan`, `kayitli_ogrenciler`
- `ogrenci_kaydet(ogrenci)` → kontenjan / mükerrer kayıt kontrolü ile kayıt yapar

## Özellikler

- **Dashboard** — toplam kurs, öğrenci, aktif kayıt ve ortalama doluluk istatistikleri
- **Kurslar** — 2 sütunlu kart grid'i, her kart için doluluk barı, arama, ekleme/silme/detay
- **Öğrenciler** — baş harfli avatarlı kart listesi, kurs sayısı göstergesi, arama
- **Kayıt akışı** — bir kursa öğrenci kaydetme; kontenjan dolduysa veya mükerrer kayıtta uyarı
- **Otomatik kalıcılık** — her değişiklik anında JSON'a yazılır
- **Türkçe arayüz** — placeholder'lardan onay mesajlarına kadar
