"""
Minimalist & Smart Text Editor
Designed with a modern, distraction-free aesthetic, dynamic themes,
and smart productivity tools.
"""

import math
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkfont


# ==========================================
# THEME CONFIGURATIONS
# ==========================================
THEMES = {
    "dark": {
        "name": "Dark Zinc",
        "icon": "🌙",
        "window_bg": "#121214",
        "header_bg": "#18181b",
        "header_fg": "#a1a1aa",
        "header_btn_bg": "#222227",
        "header_btn_fg": "#e4e4e7",
        "header_btn_hover": "#2e2e36",
        "header_btn_active": "#3f3f46",
        "editor_bg": "#18181b",
        "editor_fg": "#f4f4f5",
        "gutter_bg": "#141416",
        "gutter_fg": "#52525b",
        "gutter_active_fg": "#a1a1aa",
        "accent": "#8b5cf6",
        "accent_hover": "#7c3aed",
        "accent_text": "#ffffff",
        "select_bg": "#373059",
        "select_fg": "#ffffff",
        "cursor": "#a78bfa",
        "current_line": "#1e1e24",
        "status_bg": "#141416",
        "status_fg": "#71717a",
        "find_bg": "#1a1a1e",
        "find_border": "#27272a",
        "find_fg": "#f4f4f5",
        "border": "#27272a",
        "highlight_bg": "#4c1d95",
        "highlight_fg": "#ffffff",
        "badge_bg": "#27272a",
        "badge_fg": "#d4d4d8",
    },
    "light": {
        "name": "Clean Slate",
        "icon": "☀️",
        "window_bg": "#f4f4f6",
        "header_bg": "#ffffff",
        "header_fg": "#52525b",
        "header_btn_bg": "#f1f1f4",
        "header_btn_fg": "#27272a",
        "header_btn_hover": "#e4e4e7",
        "header_btn_active": "#d4d4d8",
        "editor_bg": "#ffffff",
        "editor_fg": "#18181b",
        "gutter_bg": "#f9f9fb",
        "gutter_fg": "#a1a1aa",
        "gutter_active_fg": "#52525b",
        "accent": "#6366f1",
        "accent_hover": "#4f46e5",
        "accent_text": "#ffffff",
        "select_bg": "#c7d2fe",
        "select_fg": "#1e1b4b",
        "cursor": "#4f46e5",
        "current_line": "#f8f9fa",
        "status_bg": "#f4f4f6",
        "status_fg": "#71717a",
        "find_bg": "#ffffff",
        "find_border": "#e4e4e7",
        "find_fg": "#18181b",
        "border": "#e4e4e7",
        "highlight_bg": "#fde047",
        "highlight_fg": "#000000",
        "badge_bg": "#e4e4e7",
        "badge_fg": "#3f3f46",
    },
    "sepia": {
        "name": "Warm Paper",
        "icon": "📜",
        "window_bg": "#f2ecde",
        "header_bg": "#faf6eb",
        "header_fg": "#60564e",
        "header_btn_bg": "#ece4d3",
        "header_btn_fg": "#3b342e",
        "header_btn_hover": "#dfd5c1",
        "header_btn_active": "#d2c7b1",
        "editor_bg": "#faf6eb",
        "editor_fg": "#2c2520",
        "gutter_bg": "#f2ecde",
        "gutter_fg": "#9e9185",
        "gutter_active_fg": "#5c5044",
        "accent": "#c26a27",
        "accent_hover": "#a8541c",
        "accent_text": "#ffffff",
        "select_bg": "#e6d3bf",
        "select_fg": "#2c2520",
        "cursor": "#c26a27",
        "current_line": "#f4eedf",
        "status_bg": "#ece4d3",
        "status_fg": "#7c6f63",
        "find_bg": "#faf6eb",
        "find_border": "#dfd5c1",
        "find_fg": "#2c2520",
        "border": "#dfd5c1",
        "highlight_bg": "#fed7aa",
        "highlight_fg": "#431407",
        "badge_bg": "#dfd5c1",
        "badge_fg": "#453c34",
    },
}


class SmartTextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Minimalist Text Editor")
        self.geometry("980x680")
        self.minsize(580, 400)

        # State tracking
        self.current_filepath = None
        self.is_modified = False
        self.current_theme_key = "dark"
        self.zen_mode = False
        self.font_size = 13
        self.search_matches = []
        self.current_match_index = -1

        # Typography configuration
        self._init_fonts()

        # Build UI layout
        self._build_ui()

        # Keyboard shortcuts
        self._setup_bindings()

        # Apply initial theme
        self.apply_theme("dark")

        # Set initial title & stats
        self._update_title()
        self._update_stats()

    def _init_fonts(self):
        """Pick the best available modern fonts on the system."""
        available = set(tkfont.families(self))

        # Modern code fonts in order of preference
        code_candidates = [
            "Cascadia Code",
            "JetBrains Mono",
            "Fira Code",
            "Consolas",
            "Menlo",
            "Courier New",
        ]
        self.editor_font_family = next(
            (f for f in code_candidates if f in available), "Courier New"
        )

        # Modern UI fonts
        ui_candidates = ["Segoe UI", "SF Pro Text", "Helvetica Neue", "Arial"]
        self.ui_font_family = next(
            (f for f in ui_candidates if f in available), "Segoe UI"
        )

        self.editor_font = tkfont.Font(
            family=self.editor_font_family, size=self.font_size
        )
        self.gutter_font = tkfont.Font(
            family=self.editor_font_family, size=self.font_size
        )
        self.ui_font = tkfont.Font(family=self.ui_font_family, size=9)
        self.ui_bold_font = tkfont.Font(
            family=self.ui_font_family, size=9, weight="bold"
        )
        self.ui_title_font = tkfont.Font(
            family=self.ui_font_family, size=10, weight="bold"
        )

    def _build_ui(self):
        """Build the modern minimalist interface."""
        # Main container
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # 1. Top Sleek Header Bar
        self.header = tk.Frame(self.container, height=44, padx=14, pady=6)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Left Header: App Brand + File Status Pill
        self.header_left = tk.Frame(self.header)
        self.header_left.pack(side="left", fill="y")

        self.brand_label = tk.Label(
            self.header_left,
            text="✦ EDIT",
            font=self.ui_title_font,
            cursor="hand2",
        )
        self.brand_label.pack(side="left", padx=(0, 10))

        self.title_pill = tk.Label(
            self.header_left,
            text="Untitled",
            font=self.ui_font,
            padx=10,
            pady=2,
            relief="flat",
        )
        self.title_pill.pack(side="left")

        # Right Header: Minimal Action Toolbar
        self.header_right = tk.Frame(self.header)
        self.header_right.pack(side="right", fill="y")

        self.btn_new = self._create_header_btn(
            self.header_right, "＋ New", self.new_file, tooltip="New File (Ctrl+N)"
        )
        self.btn_open = self._create_header_btn(
            self.header_right, "📂 Open", self.open_file, tooltip="Open File (Ctrl+O)"
        )
        self.btn_save = self._create_header_btn(
            self.header_right, "💾 Save", self.save_file, tooltip="Save File (Ctrl+S)"
        )
        self.btn_find = self._create_header_btn(
            self.header_right, "🔍 Find", self.toggle_find_bar, tooltip="Find & Replace (Ctrl+F)"
        )
        self.btn_zen = self._create_header_btn(
            self.header_right, "⛶ Focus", self.toggle_zen_mode, tooltip="Focus Mode (F11 / Esc to exit)"
        )
        self.btn_theme = self._create_header_btn(
            self.header_right, "🌙 Dark", self.cycle_theme, tooltip="Cycle Theme"
        )

        for btn in [
            self.btn_new,
            self.btn_open,
            self.btn_save,
            self.btn_find,
            self.btn_zen,
            self.btn_theme,
        ]:
            btn.pack(side="left", padx=3)

        # 2. Modern Find & Replace Bar (hidden by default)
        self.find_bar = tk.Frame(self.container, height=40, padx=12, pady=6)
        self.find_bar.pack_propagate(False)

        self.lbl_find = tk.Label(self.find_bar, text="Find:", font=self.ui_font)
        self.lbl_find.pack(side="left", padx=(0, 4))

        self.entry_find = tk.Entry(
            self.find_bar,
            font=self.ui_font,
            relief="flat",
            highlightthickness=1,
            width=18,
        )
        self.entry_find.pack(side="left", padx=(0, 6), ipady=3)
        self.entry_find.bind("<Return>", lambda e: self.find_next())
        self.entry_find.bind("<Shift-Return>", lambda e: self.find_prev())
        self.entry_find.bind("<KeyRelease>", lambda e: self.on_find_key_release(e))

        self.lbl_replace = tk.Label(
            self.find_bar, text="Replace:", font=self.ui_font
        )
        self.lbl_replace.pack(side="left", padx=(6, 4))

        self.entry_replace = tk.Entry(
            self.find_bar,
            font=self.ui_font,
            relief="flat",
            highlightthickness=1,
            width=18,
        )
        self.entry_replace.pack(side="left", padx=(0, 6), ipady=3)
        self.entry_replace.bind("<Return>", lambda e: self.replace_current())

        self.btn_find_prev = self._create_action_btn(
            self.find_bar, "▲", self.find_prev, width=3
        )
        self.btn_find_prev.pack(side="left", padx=2)

        self.btn_find_next = self._create_action_btn(
            self.find_bar, "▼", self.find_next, width=3
        )
        self.btn_find_next.pack(side="left", padx=2)

        self.btn_replace_one = self._create_action_btn(
            self.find_bar, "Replace", self.replace_current
        )
        self.btn_replace_one.pack(side="left", padx=2)

        self.btn_replace_all = self._create_action_btn(
            self.find_bar, "All", self.replace_all
        )
        self.btn_replace_all.pack(side="left", padx=2)

        self.lbl_match_count = tk.Label(
            self.find_bar, text="0 matches", font=self.ui_font
        )
        self.lbl_match_count.pack(side="left", padx=10)

        self.btn_close_find = self._create_action_btn(
            self.find_bar, "✕", self.hide_find_bar, width=3
        )
        self.btn_close_find.pack(side="right", padx=2)

        # 3. Editor & Gutter Workspace
        self.work_area = tk.Frame(self.container)
        self.work_area.pack(fill="both", expand=True)

        # Synchronous Line Numbers Gutter
        self.gutter = tk.Text(
            self.work_area,
            width=4,
            padx=8,
            pady=12,
            takefocus=0,
            border=0,
            font=self.gutter_font,
            state="disabled",
            cursor="left_ptr",
        )
        self.gutter.pack(side="left", fill="y")

        # Scrollbar (sleek minimalist)
        self.scrollbar = ttk.Scrollbar(
            self.work_area, orient="vertical", command=self._on_scrollbar_scroll
        )
        self.scrollbar.pack(side="right", fill="y")

        # Main Text Editor with generous padding
        self.text = tk.Text(
            self.work_area,
            wrap=tk.WORD,
            undo=True,
            autoseparators=True,
            maxundo=-1,
            font=self.editor_font,
            padx=16,
            pady=12,
            border=0,
            relief="flat",
            spacing1=2,  # space above lines
            spacing3=2,  # space below lines
            yscrollcommand=self._on_text_scroll,
        )
        self.text.pack(side="left", fill="both", expand=True)

        # 4. Smart Status Bar
        self.status_bar = tk.Frame(self.container, height=28, padx=14, pady=3)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)

        # Status Left: Cursor Position & Line Count
        self.status_pos = tk.Label(
            self.status_bar, text="Ln 1, Col 1", font=self.ui_font
        )
        self.status_pos.pack(side="left", padx=(0, 10))

        self.status_dot1 = tk.Label(
            self.status_bar, text="•", font=self.ui_font
        )
        self.status_dot1.pack(side="left", padx=(0, 10))

        # Status Word & Character Count
        self.status_words = tk.Label(
            self.status_bar, text="0 words  •  0 chars", font=self.ui_font
        )
        self.status_words.pack(side="left", padx=(0, 10))

        self.status_dot2 = tk.Label(
            self.status_bar, text="•", font=self.ui_font
        )
        self.status_dot2.pack(side="left", padx=(0, 10))

        # Reading time estimate
        self.status_reading = tk.Label(
            self.status_bar, text="0 min read", font=self.ui_font
        )
        self.status_reading.pack(side="left")

        # Status Right: Encoding & Zoom indicator
        self.status_zoom = tk.Label(
            self.status_bar, text="100%", font=self.ui_font, cursor="hand2"
        )
        self.status_zoom.pack(side="right", padx=(10, 0))
        self.status_zoom.bind("<Button-1>", lambda e: self.reset_zoom())

        self.status_dot3 = tk.Label(
            self.status_bar, text="•", font=self.ui_font
        )
        self.status_dot3.pack(side="right", padx=(10, 0))

        self.status_encoding = tk.Label(
            self.status_bar, text="UTF-8", font=self.ui_font
        )
        self.status_encoding.pack(side="right")

        # Floating Exit Focus Pill (visible during Focus mode)
        self.zen_exit_pill = tk.Label(
            self.container,
            text="✕ Exit Focus (ESC)",
            font=self.ui_font,
            padx=12,
            pady=5,
            cursor="hand2",
            relief="flat",
        )
        self.zen_exit_pill.bind("<Button-1>", lambda e: self.toggle_zen_mode())
        self.zen_exit_pill.bind(
            "<Enter>",
            lambda e: self._on_btn_hover(
                self.zen_exit_pill, True, self.current_theme["header_btn_hover"]
            ),
        )
        self.zen_exit_pill.bind(
            "<Leave>",
            lambda e: self._on_btn_hover(
                self.zen_exit_pill, False, self.current_theme["badge_bg"]
            ),
        )

    def _create_header_btn(self, parent, text, command, tooltip=""):
        """Create a rounded minimalist flat button for the header toolbar."""
        btn = tk.Label(
            parent,
            text=text,
            font=self.ui_font,
            padx=10,
            pady=4,
            cursor="hand2",
            relief="flat",
        )
        btn.bind("<Button-1>", lambda e: command())
        btn.bind(
            "<Enter>",
            lambda e: self._on_btn_hover(
                btn, True, self.current_theme["header_btn_hover"]
            ),
        )
        btn.bind(
            "<Leave>",
            lambda e: self._on_btn_hover(
                btn, False, self.current_theme["header_btn_bg"]
            ),
        )
        return btn

    def _create_action_btn(self, parent, text, command, width=None):
        """Create a compact button for bars like Find & Replace."""
        btn = tk.Label(
            parent,
            text=text,
            font=self.ui_font,
            padx=8,
            pady=2,
            cursor="hand2",
            relief="flat",
            width=width,
        )
        btn.bind("<Button-1>", lambda e: command())
        btn.bind(
            "<Enter>",
            lambda e: self._on_btn_hover(
                btn, True, self.current_theme["header_btn_hover"]
            ),
        )
        btn.bind(
            "<Leave>",
            lambda e: self._on_btn_hover(
                btn, False, self.current_theme["header_btn_bg"]
            ),
        )
        return btn

    def _on_btn_hover(self, btn, is_hover, color):
        """Hover styling for custom flat buttons."""
        try:
            btn.config(bg=color)
        except tk.TclError:
            pass

    # ==========================================
    # KEYBOARD SHORTCUTS & EVENT BINDINGS
    # ==========================================
    def _setup_bindings(self):
        # File operations
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-S>", lambda e: self.save_file_as())

        # Find & Replace and Focus Mode Escape
        self.bind("<Control-f>", lambda e: self.toggle_find_bar())
        self.bind("<Escape>", self._handle_escape)
        self.text.bind("<Escape>", self._handle_escape)

        # Distraction Free / Zen Mode
        self.bind("<F11>", lambda e: self.toggle_zen_mode())

        # Font Zoom with Ctrl+MouseWheel & Ctrl +/-
        self.text.bind("<Control-MouseWheel>", self._on_mouse_zoom)
        self.bind("<Control-plus>", lambda e: self.zoom_in())
        self.bind("<Control-equal>", lambda e: self.zoom_in())
        self.bind("<Control-minus>", lambda e: self.zoom_out())
        self.bind("<Control-0>", lambda e: self.reset_zoom())

        # Text modifications & cursor tracking
        self.text.bind("<<Modified>>", self._on_text_modified)
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<ButtonRelease-1>", lambda e: self._update_cursor_pos())

        # Smart Editing Features
        self.text.bind("<Return>", self._handle_smart_return)
        self.text.bind("<Tab>", self._handle_smart_tab)
        self.text.bind("<ISO_Left_Tab>", self._handle_smart_untab)
        self.text.bind("<Shift-Tab>", self._handle_smart_untab)
        self.text.bind("<KeyPress>", self._handle_auto_pair)

        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

    def _handle_escape(self, event=None):
        """Escape closes find bar if open, or exits Focus/Zen mode if active."""
        if self.find_bar.winfo_ismapped():
            self.hide_find_bar()
            return "break"
        if self.zen_mode:
            self.toggle_zen_mode()
            return "break"
        return None

    # ==========================================
    # SMART EDITING BEHAVIORS
    # ==========================================
    def _handle_smart_return(self, event):
        """Auto-indent the new line to match the previous line indentation."""
        cursor_index = self.text.index(tk.INSERT)
        current_line_num = cursor_index.split(".")[0]
        current_line = self.text.get(
            f"{current_line_num}.0", f"{current_line_num}.end"
        )

        # Find leading whitespace
        indent_match = re.match(r"^(\s*)", current_line)
        indent = indent_match.group(1) if indent_match else ""

        # Extra indentation if previous line ended with colon/brace/parenthesis
        stripped = current_line.rstrip()
        if stripped.endswith((":", "{", "[", "(")):
            indent += "    "

        self.text.insert(tk.INSERT, "\n" + indent)
        self.text.see(tk.INSERT)
        self._update_line_numbers()
        self._update_stats()
        return "break"

    def _handle_smart_tab(self, event):
        """Indent by 4 spaces or indent highlighted block."""
        try:
            sel_start = self.text.index(tk.SEL_FIRST)
            sel_end = self.text.index(tk.SEL_LAST)
        except tk.TclError:
            # No selection: insert 4 spaces
            self.text.insert(tk.INSERT, "    ")
            return "break"

        start_line = int(sel_start.split(".")[0])
        end_line = int(sel_end.split(".")[0])

        for line_num in range(start_line, end_line + 1):
            self.text.insert(f"{line_num}.0", "    ")
        return "break"

    def _handle_smart_untab(self, event):
        """Shift-Tab dedents 4 spaces."""
        try:
            sel_start = self.text.index(tk.SEL_FIRST)
            sel_end = self.text.index(tk.SEL_LAST)
            start_line = int(sel_start.split(".")[0])
            end_line = int(sel_end.split(".")[0])
        except tk.TclError:
            start_line = int(self.text.index(tk.INSERT).split(".")[0])
            end_line = start_line

        for line_num in range(start_line, end_line + 1):
            line_text = self.text.get(f"{line_num}.0", f"{line_num}.end")
            if line_text.startswith("    "):
                self.text.delete(f"{line_num}.0", f"{line_num}.4")
            elif line_text.startswith("\t") or line_text.startswith(" "):
                self.text.delete(f"{line_num}.0", f"{line_num}.1")
        return "break"

    def _handle_auto_pair(self, event):
        """Auto-close brackets and quotes gracefully."""
        pairs = {"(": ")", "[": "]", "{": "}", '"': '"', "'": "'"}
        char = event.char

        if char in pairs:
            # If text is selected, wrap the selection
            try:
                sel_start = self.text.index(tk.SEL_FIRST)
                sel_end = self.text.index(tk.SEL_LAST)
                selected_text = self.text.get(sel_start, sel_end)
                self.text.delete(sel_start, sel_end)
                self.text.insert(sel_start, f"{char}{selected_text}{pairs[char]}")
                return "break"
            except tk.TclError:
                # No selection: insert pair and place cursor in middle
                self.text.insert(tk.INSERT, char + pairs[char])
                self.text.mark_set(tk.INSERT, f"{tk.INSERT}-1c")
                return "break"
        return None

    # ==========================================
    # SCROLL & LINE NUMBER SYNCHRONIZATION
    # ==========================================
    def _on_text_scroll(self, *args):
        """Sync gutter and scrollbar when editor scrolls."""
        self.gutter.yview_moveto(args[0])
        self.scrollbar.set(*args)
        self._update_line_numbers()

    def _on_scrollbar_scroll(self, *args):
        """Sync text and gutter when scrollbar is dragged."""
        self.text.yview(*args)
        self.gutter.yview(*args)

    def _update_line_numbers(self):
        """Re-render line numbers in gutter with smart alignment."""
        line_count = int(self.text.index("end-1c").split(".")[0])
        digits = max(2, len(str(line_count)))
        self.gutter.config(width=digits + 2)

        lines = "\n".join(str(i).rjust(digits) for i in range(1, line_count + 1))

        self.gutter.config(state="normal")
        self.gutter.delete("1.0", tk.END)
        self.gutter.insert("1.0", lines)
        self.gutter.config(state="disabled")

        # Keep gutter scrolled in exact sync with editor
        self.gutter.yview_moveto(self.text.yview()[0])

    # ==========================================
    # EVENT HANDLERS & STATS TRACKING
    # ==========================================
    def _on_text_modified(self, event=None):
        """Track unsaved state changes."""
        if self.text.edit_modified():
            self.is_modified = True
            self._update_title()
            self.text.edit_modified(False)
            self._update_line_numbers()
            self._update_stats()

    def _on_key_release(self, event=None):
        """Update stats on keystrokes."""
        self._update_cursor_pos()
        self._update_stats()

    def _update_cursor_pos(self):
        """Update Ln / Col in status bar."""
        cursor_index = self.text.index(tk.INSERT)
        row, col = cursor_index.split(".")
        self.status_pos.config(text=f"Ln {row}, Col {int(col) + 1}")

    def _update_stats(self):
        """Calculate word count, char count, and estimated reading time."""
        content = self.text.get("1.0", "end-1c")
        char_count = len(content)
        words = re.findall(r"\b\w+\b", content)
        word_count = len(words)

        self.status_words.config(
            text=f"{word_count:,} words  •  {char_count:,} chars"
        )

        # Average reading speed: ~200 words per minute
        reading_minutes = max(1, math.ceil(word_count / 200)) if word_count > 0 else 0
        if reading_minutes <= 1 and word_count > 0:
            reading_str = "1 min read"
        else:
            reading_str = f"{reading_minutes} min read"
        self.status_reading.config(text=reading_str)

    def _update_title(self):
        """Update application title and modern title pill."""
        if self.current_filepath:
            name = os.path.basename(self.current_filepath)
        else:
            name = "Untitled"

        dot = "● " if self.is_modified else ""
        self.title(f"{dot}{name} — Minimalist Editor")
        self.title_pill.config(text=f"{dot}{name}")

    # ==========================================
    # ZOOM CONTROLS
    # ==========================================
    def _on_mouse_zoom(self, event):
        """Zoom with Ctrl+MouseWheel."""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        return "break"

    def zoom_in(self):
        if self.font_size < 36:
            self.font_size += 1
            self._apply_font_size()

    def zoom_out(self):
        if self.font_size > 8:
            self.font_size -= 1
            self._apply_font_size()

    def reset_zoom(self):
        self.font_size = 13
        self._apply_font_size()

    def _apply_font_size(self):
        self.editor_font.config(size=self.font_size)
        self.gutter_font.config(size=self.font_size)
        percent = int((self.font_size / 13) * 100)
        self.status_zoom.config(text=f"{percent}%")
        self._update_line_numbers()

    # ==========================================
    # ZEN / DISTRACTION-FREE MODE
    # ==========================================
    def toggle_zen_mode(self):
        """Toggle distraction-free writing canvas."""
        self.zen_mode = not self.zen_mode
        if self.zen_mode:
            self.header.pack_forget()
            self.status_bar.pack_forget()
            self.gutter.pack_forget()
            self.find_bar.pack_forget()
            self.scrollbar.pack_forget()
            # Add generous breathing room in zen mode
            self.text.config(padx=120, pady=40)
            self.btn_zen.config(text="⛶ Exit Zen")
            # Show floating exit pill in the top-right corner
            self.zen_exit_pill.config(
                bg=self.current_theme["badge_bg"],
                fg=self.current_theme["badge_fg"],
            )
            self.zen_exit_pill.place(relx=0.98, rely=0.02, anchor="ne")
        else:
            self.zen_exit_pill.place_forget()
            self.text.config(padx=16, pady=12)

            # Reset pack ordering cleanly so header is always at the top
            self.work_area.pack_forget()
            self.header.pack(fill="x", side="top")
            self.status_bar.pack(fill="x", side="bottom")
            self.work_area.pack(fill="both", expand=True)

            # Restore gutter on left and scrollbar on right
            self.gutter.pack(side="left", fill="y", before=self.text)
            self.scrollbar.pack(side="right", fill="y", before=self.text)

            self.btn_zen.config(text="⛶ Focus")
            self._update_line_numbers()

    # ==========================================
    # THEME SWITCHING
    # ==========================================
    def cycle_theme(self):
        """Cycle through Dark -> Light -> Sepia -> Dark."""
        order = ["dark", "light", "sepia"]
        next_idx = (order.index(self.current_theme_key) + 1) % len(order)
        self.apply_theme(order[next_idx])

    def apply_theme(self, theme_key):
        """Apply colors, tags, and styling cleanly."""
        self.current_theme_key = theme_key
        t = THEMES[theme_key]
        self.current_theme = t

        # Update theme button label
        self.btn_theme.config(text=f"{t['icon']} {t['name'].split()[0]}")

        # Window & containers
        self.config(bg=t["window_bg"])
        self.container.config(bg=t["window_bg"])
        self.work_area.config(bg=t["window_bg"])

        # Header
        self.header.config(bg=t["header_bg"])
        self.header_left.config(bg=t["header_bg"])
        self.header_right.config(bg=t["header_bg"])
        self.brand_label.config(
            bg=t["header_bg"], fg=t["accent"], activebackground=t["header_bg"]
        )
        self.title_pill.config(bg=t["badge_bg"], fg=t["badge_fg"])
        if hasattr(self, "zen_exit_pill"):
            self.zen_exit_pill.config(bg=t["badge_bg"], fg=t["badge_fg"])

        # Header buttons
        for btn in [
            self.btn_new,
            self.btn_open,
            self.btn_save,
            self.btn_find,
            self.btn_zen,
            self.btn_theme,
        ]:
            btn.config(bg=t["header_btn_bg"], fg=t["header_btn_fg"])

        # Find bar
        self.find_bar.config(bg=t["find_bg"])
        self.lbl_find.config(bg=t["find_bg"], fg=t["find_fg"])
        self.lbl_replace.config(bg=t["find_bg"], fg=t["find_fg"])
        self.lbl_match_count.config(bg=t["find_bg"], fg=t["status_fg"])
        self.entry_find.config(
            bg=t["header_btn_bg"],
            fg=t["find_fg"],
            insertbackground=t["cursor"],
            highlightbackground=t["find_border"],
            highlightcolor=t["accent"],
        )
        self.entry_replace.config(
            bg=t["header_btn_bg"],
            fg=t["find_fg"],
            insertbackground=t["cursor"],
            highlightbackground=t["find_border"],
            highlightcolor=t["accent"],
        )
        for abtn in [
            self.btn_find_prev,
            self.btn_find_next,
            self.btn_replace_one,
            self.btn_replace_all,
            self.btn_close_find,
        ]:
            abtn.config(bg=t["header_btn_bg"], fg=t["header_btn_fg"])

        # Gutter
        self.gutter.config(
            bg=t["gutter_bg"],
            fg=t["gutter_fg"],
            selectbackground=t["gutter_bg"],
            selectforeground=t["gutter_fg"],
        )

        # Editor
        self.text.config(
            bg=t["editor_bg"],
            fg=t["editor_fg"],
            insertbackground=t["cursor"],
            selectbackground=t["select_bg"],
            selectforeground=t["select_fg"],
        )

        # Search highlight tag
        self.text.tag_config(
            "search_highlight",
            background=t["highlight_bg"],
            foreground=t["highlight_fg"],
        )
        self.text.tag_config(
            "search_current",
            background=t["accent"],
            foreground=t["accent_text"],
        )

        # Status Bar
        self.status_bar.config(bg=t["status_bg"])
        for lbl in [
            self.status_pos,
            self.status_words,
            self.status_reading,
            self.status_encoding,
            self.status_zoom,
            self.status_dot1,
            self.status_dot2,
            self.status_dot3,
        ]:
            lbl.config(bg=t["status_bg"], fg=t["status_fg"])

        self._update_line_numbers()

    # ==========================================
    # FIND & REPLACE FUNCTIONALITY
    # ==========================================
    def toggle_find_bar(self):
        """Show or hide the Find & Replace bar."""
        if self.find_bar.winfo_ismapped():
            self.hide_find_bar()
        else:
            self.show_find_bar()

    def show_find_bar(self):
        # Insert find bar directly below header
        self.find_bar.pack(before=self.work_area, fill="x", side="top")
        self.entry_find.focus_set()
        # Pre-fill with selection if any
        try:
            sel = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if sel and "\n" not in sel:
                self.entry_find.delete(0, tk.END)
                self.entry_find.insert(0, sel)
                self.find_all_matches()
        except tk.TclError:
            pass

    def hide_find_bar(self):
        self.find_bar.pack_forget()
        self.clear_find_highlights()
        self.text.focus_set()

    def on_find_key_release(self, event):
        """Real-time match highlighting as user types."""
        if event.keysym in ("Return", "Shift_L", "Shift_R", "Escape"):
            return
        self.find_all_matches()

    def clear_find_highlights(self):
        self.text.tag_remove("search_highlight", "1.0", tk.END)
        self.text.tag_remove("search_current", "1.0", tk.END)
        self.search_matches = []
        self.current_match_index = -1
        self.lbl_match_count.config(text="0 matches")

    def find_all_matches(self):
        """Find and highlight all occurrences of query."""
        self.clear_find_highlights()
        query = self.entry_find.get()
        if not query:
            return

        start = "1.0"
        while True:
            pos = self.text.search(query, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(query)}c"
            self.search_matches.append((pos, end))
            self.text.tag_add("search_highlight", pos, end)
            start = end

        count = len(self.search_matches)
        if count > 0:
            self.current_match_index = 0
            self._highlight_active_match()
            self.lbl_match_count.config(text=f"1 of {count}")
        else:
            self.lbl_match_count.config(text="No match")

    def _highlight_active_match(self):
        """Highlight current active match in distinct accent color."""
        if not self.search_matches or self.current_match_index < 0:
            return
        self.text.tag_remove("search_current", "1.0", tk.END)
        pos, end = self.search_matches[self.current_match_index]
        self.text.tag_add("search_current", pos, end)
        self.text.see(pos)
        self.lbl_match_count.config(
            text=f"{self.current_match_index + 1} of {len(self.search_matches)}"
        )

    def find_next(self):
        if not self.search_matches:
            self.find_all_matches()
            return
        self.current_match_index = (self.current_match_index + 1) % len(
            self.search_matches
        )
        self._highlight_active_match()

    def find_prev(self):
        if not self.search_matches:
            self.find_all_matches()
            return
        self.current_match_index = (self.current_match_index - 1) % len(
            self.search_matches
        )
        self._highlight_active_match()

    def replace_current(self):
        if not self.search_matches or self.current_match_index < 0:
            return
        replacement = self.entry_replace.get()
        pos, end = self.search_matches[self.current_match_index]

        self.text.delete(pos, end)
        self.text.insert(pos, replacement)
        # Refresh matches
        self.find_all_matches()

    def replace_all(self):
        query = self.entry_find.get()
        replacement = self.entry_replace.get()
        if not query:
            return

        content = self.text.get("1.0", "end-1c")
        new_content, count = re.subn(re.escape(query), replacement, content, flags=re.IGNORECASE)

        if count > 0:
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", new_content)
            self.find_all_matches()
            self.lbl_match_count.config(text=f"Replaced {count}")
        else:
            self.lbl_match_count.config(text="No match")

    # ==========================================
    # FILE OPERATIONS
    # ==========================================
    def prompt_save_if_modified(self):
        """Ask user if they want to save changes before discarding."""
        if not self.is_modified:
            return True

        filename = (
            os.path.basename(self.current_filepath)
            if self.current_filepath
            else "Untitled"
        )
        choice = messagebox.askyesnocancel(
            "Save Changes?",
            f"Do you want to save changes to '{filename}' before proceeding?",
        )

        if choice is True:
            return self.save_file()
        elif choice is False:
            return True
        else:
            return False

    def new_file(self):
        if not self.prompt_save_if_modified():
            return

        self.text.delete("1.0", tk.END)
        self.current_filepath = None
        self.is_modified = False
        self.text.edit_modified(False)
        self._update_title()
        self._update_line_numbers()
        self._update_stats()

    def open_file(self):
        if not self.prompt_save_if_modified():
            return

        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("Markdown", "*.md"),
                ("Python Files", "*.py"),
                ("HTML/CSS/JS", "*.html;*.css;*.js"),
                ("JSON/YAML", "*.json;*.yaml;*.yml"),
                ("All Files", "*.*"),
            ]
        )

        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, content)
                self.current_filepath = filepath
                self.is_modified = False
                self.text.edit_modified(False)
                self._update_title()
                self._update_line_numbers()
                self._update_stats()

            except (OSError, UnicodeDecodeError) as err:
                messagebox.showerror("Open Error", f"Could not open file:\n{err}")

    def save_file(self):
        if not self.current_filepath:
            return self.save_file_as()
        else:
            return self._write_file(self.current_filepath)

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Markdown", "*.md"),
                ("Python Files", "*.py"),
                ("All Files", "*.*"),
            ],
        )

        if filepath:
            return self._write_file(filepath)
        return False

    def _write_file(self, filepath):
        try:
            content = self.text.get("1.0", "end-1c")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            self.current_filepath = filepath
            self.is_modified = False
            self.text.edit_modified(False)
            self._update_title()
            return True
        except OSError as err:
            messagebox.showerror("Save Error", f"Could not save file:\n{err}")
            return False

    def on_close_window(self):
        """Safely intercept window close button."""
        if self.prompt_save_if_modified():
            self.destroy()


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================
def main():
    app = SmartTextEditor()
    app.mainloop()


if __name__ == "__main__":
    main()
