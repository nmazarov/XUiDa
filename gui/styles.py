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
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
}}

QWidget {{
    background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
    font-size: 13px;
}}

QMenuBar {{
    background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
    border-bottom: 1px solid {BORDER_COLOR};
    padding: 3px 6px;
    font-size: 13px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 5px 12px;
    border-radius: 6px;
    color: {TEXT_PRIMARY};
}}

QMenuBar::item:selected {{
    background-color: {CARD_BG};
    color: {ACCENT_BLUE};
}}

QMenu {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 6px;
}}

QMenu::item {{
    padding: 6px 28px 6px 12px;
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
    background-color: {BG_COLOR};
    border-bottom: 1px solid {BORDER_COLOR};
    spacing: 6px;
    padding: 5px 10px;
}}

QToolButton {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 500;
}}

QToolButton:hover {{
    background-color: #212c3e;
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
    padding: 6px;
    outline: none;
}}

QTreeWidget::item {{
    padding: 6px 4px;
    border-radius: 4px;
    margin: 1px 0;
    color: {TEXT_PRIMARY};
    background-color: {BG_COLOR};
}}

QTreeWidget::item:hover {{
    background-color: #1a2536;
    color: #00d2ff;
}}

QTreeWidget::item:selected {{
    background-color: {SELECTION_COLOR};
    color: #ffffff;
}}

/* UNIFIED TABLE STYLES - ZERO WHITE STRIPES */
QTableWidget, QTableView {{
    background-color: {BG_COLOR};
    alternate-background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    gridline-color: {BORDER_COLOR};
    selection-background-color: {SELECTION_COLOR};
    selection-color: #ffffff;
    outline: none;
}}

QTableWidget::item, QTableView::item {{
    background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
    padding: 6px 10px;
    border: none;
}}

QTableWidget::item:alternate, QTableView::item:alternate {{
    background-color: {BG_COLOR};
    color: {TEXT_PRIMARY};
}}

QTableWidget::item:hover, QTableView::item:hover {{
    background-color: #1a2332;
    color: #ffffff;
}}

QTableWidget::item:selected, QTableView::item:selected {{
    background-color: {SELECTION_COLOR};
    color: #ffffff;
}}

QHeaderView::section {{
    background-color: {CARD_BG};
    color: {ACCENT_BLUE};
    font-weight: bold;
    padding: 8px 12px;
    border: none;
    border-right: 1px solid {BORDER_COLOR};
    border-bottom: 1px solid {BORDER_COLOR};
    font-size: 12px;
}}

QLineEdit {{
    background-color: {CARD_BG};
    color: #ffffff;
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 6px 12px;
    selection-background-color: {SELECTION_COLOR};
}}

QLineEdit:focus {{
    border-color: {ACCENT_BLUE};
    background-color: {BG_COLOR};
}}

QPushButton {{
    background-color: #238636;
    color: #ffffff;
    font-weight: 600;
    border: 1px solid rgba(240, 246, 252, 0.1);
    border-radius: 6px;
    padding: 6px 14px;
}}

QPushButton:hover {{
    background-color: #2ea043;
}}

QPushButton:pressed {{
    background-color: #238636;
}}

QPushButton#secondaryBtn {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
}}

QPushButton#secondaryBtn:hover {{
    background-color: #222d3e;
    border-color: {ACCENT_BLUE};
    color: #ffffff;
}}

QPushButton#secondaryBtn:checked {{
    background-color: {SELECTION_COLOR};
    border-color: {ACCENT_BLUE};
    color: #ffffff;
}}

QPushButton#dangerBtn {{
    background-color: #da3633;
    color: #ffffff;
    border: 1px solid rgba(240, 246, 252, 0.1);
}}

QPushButton#dangerBtn:hover {{
    background-color: #f85149;
}}

QComboBox {{
    background-color: {CARD_BG};
    color: #ffffff;
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 5px 12px;
    min-width: 160px;
}}

QComboBox:hover {{
    border-color: {ACCENT_BLUE};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    selection-background-color: {SELECTION_COLOR};
    selection-color: #ffffff;
    padding: 4px;
}}

QProgressBar {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    font-size: 11px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #00d2ff);
    border-radius: 5px;
}}

QStatusBar {{
    background-color: {BG_COLOR};
    color: {TEXT_SECONDARY};
    border-top: 1px solid {BORDER_COLOR};
    padding: 3px 10px;
    font-size: 12px;
}}

QScrollBar:vertical {{
    background: {BG_COLOR};
    width: 8px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {BORDER_COLOR};
    min-height: 25px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical:hover {{
    background: #00d2ff;
}}

QScrollBar:horizontal {{
    background: {BG_COLOR};
    height: 8px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: {BORDER_COLOR};
    min-width: 25px;
    border-radius: 4px;
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
