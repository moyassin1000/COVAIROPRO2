# Convairo Pro

برنامج Windows Desktop احترافي لتحويل الملفات بين صيغ متعددة، مبني بلغة Python وواجهة PySide6، مع SQLite، نظام مستخدمين، اشتراك Mock، ولوحة Admin.

## المميزات

- واجهة عربية وإنجليزية.
- دعم RTL عند اختيار العربية.
- Splash Screen.
- تسجيل دخول وإنشاء حساب.
- أول مستخدم في قاعدة بيانات جديدة يصبح Admin تلقائيًا.
- كلمات المرور محفوظة باستخدام bcrypt وليست نصًا عاديًا.
- سجل تحويلات خاص بكل مستخدم.
- حالات المستخدم: Free / Premium / Admin.
- اشتراك Mock قابل للربط لاحقًا ببوابة دفع.
- لوحة Admin لإدارة المستخدمين، الصلاحيات، التفعيل، وسجل العمليات.
- تحويلات في Background Thread لمنع تجميد الواجهة.
- فحص وجود FFmpeg و LibreOffice وإظهار رسائل واضحة عند نقص الأدوات.

## التشغيل على Windows

```bat
cd convairo_pro
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## الأدوات الخارجية المطلوبة

### FFmpeg

مطلوب لتحويل الفيديو والصوت. يجب تثبيته وإضافة مجلد `bin` إلى PATH.

### LibreOffice

مطلوب لتحويل المستندات إلى PDF. يجب تثبيته وإضافة مسار `soffice.exe` إلى PATH.

### Poppler اختياري

مطلوب فقط لتحويل PDF إلى صور عند استخدام `pdf2image`.

## بناء ملف EXE

```bat
scripts\build_exe.bat
```

سيتم إنشاء النسخة داخل:

```text
dist\Convairo Pro\
```

## رفع المشروع على GitHub

```bat
git init
git add .
git commit -m "Initial Convairo Pro project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/convairo-pro.git
git push -u origin main
```

## ملفات لا يجب رفعها

- `app_data.sqlite3`
- ملفات `logs/`
- ملفات `output/`
- `.env`
- أي مفاتيح API أو كلمات مرور

تم ضبط `.gitignore` لتجاهل هذه الملفات.
