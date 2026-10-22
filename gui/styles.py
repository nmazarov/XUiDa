"""
XUiDa64 - Modern UI Themes & QSS Stylesheets
Features a unified, high-contrast dark background (#141a24) across the entire interface.
Eliminates jarring white stripes and guarantees high text readability.
"""

# Unified dark background color for entire application
BG_COLOR = "#141a24"
BG_ALT = "#141a24"
CARD_BG = "#19212e"
BORDER_COLOR = "#2a364a"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#cbd5e1"
ACCENT_BLUE = "#58a6ff"
SELECTION_COLOR = "#1f6feb"

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

QMenuBar {{
    background-color: #121822;
    color: {TEXT_PRIMARY};
    border-bottom: 1px solid {BORDER_COLOR};
    padding: 3px 6px;
    font-size: 12px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 5px 12px;
    border-radius: 5px;
    color: {TEXT_PRIMARY};
}}

QMenuBar::item:selected {{
    background-color: {CARD_BG};
    color: {ACCENT_BLUE};
}}

QMenu {{
    background-color: #17202e;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 5px;
}}

QMenu::item {{
    padding: 6px 26px 6px 12px;
    border-radius: 4px;
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

QToolBar {{
    background-color: #121822;
    border-bottom: 1px solid {BORDER_COLOR};
    spacing: 5px;
    padding: 4px 8px;
}}

QToolButton {{
    background-color: {CARD_BG};
    color: #e2e8f0;
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 5px 11px;
    font-size: 11px;
    font-weight: 600;
}}

QToolButton:hover {{
    background-color: #202d42;
    border: 1px solid #00d2ff;
    color: #ffffff;
}}

QToolButton:pressed {{
    background-color: {SELECTION_COLOR};
    border: 1px solid #00d2ff;
    color: #ffffff;
}}

QSplitter::handle {{
    background-color: {BORDER_COLOR};
    width: 2px;
}}

QSplitter::handle:hover {{
    background-color: #00d2ff;
}}

QTreeWidget {{
    background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 5px 3px;
    outline: none;
}}

QTreeWidget::item {{
    padding: 5px 6px;
    border-radius: 4px;
    margin: 1px 2px;
    color: {TEXT_SECONDARY};
    background-color: {BG_COLOR};
}}

QTreeWidget::item:hover {{
    background-color: #192436;
    color: #00d2ff;
}}

QTreeWidget::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #0099ff);
    color: #ffffff;
    font-weight: 600;
}}

/* UNIFIED TABLE STYLES - ZERO WHITE STRIPES & CRISP VERTICAL ALIGNMENT */
QTableWidget, QTableView {{
    background-color: {BG_COLOR};
    alternate-background-color: {BG_COLOR};
    color: #f1f5f9;
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    gridline-color: #1e2838;
    selection-background-color: {SELECTION_COLOR};
    selection-color: #ffffff;
    outline: none;
}}

QTableWidget::item, QTableView::item {{
    background-color: {BG_COLOR};
    color: #f1f5f9;
    padding: 6px 10px;
    border: none;
    font-size: 12px;
}}

QTableWidget::item:alternate, QTableView::item:alternate {{
    background-color: {BG_COLOR};
    color: #f1f5f9;
}}

QTableWidget::item:hover, QTableView::item:hover {{
    background-color: #1c2738;
    color: #38bdf8;
}}

QTableWidget::item:selected, QTableView::item:selected {{
    background-color: {SELECTION_COLOR};
    color: #ffffff;
}}

QHeaderView::section {{
    background-color: #17202d;
    color: {ACCENT_BLUE};
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.3px;
    padding: 7px 10px;
    border: none;
    border-right: 1px solid {BORDER_COLOR};
    border-bottom: 1px solid {BORDER_COLOR};
}}

QLineEdit {{
    background-color: {CARD_BG};
    color: #ffffff;
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    selection-background-color: {SELECTION_COLOR};
}}

QLineEdit:focus {{
    border-color: #00d2ff;
    background-color: #121822;
}}

QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #238636, stop:1 #1e7e34);
    color: #ffffff;
    font-weight: 600;
    font-size: 12px;
    border: 1px solid rgba(240, 246, 252, 0.15);
    border-radius: 6px;
    padding: 5px 14px;
}}

QPushButton:hover {{
    background: #2ea043;
    border-color: #3fb950;
}}

QPushButton:pressed {{
    background-color: #238636;
}}

QPushButton#secondaryBtn {{
    background: {CARD_BG};
    color: #e2e8f0;
    border: 1px solid {BORDER_COLOR};
    font-weight: 500;
}}

QPushButton#secondaryBtn:hover {{
    background-color: #202d40;
    border-color: #00d2ff;
    color: #ffffff;
}}

QPushButton#secondaryBtn:checked {{
    background-color: {SELECTION_COLOR};
    border-color: #00d2ff;
    color: #ffffff;
}}

QPushButton#dangerBtn {{
    background-color: #da3633;
    color: #ffffff;
    border: 1px solid rgba(240, 246, 252, 0.15);
}}

QPushButton#dangerBtn:hover {{
    background-color: #f85149;
}}

QComboBox {{
    background-color: {CARD_BG};
    color: #ffffff;
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    min-width: 140px;
}}

QComboBox:hover {{
    border-color: #00d2ff;
}}

QComboBox::drop-down {{
    border: none;
    width: 22px;
}}

QComboBox QAbstractItemView {{
    background-color: #17202e;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    selection-background-color: {SELECTION_COLOR};
    selection-color: #ffffff;
    padding: 4px;
}}

QProgressBar {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 5px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    font-size: 10px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #00d2ff);
    border-radius: 4px;
}}

QStatusBar {{
    background-color: #111620;
    color: #94a3b8;
    border-top: 1px solid {BORDER_COLOR};
    padding: 2px 8px;
    font-size: 11px;
}}

QScrollBar:vertical {{
    background: {BG_COLOR};
    width: 7px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {BORDER_COLOR};
    min-height: 25px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background: #00d2ff;
}}

QScrollBar:horizontal {{
    background: {BG_COLOR};
    height: 7px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: {BORDER_COLOR};
    min-width: 25px;
    border-radius: 3px;
}}

QScrollBar::handle:horizontal:hover {{
    background: #00d2ff;
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    width: 0;
    height: 0;
}}

QFrame#statusBanner {{
    border-radius: 6px;
    padding: 8px;
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
