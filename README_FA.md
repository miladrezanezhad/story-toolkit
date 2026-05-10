# 📚 داستان‌ساز هوشمند | Story Toolkit

[![Tests](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml)
[![Security Tests](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/security.yml/badge.svg)](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/security.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.2.3-orange.svg)](https://github.com/miladrezanezhad/story-toolkit/releases)
[![Security Status](https://img.shields.io/badge/Security-Passed-brightgreen.svg)](SECURITY.md)
[![Author](https://img.shields.io/badge/Author-Milad%20Rezanezhad-purple.svg)](https://github.com/miladrezanezhad)
[![PyPI version](https://img.shields.io/pypi/v/story-toolkit.svg)](https://pypi.org/project/story-toolkit/)

**یک کتابخانه جامع پایتون برای تولید داستان‌های جذاب و منسجم با پشتیبانی اختیاری از هوش مصنوعی**

Story Toolkit ابزارهایی برای ساخت شخصیت، تولید پیرنگ، نوشتن دیالوگ، جهان‌سازی و تحلیل انسجام داستان ارائه می‌دهد. **🎉 جدید در نسخه 2.2.3:** استحکام امنیتی با ۷۶ تست امنیتی (۱۰۰٪ پاس) و رفع آسیب‌پذیری‌های حیاتی.

---

## 🌐 زبان

این README به زبان‌های زیر موجود است:

| زبان | فایل |
|------|------|
| 🇬🇧 **English** | [README.md](README.md) |

---

## ✨ ویژگی‌ها

| ویژگی | توضیح |
|-------|-------|
| 🎭 **ساخت شخصیت** | ساخت شخصیت‌های پیچیده با ویژگی‌ها، اهداف، مهارت‌ها، ترس‌ها و روابط |
| 📚 **تولید پیرنگ** | تولید ساختار داستان برای ژانرهای مختلف |
| 💬 **نوشتن دیالوگ** | ایجاد دیالوگ‌های طبیعی با الگوهای زمینه‌محور |
| 🌍 **جهان‌سازی** | طراحی دنیاهای دقیق با مکان‌ها، فرهنگ‌ها، قوانین و جناح‌ها |
| 🔍 **بررسی انسجام** | شناسایی حفره‌های داستانی، تناقضات شخصیتی و مشکلات زمانی |
| 📊 **تحلیل متن** | تحلیل خوانایی، سرعت روایت، تعادل دیالوگ و غنای واژگان |
| 🤖 **پشتیبانی از LLM** | اتصال اختیاری به OpenAI، Anthropic و مدل‌های محلی |
| 💾 **حافظه بلندمدت** | پایگاه داده SQLite برای ذخیره‌سازی داستان‌ها |
| 📄 **خروجی چندفرمتی** | PDF، EPUB، HTML، JSON، Markdown |
| 📋 **قالب‌های آماده** | سفر قهرمان، 3 پرده، معمایی، عاشقانه، ترسناک |
| 💻 **ابزار خط فرمان** | رابط کاربری خط فرمان کامل |
| 🔒 **استحکام امنیتی** | محافظت در برابر XSS، تزریق SQL، مسیرگذاری |

---

## 📦 نصب

```bash
# نصب پایه (بدون LLM)
pip install story-toolkit

# با پشتیبانی از OpenAI (GPT-4, GPT-3.5)
pip install story-toolkit[openai]

# با پشتیبانی از Anthropic (Claude)
pip install story-toolkit[anthropic]

# با پشتیبانی از مدل محلی (Ollama - رایگان)
pip install story-toolkit[local]

# با پشتیبانی از خروجی PDF و EPUB
pip install story-toolkit[export]

# با ابزارهای تست امنیتی
pip install story-toolkit[security]

# نصب کامل (همه قابلیت‌ها)
pip install story-toolkit[all]

# یا نصب از طریق سورس
git clone https://github.com/miladrezanezhad/story-toolkit.git
cd story-toolkit
pip install -e .
```

---

## 🚀 شروع سریع

### استفاده پایه (بدون هوش مصنوعی)

```python
from story_toolkit import StoryToolkit

# ساخت نمونه از ابزار
toolkit = StoryToolkit()

# ساخت داستان
story = toolkit.create_story(genre="fantasy", theme="courage")

# افزودن قهرمان
hero = toolkit.add_character_to_story(story, "کای", "protagonist")
hero.add_trait("brave")
hero.add_goal("Save the kingdom")

# تولید دیالوگ
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "کای", "اهریمن", context="conflict"
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
اهریمن: چاره‌ای برام نذاشتی.
کای: همیشه یه راه هست. تو فقط اشتباه انتخاب کردی.
امتیاز انسجام: 100%
```

### استفاده از قالب‌های آماده (نسخه 2.2.1)

```python
from story_toolkit import StoryToolkit

toolkit = StoryToolkit()

# ساخت داستان با قالب سفر قهرمان (12 مرحله)
story = toolkit.use_template("hero_journey", genre="fantasy", theme="redemption")

# لیست همه قالب‌ها
templates = toolkit.list_templates()
for t in templates:
    print(f"{t['name']}: {t['stage_count']} مرحله")
```

### خروجی PDF (نسخه 2.2.0)

```python
from story_toolkit import StoryToolkit
from story_toolkit.exporters import PDFExporter, ExportConfig, PDFStyle

toolkit = StoryToolkit()
story = toolkit.create_story("fantasy", "courage")

# خروجی PDF
config = ExportConfig(title="داستان من", author="من", pdf_style=PDFStyle.PRINT)
exporter = PDFExporter(config)
exporter.export(story, "my_story.pdf")
```

### استفاده از ابزار خط فرمان (نسخه 2.2.2)

```bash
# ایجاد داستان جدید
story-toolkit story new --genre fantasy --theme courage

# لیست قالب‌های آماده
story-toolkit template list

# استفاده از قالب
story-toolkit template use hero_journey --output my_story.json
```

### استفاده پیشرفته با هوش مصنوعی

```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# ایجاد پشتیبان هوش مصنوعی (Mock برای تست)
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# تولید دیالوگ پیشرفته
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "کای", "اهریمن",
    context="نبرد نهایی",
    use_advanced=True,
    style="dramatic",
    num_lines=8
)

# بررسی وضعیت LLM
print(f"وضعیت LLM: {toolkit.get_llm_status()}")
```

---

## 🔒 ویژگی‌های امنیتی (نسخه 2.2.3)

نسخه 2.2.3 شامل استحکام امنیتی جامع است:

| کنترل امنیتی | وضعیت | توضیح |
|--------------|-------|-------|
| **پیشگیری XSS** | ✅ | کدگذاری HTML در تمام خروجی‌ها |
| **تزریق SQL** | ✅ | پرس و جوهای پارامتری |
| **مسیرگذاری** | ✅ | اعتبارسنجی مسیر |
| **تزریق دستورات** | ✅ | عدم استفاده از shell=True |
| **حفاظت DoS** | ✅ | محدودیت منابع |
| **امنیت حافظه** | ✅ | عدم نشت حافظه |
| **تست‌های امنیتی** | ✅ | ۷۶ تست (۱۰۰٪ پاس) |

```python
# ماژول پاک‌ساز امنیتی
from story_toolkit.security import sanitize_html, sanitize_path

# کدگذاری خودکار HTML
safe_text = sanitize_html("<script>alert('xss')</script>")
# خروجی: &lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;

# اعتبارسنجی مسیر فایل
safe_path = sanitize_path("../../../etc/passwd")
# خطا: ValueError: Path traversal attempt
```

---

## 🤖 پشتیبان‌های هوش مصنوعی (LLM)

| ارائه‌دهنده | نصب | نیاز به کلید API |
|-------------|------|------------------|
| **Mock** | داخلی | ❌ خیر (برای تست) |
| **OpenAI** | `pip install story-toolkit[openai]` | ✅ بله |
| **Anthropic** | `pip install story-toolkit[anthropic]` | ✅ بله |
| **محلی (Ollama)** | `pip install story-toolkit[local]` | ❌ خیر (رایگان) |

---

## 📋 قالب‌های آماده داستان (نسخه 2.2.1)

| نام قالب | ژانر | مراحل | توضیح |
|----------|------|-------|-------|
| `hero_journey` | فانتزی/ماجراجویی | 12 | سفر قهرمان (کمپبل) |
| `three_act` | عمومی | 3 | ساختار 3 پرده |
| `mystery_clues` | معمایی | 5 | ساختار داستان کارآگاهی |
| `romance_beat` | عاشقانه | 15 | ساختار 15 مرحله‌ای عاشقانه |
| `horror_cycle` | ترسناک | 6 | ساختار داستان ترسناک |

---

## 📄 فرمت‌های خروجی (نسخه 2.2.0)

| فرمت | توضیح | دستور |
|------|-------|-------|
| **PDF** | چاپ، دست‌نویس، کتاب الکترونیک | `exporter.export(story, "file.pdf")` |
| **EPUB** | کتاب الکترونیک | `exporter.export(story, "file.epub")` |
| **HTML** | 4 قالب (مدرن، کلاسیک، تیره، مینیمال) | `exporter.export(story, "file.html")` |
| **JSON** | داده خام | `save_story(story, "file.json")` |
| **Markdown** | متن خوانا | `export_to_markdown(story, "file.md")` |

---

## 💾 حافظه بلندمدت (نسخه 2.1.0)

```python
from story_toolkit import StoryToolkit

# فعال‌سازی حافظه SQLite
toolkit = StoryToolkit(memory_backend="sqlite", db_path="stories.db")

# ایجاد داستان با ذخیره خودکار
story = toolkit.create_story("fantasy", "courage", save_to_memory=True)

# افزودن رویداد به تایم‌لاین
toolkit.add_event(1, "قهرمان نقشه را پیدا می‌کند", "plot", 9)

# مشاهده تایم‌لاین
for event in toolkit.get_timeline():
    print(f"فصل {event.chapter}: {event.description}")

# لیست داستان‌های ذخیره شده
stories = toolkit.list_stored_stories()
```

---

## 📁 ساختار پروژه

```
story_toolkit/
├── story_toolkit/          # بسته اصلی پایتون
│   ├── core/               # موتور داستان، شخصیت، پیرنگ، جهان‌ساز
│   ├── generators/         # تولیدکننده‌های شخصیت، پیرنگ، دیالوگ
│   ├── nlp/                # بررسی‌کننده انسجام و تحلیلگر متن
│   ├── llm/                # لایه هوش مصنوعی
│   ├── memory/             # حافظه بلندمدت SQLite
│   ├── exporters/          # خروجی PDF، EPUB، HTML
│   ├── templates/          # قالب‌های آماده داستان
│   ├── cli/                # ابزار خط فرمان
│   ├── security/           # پاک‌سازهای امنیتی (نسخه 2.2.3)
│   └── utils/              # توابع کمکی
├── docs/                   # مستندات (انگلیسی و فارسی)
├── examples/               # مثال‌های استفاده
├── tests/                  # تست‌های واحد + تست‌های امنیتی
└── requirements.txt        # وابستگی‌ها
```

---

## 📖 مستندات

مستندات کامل به دو زبان موجود است:

| زبان | لینک |
|------|------|
| 🇬🇧 English | [docs/eng/index.html](docs/eng/index.html) |
| 🇮🇷 فارسی | [docs/fa-ir/index.html](docs/fa-ir/index.html) |

### صفحات مستندات

- **راهنمای شروع سریع** — در ۵ دقیقه اولین داستان خود را بسازید
- **مرجع API** — مستندات کامل همه کلاس‌ها و متدها
- **راهنمای یکپارچگی LLM** —如何使用 OpenAI، Anthropic و مدل‌های محلی
- **راهنمای CLI** — استفاده از ابزار خط فرمان
- **راهنمای امنیت** — بهترین روش‌های امنیتی
- **مثال‌ها** — مثال‌های ساده، کامل و پیشرفته

---

## 🧪 اجرای تست‌ها

```bash
# اجرای همه تست‌های واحد
pytest tests/v1 tests/v2 tests/v2_1 tests/v2_2 tests/v2_2_1 tests/v2_2_2 -v

# اجرای تست‌های امنیتی (۷۶ تست)
python tests/run_security_tests.py

# اجرای همه تست‌ها (واحد + امنیت)
python tests/test_story_toolkit.py

# اجرای تست امنیتی خاص
python tests/security/test_xss_prevention.py
```

همه تست‌ها باید با موفقیت گذرند:
```
✅ تست‌های واحد گذرانده شدند! (70/70)
✅ تست‌های امنیتی گذرانده شدند! (76/76)
```

---

## 🎮 مثال‌های استفاده

```bash
# مثال ساده
python -m examples.simple_example

# دموی کامل
python -m examples.example

# ویژگی‌های پیشرفته (با هوش مصنوعی)
python -m examples.advanced_example
```

---

## 🛠️ کامپوننت‌های اصلی

### توسعه شخصیت
```python
from story_toolkit.core.character import Character

hero = Character(name="النا", age=32, role="protagonist")
hero.add_trait("brave")
hero.add_skill("sword_mastery")
hero.add_relationship("Villain", "enemy", strength=9)
hero.advance_arc()  # initial → challenged → transformation → new_equilibrium
```

### جهان‌سازی
```python
from story_toolkit.core.world_builder import WorldBuilder

world = WorldBuilder()
world.create_world("الدوریا", "fantasy")
world.add_location("شهر کریستال", "کلانشهر باستانی", "city")
world.add_rule("magical", "فقط متولدان ماه‌گرفتگی جادو دارند")
world.add_faction("انجمن سایه", "سازمان مخفی", goals=["کنترل جادو"])
```

### تولید پیرنگ
```python
from story_toolkit.generators.plot_generator import PlotGenerator

gen = PlotGenerator()
plot = gen.generate_plot("mystery", complexity=4)
print(f"فصل‌ها: {plot['estimated_length']['estimated_chapters']}")
print(f"کلمات: {plot['estimated_length']['estimated_words']:,}")
```

### بررسی انسجام
```python
from story_toolkit.nlp.coherence_checker import CoherenceChecker

checker = CoherenceChecker()
report = checker.generate_coherence_report(story_data)

if report['plot_holes']:
    print("حفره‌های داستانی:")
    for hole in report['plot_holes']:
        print(f"  - {hole}")

for rec in report['recommendations']:
    print(f"💡 {rec}")
```

---

## 🔧 نیازمندی‌ها

- پایتون 3.11 یا بالاتر
- وابستگی‌های ذکر شده در `requirements.txt`

### وابستگی‌های اختیاری

| قابلیت | بسته |
|--------|------|
| OpenAI | `openai>=1.0.0` |
| Anthropic | `anthropic>=0.18.0` |
| مدل محلی | `ollama>=0.1.0` |
| خروجی PDF | `reportlab>=4.0` |
| خروجی EPUB | `ebooklib>=0.18` |
| تست امنیتی | `psutil>=5.9.0` |

---

## 🔄 تاریخچه نسخه‌ها

| نسخه | ویژگی‌ها | امنیت | پایتون |
|------|----------|-------|--------|
| **2.2.3** | استحکام امنیتی | 🔒 ۱۰۰٪ | 3.11+ |
| 2.2.2 | ابزار خط فرمان | ⚠️ بروزرسانی توصیه می‌شود | 3.11+ |
| 2.2.1 | قالب‌های آماده (5 قالب) | ⚠️ بروزرسانی توصیه می‌شود | 3.11+ |
| 2.2.0 | خروجی چندفرمتی (PDF, EPUB, HTML) | ⚠️ بروزرسانی توصیه می‌شود | 3.11+ |
| 2.1.0 | حافظه SQLite | ⚠️ بروزرسانی توصیه می‌شود | 3.11+ |
| 2.0.0 | لایه هوش مصنوعی | ⚠️ بروزرسانی توصیه می‌شود | 3.11+ |
| 1.0.0 | ویژگی‌های هسته | ⚠️ بروزرسانی توصیه می‌شود | 3.8+ |

---

## 🔒 گزارش آسیب‌پذیری امنیتی

لطفاً آسیب‌پذیری‌های امنیتی را به آدرس زیر گزارش کنید: **miladvf2014@gmail.com**

برای اطلاعات بیشتر، [SECURITY.md](SECURITY.md) را ببینید.

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است.

---

## 👤 نویسنده

**میلاد رضانژاد**

- گیت‌هاب: [https://github.com/miladrezanezhad](https://github.com/miladrezanezhad)
- پروژه: [https://github.com/miladrezanezhad/story-toolkit](https://github.com/miladrezanezhad/story-toolkit)

---

## 🤝 مشارکت

مشارکت‌ها پذیرفته می‌شوند!

---

## 🌟 حمایت

اگر این پروژه را مفید می‌دانید، لطفاً با دادن یک ⭐️ در گیت‌هاب از آن حمایت کنید!

---

*ساخته شده با ❤️ و 🔒 برای نویسندگان و برنامه‌نویسان*

---

## ✨ نکات برجسته نسخه 2.2.3

| ویژگی | توضیح |
|-------|-------|
| 🔒 **امنیت** | ۷۶ تست امنیتی (۱۰۰٪ پاس) |
| 🛡️ **محافظت XSS** | کدگذاری HTML در تمام خروجی‌ها |
| 🚫 **تزریق SQL** | پرس و جوهای پارامتری |
| 📁 **مسیرگذاری** | اعتبارسنجی مسیر |
| 💻 **تزریق دستورات** | عدم استفاده از shell=True |
| 🔐 **ماژول امنیت** | `story_toolkit.security` |
| 🧪 **تست‌های امنیتی** | اجرا با `python tests/run_security_tests.py` |
| 📄 **مستندات امنیت** | [SECURITY.md](SECURITY.md) |
