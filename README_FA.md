# 📚 Story Development Toolkit

[![Tests](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/miladrezanezhad/story-toolkit/releases)
[![Author](https://img.shields.io/badge/Author-Milad%20Rezanezhad-purple.svg)](https://github.com/miladrezanezhad)

**A comprehensive Python toolkit for generating engaging and coherent stories.**

**ابزار جامع پایتون برای تولید داستان‌های جذاب و منسجم**

Story Development Toolkit ابزارهایی برای ایجاد شخصیت، تولید پیرنگ، نوشتن دیالوگ، جهان‌سازی و بررسی انسجام داستان فراهم می‌کند — همه در یک پکیج.

---

## ✨ ویژگی‌ها

| ویژگی | توضیح |
|---------|-------------|
| 🎭 **ایجاد شخصیت** | ساخت شخصیت‌های پیچیده با ویژگی‌ها، اهداف، مهارت‌ها، ترس‌ها و روابط |
| 📚 **تولید پیرنگ** | تولید ساختار داستان برای فانتزی، معمایی، عاشقانه، ماجراجویی، علمی-تخیلی |
| 💬 **نوشتن دیالوگ** | ایجاد دیالوگ‌های طبیعی با قالب‌های آماده |
| 🌍 **جهان‌سازی** | طراحی جهان‌های داستانی با مکان‌ها، فرهنگ‌ها، قوانین و گروه‌ها |
| 🔍 **بررسی انسجام** | شناسایی حفره‌های داستانی، ناسازگاری شخصیت‌ها، مشکلات زمانی |
| 📊 **تحلیل متن** | تحلیل خوانایی، ریتم، تعادل دیالوگ و غنای واژگان |

---

## 📦 نصب

```bash
# کلون کردن مخزن
git clone https://github.com/miladrezanezhad/story-toolkit.git
cd story-toolkit

# نصب وابستگی‌ها
pip install -r requirements.txt

# یا نصب به صورت پکیج قابل ویرایش
pip install -e .
```

---

## 🚀 شروع سریع

```python
from story_toolkit import StoryToolkit

# ایجاد نمونه
toolkit = StoryToolkit()

# ساخت داستان
story = toolkit.create_story(genre="fantasy", theme="courage")

# افزودن قهرمان
hero = toolkit.add_character_to_story(story, "کای", "protagonist")
hero.add_trait("brave")
hero.add_goal("Save the kingdom")

# تولید دیالوگ
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "کای", "Villain", context="conflict"
)
for line in dialogue:
    print(line)

# بررسی انسجام
report = toolkit.check_story_coherence(story)
print(f"امتیاز انسجام: {report['overall_score']:.0%}")
```

**خروجی:**
```
کای: نمی‌تونم باور کنم این کار رو کردی!
Villain: چاره‌ای برام نذاشتی.
کای: همیشه یه راه هست. تو فقط اشتباه انتخاب کردی.
امتیاز انسجام: 100%
```

---

## 📁 ساختار پروژه

```
story_toolkit/
├── story_toolkit/          # پکیج اصلی پایتون
│   ├── core/               # موتور داستان، شخصیت، پیرنگ، جهان‌ساز
│   ├── generators/         # تولیدکننده شخصیت، پیرنگ و دیالوگ
│   ├── nlp/                # بررسی انسجام و تحلیل متن
│   └── utils/              # توابع کمکی
├── docs/                   # مستندات (انگلیسی و فارسی)
│   ├── eng/                # مستندات انگلیسی
│   └── fa-ir/              # مستندات فارسی
├── examples/               # مثال‌های استفاده
├── tests/                  # تست‌های واحد
├── requirements.txt        # وابستگی‌ها
└── setup.py                # نصب پکیج
```

---

## 📖 مستندات

مستندات کامل به دو زبان در دسترس است:

| زبان | لینک |
|----------|------|
| 🇬🇧 English | [docs/eng/index.html](docs/eng/index.html) |
| 🇮🇷 فارسی | [docs/fa-ir/index.html](docs/fa-ir/index.html) |

یا صفحه انتخاب زبان را باز کنید:

```bash
start docs/index.html
```

---

## 🧪 اجرای تست‌ها

```bash
# تست ماژول‌های اصلی
python -m tests.test_core

# تست تولیدکننده‌ها
python -m tests.test_generators

# تست ابزارهای NLP
python -m tests.test_nlp
```

---

## 👤 نویسنده

**میلاد رضانژاد**

- گیت‌هاب: [https://github.com/miladrezanezhad](https://github.com/miladrezanezhad)
- پروژه: [https://github.com/miladrezanezhad/story-toolkit](https://github.com/miladrezanezhad/story-toolkit)

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است — فایل [LICENSE](LICENSE) را ببینید.

---

## 🌟 حمایت

اگر این پروژه برایتان مفید بود، لطفاً در گیت‌هاب به آن ⭐️ بدهید!

---
