# -*- coding: utf-8 -*-
"""
SideClick — автокликер для боковых кнопок мыши (X1/X2).
Переключается боковой кнопкой мыши или F8.

GitHub:   https://github.com/artur0vi4
Telegram: @jamurai
"""

import ctypes
import json
import locale
import os
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk

from pynput import keyboard, mouse

# ============================ О ПРОГРАММЕ ============================
APP_NAME      = "SideClick"
APP_VERSION   = "1.0.0"
AUTHOR_GITHUB = "artur0vi4"
AUTHOR_TG     = "@jamurai"
REPO_URL      = "https://github.com/artur0vi4/sideclick"  # ← проверь адрес своего репо

# страницы «Поддержать проект» на GitHub (RU/EN)
DONATE_URL_RU = "https://github.com/artur0vi4/sideclick/blob/main/docs/RU/Funding.md"
DONATE_URL_EN = "https://github.com/artur0vi4/sideclick/blob/main/docs/EN/Funding.md"
# =====================================================================

# ============================ ЦВЕТОВАЯ ТЕМА ==========================
BG     = "#16161e"   # фон
CARD   = "#1f2335"   # карточки
BORDER = "#2a2e42"   # рамки
FG     = "#c0caf5"   # текст
MUTED  = "#787fa3"   # приглушённый текст
ACCENT = "#7aa2f7"   # акцентный цвет (голубой)
GREEN  = "#9ece6a"   # кнопка старт
RED    = "#f7768e"   # кнопка стоп
FONT   = "Segoe UI"
# =====================================================================

# ============================ ЛОКАЛИЗАЦИЯ ============================
LANGUAGE_NAMES = {
    "en": "English",  "ru": "Русский",  "es": "Español",  "de": "Deutsch",
    "fr": "Français", "pt": "Português", "it": "Italiano", "zh": "中文",
}

