"""
XUiDa64 - Modern UI Themes & QSS Stylesheets
Crafted in accordance with Benji Taylor / Stageshow Design Engineering principles:
- Restraint: clean surface hierarchy, 5 distinct tonal inks, 1 primary accent.
- Depth through surface elevation (dark obsidian #0b0e14 -> #121722 -> #161c28 -> #1e2637).
- Ultra-refined 1px hairline borders without redundant tonal boxes.
- Crisp typography (Segoe UI Variable Text) with high-contrast readable labels.
- Balanced 8-12px gutters and consistent 8-10px border radii.
"""

# Base canvas & surface hierarchy tokens
BG_COLOR = "#0b0e14"       # Deep canvas
BG_SURFACE = "#10141d"     # Sidebar & header bars
CARD_BG = "#151b26"        # Interactive cards & panels
CARD_BG_HOVER = "#1c2433"  # Hovered elevation
BORDER_COLOR = "#222c3d"   # Hairline subtle border
BORDER_FOCUS = "#38bdf8"   # Electric cyan focus ring

# Text & ink tokens
TEXT_PRIMARY = "#f8fafc"   # High contrast crisp white
TEXT_SECONDARY = "#94a3b8" # Soft legible slate
TEXT_MUTED = "#64748b"     # Subtle metadata captions

# Semantic accent tokens
ACCENT_BLUE = "#38bdf8"    # Primary electric cyan
ACCENT_GREEN = "#10b981"   # Health, success, optimal
ACCENT_AMBER = "#f59e0b"   # Warning, medium load
ACCENT_RED = "#ef4444"     # Danger, purge, thermal alert
ACCENT_PURPLE = "#a855f7"  # System, telemetry
SELECTION_COLOR = "#2563eb" # Focused active pill

from PyQt5.QtGui import QPalette, QColor

def apply_dark_palette(app):
    """Configures native Windows application palette to deep obsidian colors, preventing white flashes."""
    pal = app.palette()
    pal.setColor(QPalette.Window, QColor(BG_COLOR))
    pal.setColor(QPalette.WindowText, QColor(TEXT_PRIMARY))
    pal.setColor(QPalette.Base, QColor(BG_SURFACE))
    pal.setColor(QPalette.AlternateBase, QColor(BG_SURFACE))
    pal.setColor(QPalette.ToolTipBase, QColor(BG_SURFACE))
    pal.setColor(QPalette.ToolTipText, QColor(TEXT_PRIMARY))
    pal.setColor(QPalette.Text, QColor(TEXT_PRIMARY))
    pal.setColor(QPalette.Button, QColor(CARD_BG))
    pal.setColor(QPalette.ButtonText, QColor(TEXT_PRIMARY))
    pal.setColor(QPalette.BrightText, QColor("#ffffff"))
    pal.setColor(QPalette.Highlight, QColor(SELECTION_COLOR))
    pal.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)

