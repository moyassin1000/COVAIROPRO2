"""Application QSS styles."""
from __future__ import annotations

APP_QSS = """
QWidget {
    font-family: Segoe UI, Arial, Tahoma;
    font-size: 13px;
    color: #1f2937;
}
QMainWindow, QWidget#Root {
    background: #f6f8fb;
}
QFrame#Card, QWidget#Card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
}
QLabel#Title {
    font-size: 24px;
    font-weight: 700;
    color: #111827;
}
QLabel#Subtitle {
    color: #6b7280;
}
QPushButton {
    border: 0;
    border-radius: 10px;
    padding: 10px 14px;
    background: #e5e7eb;
}
QPushButton:hover {
    background: #d1d5db;
}
QPushButton#PrimaryButton {
    color: #ffffff;
    background: #2563eb;
    font-weight: 600;
}
QPushButton#PrimaryButton:hover {
    background: #1d4ed8;
}
QPushButton#DangerButton {
    color: #ffffff;
    background: #dc2626;
    font-weight: 600;
}
QPushButton#SuccessButton {
    color: #ffffff;
    background: #059669;
    font-weight: 600;
}
QLineEdit, QComboBox, QTextEdit {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 9px;
    padding: 9px;
}
QTableWidget {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    gridline-color: #e5e7eb;
}
QHeaderView::section {
    background: #f3f4f6;
    padding: 8px;
    border: 0;
    font-weight: 600;
}
QProgressBar {
    border: 1px solid #d1d5db;
    border-radius: 9px;
    background: #ffffff;
    text-align: center;
    min-height: 20px;
}
QProgressBar::chunk {
    background: #2563eb;
    border-radius: 8px;
}
QListWidget {
    border: 0;
    background: #111827;
    color: #d1d5db;
    padding: 8px;
}
QListWidget::item {
    padding: 12px;
    border-radius: 10px;
}
QListWidget::item:selected {
    background: #2563eb;
    color: white;
}
"""
