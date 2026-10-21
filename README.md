## 🇬🇧 English

### Classic snake game in the terminal

> [!NOTE]
> A snake game written in Python that runs entirely in the terminal. It has 6 game modes, a separate high score for each mode, and customizable keys and characters. All drawing is done with ANSI escape codes using [pytermkit](https://github.com/UlasKuzgunDev/pytermkit).

> Version: 1.0

## Requirements

- Python 3.12 or newer
- [pynput](https://pypi.org/project/pynput/) (for reading key presses)
- A terminal that supports ANSI colors, at least 71 columns wide and about 45 rows tall

> [!WARNING]
> Key presses are read with `pynput`, which does not work on every system:
> - **Windows:** Works without issues.
> - **macOS:** Works, but the terminal app may need to be allowed under *System Settings → Privacy & Security → Accessibility*.
> - **Linux (X11):** Should work.
> - **Linux (Wayland):** Does not work. When I tested it on Wayland, the game could not detect any key presses, because Wayland does not allow apps to listen to the keyboard globally.
>
> You can check which one your Linux session uses with `echo $XDG_SESSION_TYPE`.

## Download

```bash
git clone https://github.com/UlasKuzgunDev/PySnake
cd PySnake
pip install -r requirements.txt
```

You can also download the project as a ZIP file through the GitHub interface.

## Usage

```bash
python main.py
```

### Main Menu

- `1) Start` — Starts the game. The snake starts moving after the first key press.
- `2) Change game mode` — Selects the game mode.
- `3) Settings` — Changes keys and characters.
- `0) Exit` — Exits the game.

### Controls

| Key | Action |
|:---:|--------|
| `w` | Up |
| `a` | Left |
| `s` | Down |
| `d` | Right |
| `q` | Quit to main menu |

> [!TIP]
> Movement keys can be changed in the settings menu. `q` is reserved and cannot be assigned.

* * *

## Game Modes

| # | Mode | Description |
|:-:|------|-------------|
| 0 | Speed up | Starts at normal speed and gets faster with every food eaten |
| 1 | Easy | Slowest speed |
| 2 | Normal | Normal speed |
| 3 | Faster | Faster than normal |
| 4 | Hard | Fast |
| 5 | Insane | Fastest speed |

> Each mode keeps its own best score. Scores are saved in `data/data.json`.

> [!NOTE]
> Horizontal and vertical movement use different delays, because terminal characters are taller than they are wide. This makes the snake look like it moves at the same speed in every direction.

* * *

## Settings

All settings are saved in `config/settings.json` and can be changed from the menu:

- Up, down, right and left keys
- Snake head character (default: `0`)
- Snake body character (default: `o`)
- Food character (default: `*`)
- Wall character (default: `#`)

> [!WARNING]
> Keys and characters must be a single character. Two actions cannot use the same key.

* * *

## Project Structure

```
PySnake
├── assets
│   └── UI.py
├── config
│   └── settings.json
├── core
│   └── game.py
├── data
│   └── data.json
├── lib
│   └── pytermkit.py
├── main.py
└── requirements.txt
```

- `main.py` — Menus, game loop, drawing and settings.
- `core/game.py` — The `Game` class: game area, snake movement, food and collision checks.
- `assets/UI.py` — Menu texts.
- `lib/pytermkit.py` — Terminal toolkit for colors and cursor control.
- `config/settings.json` — Keys, characters and game mode settings.
- `data/data.json` — Best scores for each mode.
- `requirements.txt` — Required Python packages.

* * *

## 🇹🇷 Türkçe


### Terminalde klasik yılan oyunu

> [!NOTE]
> Tamamen terminalde çalışan, Python ile yazılmış bir yılan oyunu. 6 oyun modu, her mod için ayrı en yüksek skor, değiştirilebilir tuşlar ve karakterler içerir. Tüm çizimler [pytermkit](https://github.com/UlasKuzgunDev/pytermkit) ile ANSI kaçış kodları kullanılarak yapılır.

> Versiyon: 1.0

## Gereksinimler

- Python 3.12 veya daha yeni bir sürüm
- [pynput](https://pypi.org/project/pynput/) (tuş basışlarını okumak için)
- ANSI renklerini destekleyen, en az 71 sütun genişliğinde ve yaklaşık 45 satır yüksekliğinde bir terminal

> [!WARNING]
> Tuş basışları `pynput` ile okunur ve bu kütüphane her sistemde çalışmaz:
> - **Windows:** Sorunsuz çalışır.
> - **macOS:** Çalışır, ancak terminal uygulamasına *Sistem Ayarları → Gizlilik ve Güvenlik → Erişilebilirlik* bölümünden izin vermek gerekebilir.
> - **Linux (X11):** Çalışması beklenir.
> - **Linux (Wayland):** Çalışmaz. Wayland'de denediğimde oyun hiçbir tuş basışını algılamadı, çünkü Wayland uygulamaların klavyeyi sistem genelinde dinlemesine izin vermiyor.
>
> Linux oturumunuzun hangisini kullandığını `echo $XDG_SESSION_TYPE` komutuyla öğrenebilirsiniz.

## İndirme

```bash
git clone https://github.com/UlasKuzgunDev/PySnake
cd PySnake
pip install -r requirements.txt
```

Projeyi GitHub arayüzü üzerinden ZIP olarak da indirebilirsiniz.

## Kullanım

```bash
python main.py
```

### Ana Menü

- `1) Start` — Oyunu başlatır. Yılan ilk tuşa basıldıktan sonra hareket etmeye başlar.
- `2) Change game mode` — Oyun modunu seçer.
- `3) Settings` — Tuşları ve karakterleri değiştirir.
- `0) Exit` — Oyundan çıkar.

### Kontroller

| Tuş | İşlev |
|:---:|-------|
| `w` | Yukarı |
| `a` | Sol |
| `s` | Aşağı |
| `d` | Sağ |
| `q` | Ana menüye dön |

> [!TIP]
> Hareket tuşları ayarlar menüsünden değiştirilebilir. `q` tuşu ayrılmıştır, başka bir işleve atanamaz.

* * *

## Oyun Modları

| # | Mod | Açıklama |
|:-:|-----|----------|
| 0 | Speed up | Normal hızda başlar, her yemde biraz daha hızlanır |
| 1 | Easy | En yavaş hız |
| 2 | Normal | Normal hız |
| 3 | Faster | Normalden hızlı |
| 4 | Hard | Hızlı |
| 5 | Insane | En yüksek hız |

> Her mod kendi en yüksek skorunu tutar. Skorlar `data/data.json` dosyasına kaydedilir.

> [!NOTE]
> Yatay ve dikey hareket için farklı bekleme süreleri kullanılır, çünkü terminal karakterleri enine göre daha uzundur. Bu sayede yılan her yönde aynı hızda gidiyormuş gibi görünür.

* * *

## Ayarlar

Tüm ayarlar `config/settings.json` dosyasında tutulur ve menüden değiştirilebilir:

- Yukarı, aşağı, sağ ve sol tuşları
- Yılanın baş karakteri (varsayılan: `0`)
- Yılanın gövde karakteri (varsayılan: `o`)
- Yem karakteri (varsayılan: `*`)
- Duvar karakteri (varsayılan: `#`)

> [!WARNING]
> Tuşlar ve karakterler tek bir karakter olmalıdır. İki işlev aynı tuşu kullanamaz.

* * *

## Dosya Yapısı

```
PySnake
├── assets
│   └── UI.py
├── config
│   └── settings.json
├── core
│   └── game.py
├── data
│   └── data.json
├── lib
│   └── pytermkit.py
├── main.py
└── requirements.txt
```

- `main.py` — Menüler, oyun döngüsü, çizim ve ayarlar.
- `core/game.py` — `Game` sınıfı: oyun alanı, yılan hareketi, yem ve çarpışma kontrolleri.
- `assets/UI.py` — Menü metinleri.
- `lib/pytermkit.py` — Renk ve imleç kontrolü için terminal araç kiti.
- `config/settings.json` — Tuş, karakter ve oyun modu ayarları.
- `data/data.json` — Her modun en yüksek skorları.
- `requirements.txt` — Gerekli Python paketleri.
