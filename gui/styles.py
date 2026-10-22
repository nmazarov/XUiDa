"""
XUiDa64 - Modern UI Themes & QSS Stylesheets
Supports Dark Cyber Edition and Classic AIDA64 Edition with high-DPI polish.
"""

DARK_THEME = """
QMainWindow, QDialog {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
}

QWidget {
    background-color: #0d1117;
    color: #c9d1d9;
    font-size: 13px;
}

QMenuBar {
    background-color: #161b22;
    color: #c9d1d9;
    border-bottom: 1px solid #30363d;
    padding: 3px 6px;
    font-size: 13px;
}

QMenuBar::item {
    background: transparent;
    padding: 5px 12px;
    border-radius: 6px;
}

QMenuBar::item:selected {
    background-color: #21262d;
    color: #58a6ff;
}

QMenu {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px;
}

QMenu::item {
    padding: 6px 28px 6px 12px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #1f6feb;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background: #30363d;
    margin: 4px 6px;
}

QToolBar {
    background-color: #161b22;
    border-bottom: 1px solid #30363d;
    spacing: 6px;
    padding: 5px 10px;
}

QToolButton {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
}

QToolButton:hover {
    background-color: #30363d;
    border-color: #58a6ff;
    color: #ffffff;
}

QToolButton:pressed {
    background-color: #1f6feb;
    color: #ffffff;
}

QSplitter::handle {
    background-color: #30363d;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #58a6ff;
}

QTreeWidget {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px 4px;
    border-radius: 4px;
    margin: 1px 0;
}

QTreeWidget::item:hover {
    background-color: #21262d;
    color: #58a6ff;
}

QTreeWidget::item:selected {
    background-color: #1f6feb;
    color: #ffffff;
}

QTableWidget, QTableView {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    gridline-color: #21262d;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    outline: none;
}

QHeaderView::section {
    background-color: #21262d;
    color: #8b949e;
    font-weight: 600;
    padding: 8px 12px;
    border: none;
    border-right: 1px solid #30363d;
    border-bottom: 1px solid #30363d;
    font-size: 12px;
}

QLineEdit {
    background-color: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 12px;
    selection-background-color: #1f6feb;
}

QLineEdit:focus {
    border-color: #58a6ff;
    background-color: #161b22;
}

QPushButton {
    background-color: #238636;
    color: #ffffff;
    font-weight: 600;
    border: 1px solid rgba(240, 246, 252, 0.1);
    border-radius: 6px;
    padding: 6px 14px;
}

QPushButton:hover {
    background-color: #2ea043;
}

QPushButton:pressed {
    background-color: #238636;
}

QPushButton#secondaryBtn {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
}

QPushButton#secondaryBtn:hover {
    background-color: #30363d;
    border-color: #58a6ff;
    color: #ffffff;
}

QPushButton#dangerBtn {
    background-color: #da3633;
    color: #ffffff;
    border: 1px solid rgba(240, 246, 252, 0.1);
}

QPushButton#dangerBtn:hover {
    background-color: #f85149;
}

QComboBox {
    background-color: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 5px 12px;
    min-width: 160px;
}

QComboBox:hover {
    border-color: #58a6ff;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    padding: 4px;
}

QProgressBar {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 6px;
    text-align: center;
    color: #f0f6fc;
    font-weight: bold;
    font-size: 11px;
}

QProgressBar::chunk {
    background-color: #238636;
    border-radius: 5px;
}

QStatusBar {
    background-color: #161b22;
    color: #8b949e;
    border-top: 1px solid #30363d;
    padding: 2px 8px;
    font-size: 12px;
}

QScrollBar:vertical {
    background: #161b22;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #30363d;
    min-height: 25px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #58a6ff;
}

QScrollBar:horizontal {
    background: #161b22;
    height: 10px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #30363d;
    min-width: 25px;
    border-radius: 5px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    width: 0;
    height: 0;
}
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