DARK_THEME = f"""
QMainWindow, QDialog {{
    background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI Variable Text", "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
}}

QWidget {{
    background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI Variable Text", "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    font-size: 12px;
}}

/* Top Menu Bar */
QMenuBar {{
    background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    border-bottom: 1px solid {BORDER_COLOR};
    padding: 3px 8px;
    font-size: 12px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 6px 12px;
    border-radius: 6px;
    color: {TEXT_SECONDARY};
}}

QMenuBar::item:selected {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
}}

QMenu {{
    background-color: #131924;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 6px;
}}

QMenu::item {{
    padding: 6px 28px 6px 12px;
    border-radius: 5px;
    color: {TEXT_PRIMARY};
}}

QMenu::item:selected {{
    background-color: {SELECTION_COLOR};
    color: #ffffff;
}}

QMenu::separator {{
    height: 1px;
    background: {BORDER_COLOR};
    margin: 4px 6px;
}}

/* Toolbar - Sleek elevated glass ribbon */
QToolBar {{
    background-color: {BG_SURFACE};
    border-bottom: 1px solid {BORDER_COLOR};
    spacing: 6px;
    padding: 6px 10px;
}}

QToolButton {{
    background-color: {CARD_BG};
    color: #e2e8f0;
    border: 1px solid {BORDER_COLOR};
    border-radius: 7px;
    padding: 6px 13px;
    font-size: 11px;
    font-weight: 600;
}}

QToolButton:hover {{
    background-color: {CARD_BG_HOVER};
    border: 1px solid {ACCENT_BLUE};
    color: #ffffff;
}}

QToolButton:pressed {{
    background-color: {SELECTION_COLOR};
    border: 1px solid {ACCENT_BLUE};
    color: #ffffff;
}}

/* Splitter */
QSplitter::handle {{
    background-color: {BORDER_COLOR};
    width: 2px;
}}

QSplitter::handle:hover {{
    background-color: {ACCENT_BLUE};
}}

/* Sidebar Tree Navigation */
QTreeWidget {{
    background-color: {BG_SURFACE};
    alternate-background-color: {BG_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 6px 4px;
    outline: none;
}}

QTreeWidget::item {{
    padding: 6px 8px;
    border-radius: 6px;
    margin: 2px 3px;
    color: {TEXT_SECONDARY};
    background-color: {BG_SURFACE};
}}

QTreeWidget::item:hover {{
    background-color: #17202e;
    color: {ACCENT_BLUE};
}}

QTreeWidget::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1d4ed8, stop:1 #2563eb);
    color: #ffffff;
    font-weight: 600;
}}

/* Table Views - Clean, High Contrast, Zero White Stripes */
QTableWidget {{
    background-color: {BG_COLOR};
    alternate-background-color: {BG_COLOR};
    color: #f1f5f9;
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    gridline-color: #17202d;
    selection-background-color: {SELECTION_COLOR};
    selection-color: #ffffff;
    outline: none;
}}

QTableWidget::item {{
    background-color: {BG_COLOR};
    color: #f1f5f9;
    padding: 7px 12px;
    border: none;
    font-size: 12px;
}}

QTableWidget::item:alternate {{
    background-color: {BG_COLOR};
    color: #f1f5f9;
}}

QTableWidget::item:hover {{
    background-color: #151e2c;
    color: {ACCENT_BLUE};
}}

QTableWidget::item:selected {{
    background-color: {SELECTION_COLOR};
    color: #ffffff;
}}

QHeaderView::section {{
    background-color: #121824;
    color: {ACCENT_BLUE};
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.5px;
    padding: 8px 12px;
    border: none;
    border-right: 1px solid {BORDER_COLOR};
    border-bottom: 1px solid {BORDER_COLOR};
}}

/* Line Edits & Text Inputs */
QLineEdit, QTextEdit {{
    background-color: {CARD_BG};
    color: #ffffff;
    border: 1px solid {BORDER_COLOR};
    border-radius: 7px;
    padding: 6px 11px;
    font-size: 12px;
    selection-background-color: {SELECTION_COLOR};
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 1px solid {ACCENT_BLUE};
    background-color: #111722;
}}

/* Push Buttons */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669);
    color: #ffffff;
    font-weight: 600;
    font-size: 12px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 7px;
    padding: 6px 16px;
}}

QPushButton:hover {{
    background: #059669;
    border-color: #34d399;
}}

QPushButton:pressed {{
    background-color: #047857;
}}

QPushButton#secondaryBtn {{
    background: {CARD_BG};
    color: #e2e8f0;
    border: 1px solid {BORDER_COLOR};
    font-weight: 500;
}}

QPushButton#secondaryBtn:hover {{
    background-color: {CARD_BG_HOVER};
    border-color: {ACCENT_BLUE};
    color: #ffffff;
}}

QPushButton#secondaryBtn:checked {{
    background-color: {SELECTION_COLOR};
    border-color: {ACCENT_BLUE};
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#dangerBtn {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ef4444, stop:1 #dc2626);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 7px;
    padding: 6px 16px;
    font-weight: 600;
}}

QPushButton#dangerBtn:hover {{
    background-color: #f87171;
    border-color: #fca5a5;
}}

/* Combo Box */
QComboBox {{
    background-color: {CARD_BG};
    color: #ffffff;
    border: 1px solid {BORDER_COLOR};
    border-radius: 7px;
    padding: 6px 12px;
    font-size: 12px;
    min-width: 150px;
}}

QComboBox:hover {{
    border-color: {ACCENT_BLUE};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: #131924;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    selection-background-color: {SELECTION_COLOR};
    selection-color: #ffffff;
    padding: 4px;
}}

/* Progress Bar */
QProgressBar {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    font-size: 10px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #00d2ff);
    border-radius: 5px;
}}

/* Status Bar */
QStatusBar {{
    background-color: {BG_SURFACE};
    color: {TEXT_SECONDARY};
    border-top: 1px solid {BORDER_COLOR};
    padding: 4px 10px;
    font-size: 11px;
}}

/* Scrollbar - Ultra clean 6px pill design */
QScrollBar:vertical {{
    background: {BG_COLOR};
    width: 6px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {BORDER_COLOR};
    min-height: 28px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background: {ACCENT_BLUE};
}}

QScrollBar:horizontal {{
    background: {BG_COLOR};
    height: 6px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: {BORDER_COLOR};
    min-width: 28px;
    border-radius: 3px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {ACCENT_BLUE};
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    width: 0;
    height: 0;
}}

/* CheckBoxes */
QCheckBox {{
    color: {TEXT_PRIMARY};
    spacing: 8px;
    font-size: 12px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid {BORDER_COLOR};
    background-color: {CARD_BG};
}}

QCheckBox::indicator:hover {{
    border-color: {ACCENT_BLUE};
}}

QCheckBox::indicator:checked {{
    background-color: {ACCENT_BLUE};
    border-color: {ACCENT_BLUE};
    image: none;
}}
"""