LANGUAGES = {
    "en": {
        "tagline": "Auto clicker for your mouse side buttons",
        "settings": "Settings", "cps": "Clicks per second",
        "click_button": "Click button", "hot_button": "Mouse side button",
        "language": "Language", "start": "START", "stop": "STOP",
        "on": "ON", "off": "OFF", "hint": "Toggle: mouse side button or F8",
        "made_by": "Made by",
        "support": "Say thanks ♥",
        "buttons": ["Left", "Right", "Middle"],
        "side": ["X1 — upper side button", "X2 — lower side button"],
    },
    "ru": {
        "tagline": "Автокликер для боковых кнопок мыши",
        "settings": "Настройки", "cps": "Кликов в секунду",
        "click_button": "Кнопка клика", "hot_button": "Боковая кнопка мыши",
        "language": "Язык", "start": "СТАРТ", "stop": "СТОП",
        "on": "ВКЛ", "off": "ВЫКЛ", "hint": "Переключение: боковая кнопка мыши или F8",
        "made_by": "Сделал",
        "support": "Сказать спасибо ♥",
        "buttons": ["Левая", "Правая", "Средняя"],
        "side": ["X1 — верхняя боковая", "X2 — нижняя боковая"],
    },
    "es": {
        "tagline": "Autoclick para los botones laterales del ratón",
        "settings": "Ajustes", "cps": "Clics por segundo",
        "click_button": "Botón de clic", "hot_button": "Botón lateral del ratón",
        "language": "Idioma", "start": "INICIAR", "stop": "DETENER",
        "on": "ACTIVO", "off": "INACTIVO", "hint": "Alternar: botón lateral del ratón o F8",
        "made_by": "Creado por",
        "support": "Di las gracias ♥",
        "buttons": ["Izquierdo", "Derecho", "Medio"],
        "side": ["X1 — lateral superior", "X2 — lateral inferior"],
    },
    "de": {
        "tagline": "Autoklicker für die seitlichen Maustasten",
        "settings": "Einstellungen", "cps": "Klicks pro Sekunde",
        "click_button": "Klick-Taste", "hot_button": "Seitliche Maustaste",
        "language": "Sprache", "start": "START", "stop": "STOPP",
        "on": "AN", "off": "AUS", "hint": "Umschalten: seitliche Maustaste oder F8",
        "made_by": "Erstellt von",
        "support": "Sag Danke ♥",
        "buttons": ["Links", "Rechts", "Mitte"],
        "side": ["X1 — obere Seitentaste", "X2 — untere Seitentaste"],
    },
    "fr": {
        "tagline": "Auto-clic pour les boutons latéraux de la souris",
        "settings": "Paramètres", "cps": "Clics par seconde",
        "click_button": "Bouton de clic", "hot_button": "Bouton latéral de la souris",
        "language": "Langue", "start": "DÉMARRER", "stop": "ARRÊTER",
        "on": "ACTIVÉ", "off": "DÉSACTIVÉ", "hint": "Basculer : bouton latéral de la souris ou F8",
        "made_by": "Créé par",
        "support": "Dire merci ♥",
        "buttons": ["Gauche", "Droite", "Milieu"],
        "side": ["X1 — bouton latéral haut", "X2 — bouton latéral bas"],
    },
    "pt": {
        "tagline": "Auto clique para os botões laterais do mouse",
        "settings": "Configurações", "cps": "Cliques por segundo",
        "click_button": "Botão de clique", "hot_button": "Botão lateral do mouse",
        "language": "Idioma", "start": "INICIAR", "stop": "PARAR",
        "on": "LIGADO", "off": "DESLIGADO", "hint": "Alternar: botão lateral do mouse ou F8",
        "made_by": "Criado por",
        "support": "Dizer obrigado ♥",
        "buttons": ["Esquerdo", "Direito", "Meio"],
        "side": ["X1 — lateral superior", "X2 — lateral inferior"],
    },
    "it": {
        "tagline": "Auto click per i pulsanti laterali del mouse",
        "settings": "Impostazioni", "cps": "Clic al secondo",
        "click_button": "Pulsante di clic", "hot_button": "Pulsante laterale del mouse",
        "language": "Lingua", "start": "AVVIA", "stop": "FERMA",
        "on": "ATTIVO", "off": "DISATTIVO", "hint": "Attiva/disattiva: pulsante laterale del mouse o F8",
        "made_by": "Creato da",
        "support": "Dì grazie ♥",
        "buttons": ["Sinistro", "Destro", "Centrale"],
        "side": ["X1 — laterale superiore", "X2 — laterale inferiore"],
    },
    "zh": {
        "tagline": "鼠标侧键自动点击器",
        "settings": "设置", "cps": "每秒点击次数",
        "click_button": "点击按键", "hot_button": "鼠标侧键",
        "language": "语言", "start": "开始", "stop": "停止",
        "on": "开启", "off": "关闭", "hint": "切换：鼠标侧键或 F8",
        "made_by": "作者",
        "support": "感谢 ♥",
        "buttons": ["左键", "右键", "中键"],
        "side": ["X1 — 上侧键", "X2 — 下侧键"],
    },
}
# =====================================================================

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".sideclick_config.json")


