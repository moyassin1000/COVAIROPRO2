# Convairo Pro

Convairo Pro is a professional Windows desktop application for converting files between common formats. It is designed with a modular architecture so the UI, authentication, database, subscriptions, admin panel, and conversion engines are separated and easy to extend.

## Main features

- Windows desktop app built with Python and PySide6.
- Arabic and English interface.
- RTL support for Arabic.
- Splash screen, login screen, registration screen, dashboard, settings, subscription page, history page, and Admin panel.
- SQLite local database.
- Secure password hashing with bcrypt.
- Per-user conversion history.
- User roles: Free, Premium, Admin.
- Mock subscription system ready for payment integration.
- Admin-only panel for managing users, roles, active status, and conversion logs.
- Background conversion thread so the UI does not freeze.
- External dependency checks for FFmpeg and LibreOffice.
- Organized output and logging folders.

## Supported conversion categories

### Documents

- `docx`, `doc`, `odt`, `txt` to `pdf` using LibreOffice Headless.

### PDF

- `pdf` to `png` or `jpg` using `pdf2image`.
- On Windows, PDF-to-image also requires Poppler installed and available in PATH.

### Images

- `jpg`, `png`, `webp`, `bmp`, `tiff`, `ico` using Pillow.

### Videos

- `mp4`, `mkv`, `avi`, `mov`, `webm` using FFmpeg.

### Audio

- `mp3`, `wav`, `aac`, `m4a`, `ogg`, `flac` using FFmpeg.

## Project structure

```text
convairo_pro/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── app_config.example.json
├── scripts/
│   └── build_exe.bat
├── app/
│   ├── core/
│   ├── database/
│   ├── services/
│   ├── converters/
│   ├── ui/
│   ├── auth/
│   ├── admin/
│   ├── subscriptions/
│   ├── translations/
│   └── utils/
├── assets/
│   ├── icons/
│   ├── images/
│   └── fonts/
├── output/
├── logs/
└── tests/
```

## Windows setup

### 1. Install Python

Install Python 3.11 or newer and enable **Add Python to PATH** during installation.

### 2. Create virtual environment

```bat
cd convairo_pro
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install external converters

#### FFmpeg

Install FFmpeg and add its `bin` folder to Windows PATH.

Required for video and audio conversion.

#### LibreOffice

Install LibreOffice and add the folder that contains `soffice.exe` to Windows PATH.

Required for document-to-PDF conversion.

#### Poppler optional

Install Poppler for Windows and add its `bin` folder to PATH.

Required only for PDF-to-image conversion.

## Run the app

```bat
python main.py
```

The first user created in a fresh database automatically becomes `Admin`. Every user after that is created as `Free` by default.

You can also create an admin during first launch with environment variables:

```bat
set CONVAIRO_ADMIN_NAME=Administrator
set CONVAIRO_ADMIN_EMAIL=admin@example.com
set CONVAIRO_ADMIN_PASSWORD=ChangeMe123!
python main.py
```

No default password is stored in the source code.

## Build EXE

Use the included script:

```bat
scripts\build_exe.bat
```

The generated application will be placed inside:

```text
dist\Convairo Pro\
```

Manual PyInstaller command:

```bat
pyinstaller --noconfirm --windowed --name "Convairo Pro" --add-data "app\translations;app\translations" --add-data "assets;assets" main.py
```

## GitHub upload steps

```bat
git init
git add .
git commit -m "Initial Convairo Pro project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/convairo-pro.git
git push -u origin main
```

Do not commit runtime files such as:

- `app_data.sqlite3`
- `logs/`
- `output/`
- `.env`
- API keys
- private certificates

The `.gitignore` file already excludes these files.

## Notes for future development

Recommended next upgrades:

1. Add real payment provider integration in `app/subscriptions/service.py`.
2. Add precise FFmpeg progress parsing.
3. Add drag-and-drop file selection.
4. Add preview pages for images and PDFs.
5. Add update checker.
6. Add installer generation with Inno Setup or NSIS.
7. Add more tests around authentication, roles, and conversion validation.
