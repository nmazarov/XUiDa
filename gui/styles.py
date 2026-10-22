"""
XUiDa64 - Modern UI Themes & QSS Stylesheets
Supports Dark Cyber Edition and Classic AIDA64 Edition.
"""

DARK_THEME = """
QMainWindow, QDialog {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: "Segoe UI", Arial, sans-serif;
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
    padding: 2px;
}

QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #21262d;
    color: #58a6ff;
}

QMenu {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    padding: 4px;
}

QMenu::item {
    padding: 6px 24px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #1f6feb;
    color: #ffffff;
}

QToolBar {
    background-color: #161b22;
    border-bottom: 1px solid #30363d;
    spacing: 6px;
    padding: 4px 8px;
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

QTreeWidget {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px;
}

QTreeWidget::item {
    padding: 5px;
    border-radius: 4px;
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
}

QHeaderView::section {
    background-color: #21262d;
    color: #8b949e;
    font-weight: 600;
    padding: 6px 10px;
    border: none;
    border-right: 1px solid #30363d;
    border-bottom: 1px solid #30363d;
}

QLineEdit {
    background-color: #21262d;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 10px;
}

QLineEdit:focus {
    border-color: #58a6ff;
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
    color: #ffffff;
}

QPushButton#dangerBtn {
    background-color: #da3633;
    color: #ffffff;
}

QPushButton#dangerBtn:hover {
    background-color: #f85149;
}

QProgressBar {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 6px;
    text-align: center;
    color: #f0f6fc;
    font-weight: bold;
}

QProgressBar::chunk {
    background-color: #238636;
    border-radius: 5px;
}

QStatusBar {
    background-color: #161b22;
    color: #8b949e;
    border-top: 1px solid #30363d;
}

QScrollBar:vertical {
    background: #161b22;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #30363d;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #58a6ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

CLASSIC_THEME = """
QMainWindow, QDialog {
    background-color: #f0f2f5;
    color: #1c1e21;
    font-family: "Segoe UI", Arial, sans-serif;
}

QWidget {
    background-color: #ffffff;
    color: #24292f;
    font-size: 13px;
}

QMenuBar {
    background-color: #f6f8fa;
    color: #24292f;
    border-bottom: 1px solid #d0d7de;
}

QMenuBar::item:selected {
    background-color: #0969da;
    color: #ffffff;
}

QToolBar {
    background-color: #f6f8fa;
    border-bottom: 1px solid #d0d7de;
    spacing: 6px;
    padding: 4px;
}

QToolButton {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    padding: 5px 10px;
}

QToolButton:hover {
    background-color: #eaeef2;
    border-color: #0969da;
}

QTreeWidget {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
}

QTreeWidget::item:selected {
    background-color: #0969da;
    color: #ffffff;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    gridline-color: #e1e4e8;
}

QHeaderView::section {
    background-color: #f6f8fa;
    color: #24292f;
    font-weight: 600;
    padding: 5px;
    border: 1px solid #d0d7de;
}

QPushButton {
    background-color: #1f883d;
    color: #ffffff;
    border-radius: 4px;
    padding: 6px 12px;
}
"""
