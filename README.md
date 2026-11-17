# showutc

Ekranın sağ üst köşesinde, her zaman üstte duran küçük bir saat. Anlık **Unix zaman damgasını** (milisaniye) ve saati milisaniye hassasiyetiyle gösterir.

*A tiny always-on-top desktop clock that shows the current Unix timestamp in milliseconds plus local and UTC time with millisecond precision.*

```
1794920472318
yerel 15:01:12.318
UTC   12:01:12.318
```

## Neden?

Log satırlarını, ağ paketlerini ya da farklı cihazlardan gelen zaman damgalarını karşılaştırırken "şu an kaç?" sorusuna terminale `date +%s%3N` yazmadan, göz ucuyla bakarak cevap vermek için.

## Kurulum

Gereksinim: Python 3 ve Tk (`python3-tk`). Başka bağımlılık yok.

```bash
git clone https://github.com/onatender/showutc.git
cd showutc
./install.sh          # ~/.local/bin/showutc bağlantısını oluşturur
```

`~/.local/bin` PATH'te değilse `install.sh` uyarır.

## Kullanım

```bash
showutc           # sağ üst köşe
showutc --left    # sol üst köşe
```

| Eylem | Sonuç |
|---|---|
| Sürükle | Pencereyi taşır |
| Çift tık | Ham zaman damgasını panoya kopyalar |
| Sağ tık / `Esc` | Kapatır |
| Terminalde `Ctrl+C` | Kapatır |

## Ne gösteriyor?

- **Ham değer:** 1 Ocak 1970 00:00 UTC'den bu yana geçen milisaniye. Saat diliminden bağımsızdır; aynı anda dünyanın her yerinde aynıdır.
- **yerel:** Bilgisayarın saat dilimindeki saat.
- **UTC:** Eşgüdümlü evrensel zaman.

Değer işletim sisteminin duvar saatinden (`CLOCK_REALTIME`) okunur; Python'un `time.time()`'ı, C++'ın `std::chrono::system_clock`'u ve `date` komutu aynı saati okur. Farklı bilgisayarların aynı değeri göstermesi için saatlerinin NTP ile eşitlenmiş olması gerekir.

## Notlar

- Wayland oturumlarında pencere XWayland üzerinden açılır; bazı masaüstü ortamları "her zaman üstte" isteğini yerel Wayland pencerelerine karşı uygulamayabilir.
- Ekran ~60 Hz yenilenir.

## Lisans

MIT