CLASSIC_THEME = """
QMainWindow, QDialog {
    background-color: #f6f8fa;
    color: #1f2328;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
}

QWidget {
    background-color: #ffffff;
    color: #1f2328;
    font-size: 13px;
}

QMenuBar {
    background-color: #f6f8fa;
    color: #1f2328;
    border-bottom: 1px solid #d0d7de;
    padding: 2px 4px;
}

QMenuBar::item:selected {
    background-color: #0969da;
    color: #ffffff;
    border-radius: 4px;
}

QMenu {
    background-color: #ffffff;
    color: #1f2328;
    border: 1px solid #d0d7de;
    padding: 4px;
}

QMenu::item:selected {
    background-color: #0969da;
    color: #ffffff;
}

QToolBar {
    background-color: #f6f8fa;
    border-bottom: 1px solid #d0d7de;
    spacing: 6px;
    padding: 4px 8px;
}

QToolButton {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 5px;
    padding: 5px 12px;
    color: #1f2328;
}

QToolButton:hover {
    background-color: #eaeef2;
    border-color: #0969da;
}

QTreeWidget {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 4px;
}

QTreeWidget::item:selected {
    background-color: #0969da;
    color: #ffffff;
}

QTableWidget, QTableView {
    background-color: #ffffff;
    alternate-background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    gridline-color: #eaeef2;
    selection-background-color: #0969da;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #f6f8fa;
    color: #656d76;
    font-weight: 600;
    padding: 6px 10px;
    border: 1px solid #d0d7de;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 5px 10px;
}

QPushButton {
    background-color: #1f883d;
    color: #ffffff;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1a7f37;
}

QPushButton#secondaryBtn {
    background-color: #f6f8fa;
    color: #24292f;
    border: 1px solid #d0d7de;
}

QPushButton#secondaryBtn:hover {
    background-color: #eaeef2;
}

QPushButton#dangerBtn {
    background-color: #cf222e;
    color: #ffffff;
}
"""