class SideClick(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.clicking = False
        self.mc = mouse.Controller()
        self._interval = 0.1
        self._button_name = "left"
        self._hot_button = mouse.Button.x1
        self._pulse_job = None

        self.config_data = self._load_config()
        self.lang = self.config_data.get("lang") or self._detect_language()
        if self.lang not in LANGUAGES:
            self.lang = "en"
        self.t = LANGUAGES[self.lang]

        self._setup_style()
        self._build_ui()
        self._make_icon()
        self._apply_dark_titlebar()
        self._apply_saved_settings()
        self._update_ui_state()
        self._start_threads()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # --------------------------- иконка окна ---------------------------
    def _make_icon(self):
        """Рисует иконку-мышку прямо кодом, без внешних файлов."""
        img = tk.PhotoImage(width=32, height=32)
        for y in range(4, 28):
            for x in range(9, 23):
                dx = min(x - 9, 22 - x)
                dy = min(y - 4, 27 - y)
                if dx + dy < 2:
                    continue
                img.put(ACCENT, (x, y))
        for y in range(4, 14):
            img.put(BG, (15, y))
            img.put(BG, (16, y))
        for y in range(6, 12):
            img.put(FG, (15, y))
            img.put(FG, (16, y))
        self._icon = img          # держим ссылку, иначе сборщик мусора удалит картинку
        self.iconphoto(True, img)

    # --------------------------- тёмная шапка окна ---------------------------
    @staticmethod
    def _colorref(hex_color):
        """#16161e -> формат COLORREF, который ждёт Windows."""
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return (b << 16) | (g << 8) | r

    def _apply_dark_titlebar(self):
        """Красит шапку окна под тему (Windows 10/11)."""
        try:
            self.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            dwm = ctypes.windll.dwmapi

            def set_attr(attr, value):
                return dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(value), ctypes.sizeof(value))

            # Windows 11: шапка точно в цвет программы + цвет текста + рамка
            try:
                if set_attr(35, ctypes.c_uint(self._colorref(BG))) == 0:   # фон шапки
                    set_attr(36, ctypes.c_uint(self._colorref(FG)))        # цвет текста
                    set_attr(34, ctypes.c_uint(self._colorref(BORDER)))    # рамка окна
                    return
            except Exception:
                pass

            # Windows 10: системный тёмный режим шапки
            for attr in (20, 19):
                if set_attr(attr, ctypes.c_int(1)) == 0:
                    break
        except Exception:
            pass

    # --------------------------- стиль ---------------------------
    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                        foreground=FG, arrowcolor=ACCENT, bordercolor=BORDER,
                        lightcolor=CARD, darkcolor=CARD, borderwidth=1)
        style.map("TCombobox", fieldbackground=[("readonly", CARD)],
                  foreground=[("readonly", FG)])
        style.configure("TSpinbox", fieldbackground=CARD, background=CARD,
                        foreground=FG, arrowcolor=ACCENT, bordercolor=BORDER,
                        lightcolor=CARD, darkcolor=CARD, borderwidth=1)
        self.option_add("*TCombobox*Listbox.background", CARD)
        self.option_add("*TCombobox*Listbox.foreground", FG)
        self.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.option_add("*TCombobox*Listbox.selectForeground", BG)
        self.option_add("*TCombobox*Listbox.font", (FONT, 10))

    # --------------------------- интерфейс ---------------------------
    def _footer_text(self):
        return f"{self.t['made_by']} {AUTHOR_TG}  •  github.com/{AUTHOR_GITHUB}  •  v{APP_VERSION}"

    def _open_donate(self):
        """Открывает страницу поддержки на языке интерфейса."""
        if self.lang == "ru":
            webbrowser.open(DONATE_URL_RU)
        else:
            webbrowser.open(DONATE_URL_EN)

    def _build_ui(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=18, pady=(14, 8))

        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side="left")
        tk.Label(title_box, text=APP_NAME, bg=BG, fg=FG,
                 font=(FONT, 16, "bold")).pack(anchor="w")
        self.tagline_lbl = tk.Label(title_box, text=self.t["tagline"],
                                    bg=BG, fg=MUTED, font=(FONT, 9))
        self.tagline_lbl.pack(anchor="w")
        tk.Label(header, text=f"v{APP_VERSION}", bg=BG, fg=MUTED,
                 font=(FONT, 10)).pack(side="right")

        # карточка настроек
        card = tk.Frame(self, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=18)
        inner = tk.Frame(card, bg=CARD)
        inner.pack(fill="x", padx=14, pady=12)
        inner.columnconfigure(1, weight=1)

        self.lbl_settings = tk.Label(inner, text=self.t["settings"].upper(),
                                     bg=CARD, fg=MUTED, font=(FONT, 9, "bold"))
        self.lbl_settings.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.lbl_cps = tk.Label(inner, text=self.t["cps"], bg=CARD, fg=FG, font=(FONT, 10))
        self.lbl_cps.grid(row=1, column=0, sticky="w", pady=4)
        self.cps_var = tk.StringVar(value="10")
        self.cps_var.trace_add("write", self._on_cps_change)
        ttk.Spinbox(inner, from_=1, to=100, textvariable=self.cps_var,
                    width=8, font=(FONT, 10))\
            .grid(row=1, column=1, sticky="e", pady=4)

        self.lbl_click = tk.Label(inner, text=self.t["click_button"], bg=CARD, fg=FG, font=(FONT, 10))
        self.lbl_click.grid(row=2, column=0, sticky="w", pady=4)
        self.click_combo = ttk.Combobox(inner, values=self.t["buttons"],
                                        state="readonly", width=20, font=(FONT, 10))
        self.click_combo.grid(row=2, column=1, sticky="e", pady=4)
        self.click_combo.bind("<<ComboboxSelected>>", self._on_setting_change)

        self.lbl_hot = tk.Label(inner, text=self.t["hot_button"], bg=CARD, fg=FG, font=(FONT, 10))
        self.lbl_hot.grid(row=3, column=0, sticky="w", pady=4)
        self.hot_combo = ttk.Combobox(inner, values=self.t["side"],
                                      state="readonly", width=20, font=(FONT, 10))
        self.hot_combo.grid(row=3, column=1, sticky="e", pady=4)
        self.hot_combo.bind("<<ComboboxSelected>>", self._on_setting_change)

        self.lbl_lang = tk.Label(inner, text=self.t["language"], bg=CARD, fg=FG, font=(FONT, 10))
        self.lbl_lang.grid(row=4, column=0, sticky="w", pady=(8, 2))
        self.lang_combo = ttk.Combobox(inner, values=list(LANGUAGE_NAMES.values()),
                                       state="readonly", width=20, font=(FONT, 10))
        self.lang_combo.grid(row=4, column=1, sticky="e", pady=(8, 2))
        self.lang_combo.current(list(LANGUAGE_NAMES).index(self.lang))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_change)

        # кнопка старт/стоп
        self.toggle_btn = tk.Button(self, command=self.toggle, relief="flat", bd=0,
                                    bg=GREEN, fg="#10101a", activebackground=GREEN,
                                    activeforeground="#10101a", cursor="hand2",
                                    font=(FONT, 13, "bold"))
        self.toggle_btn.pack(fill="x", padx=18, pady=(12, 4), ipady=9)
        self.toggle_btn.bind("<Enter>", lambda e: self._hover(True))
        self.toggle_btn.bind("<Leave>", lambda e: self._hover(False))

        # индикатор статуса
        status = tk.Frame(self, bg=BG)
        status.pack()
        self.status_dot = tk.Canvas(status, width=12, height=12, bg=BG, highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 7))
        self.dot = self.status_dot.create_oval(2, 2, 10, 10, fill=MUTED, outline="")
        self.status_lbl = tk.Label(status, bg=BG, fg=MUTED, font=(FONT, 11, "bold"))
        self.status_lbl.pack(side="left")

        self.hint_lbl = tk.Label(self, text=self.t["hint"], bg=BG, fg=MUTED, font=(FONT, 9))
        self.hint_lbl.pack(pady=(6, 10))

        # подвал: авторство слева, донат справа
        footer = tk.Frame(self, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        footer.pack(fill="x", side="bottom")

        self.footer_lbl = tk.Label(footer, text=self._footer_text(),
                                   bg=CARD, fg=MUTED, font=(FONT, 9), cursor="hand2")
        self.footer_lbl.pack(side="left", padx=(10, 0), pady=6)
        self.footer_lbl.bind("<Button-1>", lambda e: webbrowser.open(REPO_URL))
        self.footer_lbl.bind("<Enter>", lambda e: self.footer_lbl.config(fg=FG))
        self.footer_lbl.bind("<Leave>", lambda e: self.footer_lbl.config(fg=MUTED))

        self.donate_lbl = tk.Label(footer, text=self.t["support"],
                                   bg=CARD, fg=ACCENT, font=(FONT, 9), cursor="hand2")
        self.donate_lbl.pack(side="right", padx=(0, 10))
        self.donate_lbl.bind("<Button-1>", lambda e: self._open_donate())
        self.donate_lbl.bind("<Enter>", lambda e: self.donate_lbl.config(fg=FG))
        self.donate_lbl.bind("<Leave>", lambda e: self.donate_lbl.config(fg=ACCENT))

    # --------------------------- настройки ---------------------------
    def _apply_saved_settings(self):
        cfg = self.config_data
        try:
            self.cps_var.set(str(int(cfg.get("cps", 10))))
        except (ValueError, TypeError):
            pass
        click_idx = cfg.get("click_index", 0)
        hot_idx = cfg.get("hot_index", 0)
        if isinstance(click_idx, int) and 0 <= click_idx < 3:
            self.click_combo.current(click_idx)
        if isinstance(hot_idx, int) and 0 <= hot_idx < 2:
            self.hot_combo.current(hot_idx)
        self._sync_settings()

    def _sync_settings(self, *_):
        names = ("left", "right", "middle")
        idx = self.click_combo.current()
        if idx >= 0:
            self._button_name = names[idx]
        idx = self.hot_combo.current()
        if idx >= 0:
            self._hot_button = mouse.Button.x1 if idx == 0 else mouse.Button.x2
        self._save_config()

    def _on_setting_change(self, _event=None):
        self._sync_settings()

    def _on_cps_change(self, *_):
        try:
            self._interval = 1.0 / max(1.0, float(self.cps_var.get()))
        except ValueError:
            pass

    def _on_language_change(self, _event=None):
        code = list(LANGUAGE_NAMES)[self.lang_combo.current()]
        if code != self.lang:
            self.lang = code
            self.t = LANGUAGES[code]
            self._retranslate()
            self._save_config()

    def _retranslate(self):
        self.tagline_lbl.config(text=self.t["tagline"])
        self.lbl_settings.config(text=self.t["settings"].upper())
        self.lbl_cps.config(text=self.t["cps"])
        self.lbl_click.config(text=self.t["click_button"])
        self.lbl_hot.config(text=self.t["hot_button"])
        self.lbl_lang.config(text=self.t["language"])
        click_idx = max(0, self.click_combo.current())
        self.click_combo.config(values=self.t["buttons"])
        self.click_combo.current(click_idx)
        hot_idx = max(0, self.hot_combo.current())
        self.hot_combo.config(values=self.t["side"])
        self.hot_combo.current(hot_idx)
        self.hint_lbl.config(text=self.t["hint"])
        self.footer_lbl.config(text=self._footer_text())
        self.donate_lbl.config(text=self.t["support"])
        self._update_ui_state()

    # --------------------------- состояние ---------------------------
    def _update_ui_state(self):
        if self.clicking:
            self.toggle_btn.config(text=self.t["stop"], bg=RED, activebackground=RED)
            self.status_lbl.config(text=self.t["on"], fg=GREEN)
        else:
            self.toggle_btn.config(text=self.t["start"], bg=GREEN, activebackground=GREEN)
            self.status_lbl.config(text=self.t["off"], fg=MUTED)
            self.status_dot.itemconfig(self.dot, fill=MUTED)

    def _hover(self, entered):
        if self.clicking:
            self.toggle_btn.config(bg="#fb8ba4" if entered else RED)
        else:
            self.toggle_btn.config(bg="#b4e19b" if entered else GREEN)

    def toggle(self):
        self.clicking = not self.clicking
        self._update_ui_state()
        if self.clicking:
            self._pulse()
        elif self._pulse_job is not None:
            self.after_cancel(self._pulse_job)
            self._pulse_job = None

    def _pulse(self):
        if self.clicking:
            current = self.status_dot.itemcget(self.dot, "fill")
            self.status_dot.itemconfig(self.dot, fill=MUTED if current == GREEN else GREEN)
            self._pulse_job = self.after(400, self._pulse)
        else:
            self._pulse_job = None

    # --------------------------- фоновая работа ---------------------------
    def _start_threads(self):
        threading.Thread(target=self._clicker_loop, daemon=True).start()
        mouse.Listener(on_click=self._on_mouse_click).start()
        keyboard.Listener(on_press=self._on_key).start()

    def _clicker_loop(self):
        while True:
            if self.clicking:
                self.mc.click(getattr(mouse.Button, self._button_name))
                time.sleep(self._interval)
            else:
                time.sleep(0.05)

    def _on_mouse_click(self, _x, _y, button, pressed):
        if button == self._hot_button and pressed:
            self.after(0, self.toggle)

    def _on_key(self, key):
        if key == keyboard.Key.f8:
            self.after(0, self.toggle)

    # --------------------------- конфиг ---------------------------
    @staticmethod
    def _detect_language():
        try:
            code = (locale.getdefaultlocale()[0] or "en").split("_")[0].lower()
            return code if code in LANGUAGES else "en"
        except Exception:
            return "en"

    @staticmethod
    def _load_config():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_config(self):
        data = {
            "lang": self.lang,
            "cps": self.cps_var.get(),
            "click_index": max(0, self.click_combo.current()),
            "hot_index": max(0, self.hot_combo.current()),
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    def _on_close(self):
        self._save_config()
        self.destroy()
        os._exit(0)


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)   # чёткий текст на HiDPI-экранах
    except Exception:
        pass
    SideClick().mainloop()