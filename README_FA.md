
# 📚 داستان‌ساز هوشمند | Story Toolkit

[![Tests](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/miladrezanezhad/story-toolkit/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](https://github.com/miladrezanezhad/story-toolkit/releases)
[![Author](https://img.shields.io/badge/Author-Milad%20Rezanezhad-purple.svg)](https://github.com/miladrezanezhad)

**یک کتابخانه جامع پایتون برای تولید داستان‌های جذاب و منسجم با پشتیبانی اختیاری از هوش مصنوعی**

Story Toolkit ابزارهایی برای ساخت شخصیت، تولید پیرنگ، نوشتن دیالوگ، جهان‌سازی و تحلیل انسجام داستان ارائه می‌دهد. **🎉 جدید در نسخه 2.0.0:** قابلیت اتصال اختیاری به OpenAI، Anthropic و مدل‌های محلی!

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
| 📚 **تولید پیرنگ** | تولید ساختار داستان برای ژانرهای فانتزی، معمایی، عاشقانه، ماجراجویی، علمی-تخیلی |
| 💬 **نوشتن دیالوگ** | ایجاد دیالوگ‌های طبیعی با الگوهای زمینه‌محور |
| 🌍 **جهان‌سازی** | طراحی دنیاهای دقیق با مکان‌ها، فرهنگ‌ها، قوانین و جناح‌ها |
| 🔍 **بررسی انسجام** | شناسایی حفره‌های داستانی، تناقضات شخصیتی و مشکلات زمانی |
| 📊 **تحلیل متن** | تحلیل خوانایی، سرعت روایت، تعادل دیالوگ و غنای واژگان |
| 🤖 **پشتیبانی از LLM** | اتصال اختیاری به OpenAI، Anthropic و مدل‌های محلی (جدید در نسخه 2.0.0) |

---

## 📦 نصب

```bash
# نصب پایه (بدون LLM)
pip install story-toolkit

# با پشتیبانی از OpenAI (GPT-4, GPT-3.5)
pip install story-toolkit[openai]

# با پشتیبانی از Anthropic (Claude)
pip install story-toolkit[anthropic]

# با پشتیبانی از مدل محلی (Ollama، llama.cpp)
pip install story-toolkit[local]

# نصب کامل (همه پشتیبان‌های LLM)
pip install story-toolkit[all]

# یا نصب از طریق سورس
git clone https://github.com/miladrezanezhad/story-toolkit.git
cd story-toolkit
pip install -e .
```

---

## 🚀 شروع سریع

### استفاده پایه (بدون LLM - سازگار با نسخه 1)

```python
from story_toolkit import StoryToolkit

# ساخت نمونه از ابزار
toolkit = StoryToolkit()

# ساخت داستان
story = toolkit.create_story(genre="fantasy", theme="courage")

# اضافه کردن قهرمان
hero = toolkit.add_character_to_story(story, "Kai", "protagonist")
hero.add_trait("brave")
hero.add_goal("Save the kingdom")

# تولید دیالوگ (بر اساس الگو)
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "Kai", "Villain", context="conflict"
)
for line in dialogue:
    print(line)

# بررسی انسجام
report = toolkit.check_story_coherence(story)
print(f"Coherence Score: {report['overall_score']:.0%}")
```

**خروجی:**
```
Kai: I can't believe you would do this!
Villain: You left me no choice.
Kai: There's always a choice. You just chose wrong.
Coherence Score: 100%
```

### استفاده پیشرفته (با LLM - جدید در نسخه 2.0.0)

```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# ساخت پشتیبان LLM (Mock برای تست، بدون نیاز به کلید API)
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# تولید دیالوگ پیشرفته با LLM
dialogue = toolkit.dialogue_gen.generate_dialogue(
    "Kai", "Villain",
    context="final_battle",
    use_advanced=True,  # فعال‌سازی LLM
    style="dramatic",
    num_lines=8
)

for line in dialogue:
    print(line)

# بررسی وضعیت LLM
print(f"LLM Status: {toolkit.get_llm_status()}")
```

**خروجی:**
```
Kai: I can't believe what you've done!
Villain: You left me no choice, Kai.
Kai: There's always a choice. You chose wrong.
Villain: We'll see who was wrong in the end.
Kai: This isn't over.
LLM Status: {'available': True, 'provider': 'mock', 'model': 'mock'}
```

---

## 🤖 پشتیبان‌های LLM

نسخه 2.0.0 از چندین ارائه‌دهنده LLM پشتیبانی می‌کند:

| ارائه‌دهنده | نصب | نیاز به کلید API |
|-------------|------|------------------|
| **Mock** | داخلی | ❌ خیر (برای تست) |
| **OpenAI** | `pip install story-toolkit[openai]` | ✅ بله |
| **Anthropic** | `pip install story-toolkit[anthropic]` | ✅ بله |
| **محلی (Ollama)** | `pip install story-toolkit[local]` | ❌ خیر (رایگان) |

### مثال با OpenAI

```python
import os
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# تنظیم کلید API
os.environ["OPENAI_API_KEY"] = "sk-..."

# ساخت پشتیبان OpenAI
llm = LLMFactory.create_backend(
    provider=LLMProvider.OPENAI,
    model="gpt-3.5-turbo",
    temperature=0.8
)

toolkit = StoryToolkit(llm_backend=llm)

# تولید دیالوگ پیشرفته
dialogue = toolkit.generate_advanced_dialogue(
    "Knight", "Dragon",
    context="final_battle",
    style="epic",
    num_lines=6
)
```

### مثال با مدل محلی (Ollama)

```bash
# ابتدا Ollama را نصب و اجرا کنید
ollama pull llama2
```

```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# ساخت پشتیبان محلی (رایگان، بدون کلید API)
llm = LLMFactory.create_backend(
    provider=LLMProvider.LOCAL,
    model="llama2",
    temperature=0.7
)

toolkit = StoryToolkit(llm_backend=llm)
```

---

## 📁 ساختار پروژه

```
story_toolkit/
├── story_toolkit/          # بسته اصلی پایتون
│   ├── core/               # موتور داستان، شخصیت، پیرنگ، جهان‌ساز
│   ├── generators/         # تولیدکننده‌های شخصیت، پیرنگ و دیالوگ
│   ├── nlp/                # بررسی‌کننده انسجام و تحلیلگر متن
│   ├── llm/                # لایه LLM (جدید در نسخه 2.0.0)
│   │   ├── base.py        # کلاس‌های پایه
│   │   ├── factory.py     # کارخانه ساخت پشتیبان
│   │   └── backends/      # Mock، OpenAI، Anthropic، Local
│   └── utils/              # توابع کمکی
├── docs/                   # مستندات (انگلیسی و فارسی)
│   ├── eng/                # مستندات انگلیسی
│   └── fa-ir/              # مستندات فارسی
├── examples/               # مثال‌های استفاده
├── tests/                  # تست‌های واحد
├── requirements.txt        # وابستگی‌ها
└── setup.py                # تنظیمات بسته
```

---

## 📖 مستندات

مستندات کامل به دو زبان موجود است:

| زبان | لینک |
|------|------|
| 🇬🇧 English | [docs/eng/index.html](docs/eng/index.html) |
| 🇮🇷 فارسی | [docs/fa-ir/index.html](docs/fa-ir/index.html) |

### صفحات مستندات

- **راهنمای شروع سریع** — در 5 دقیقه اولین داستان خود را بسازید
- **مرجع API** — مستندات کامل همه کلاس‌ها و متدها
- **راهنمای یکپارچگی LLM** —如何使用 OpenAI، Anthropic و مدل‌های محلی
- **مثال‌ها** — مثال‌های ساده، کامل و پیشرفته

---

## 🧪 اجرای تست‌ها

```bash
# اجرای همه تست‌ها
pytest tests/ -v

# تست‌های ماژول هسته
python -m tests.test_core

# تست‌های تولیدکننده‌ها
python -m tests.test_generators

# تست‌های ابزار NLP
python -m tests.test_nlp

# تست‌های لایه LLM
python -m tests.test_llm_quick.test_quick_verify
```

همه تست‌ها باید با موفقیت گذر کنند:
```
✅ StoryEngine tests passed!
✅ Character tests passed!
✅ Plot tests passed!
✅ WorldBuilder tests passed!
✅ LLM layer tests passed!
```

---

## 🎮 مثال‌های استفاده

### مثال ساده
```bash
python -m examples.simple_example
```

### دموی کامل
```bash
python -m examples.example
```

### ویژگی‌های پیشرفته (با LLM)
```bash
python -m examples.advanced_example
```

---

## 🛠️ کامپوننت‌های اصلی

### توسعه شخصیت
```python
from story_toolkit.core.character import Character

hero = Character(name="Elena", age=32, role="protagonist")
hero.add_trait("brave")
hero.add_skill("sword_mastery")
hero.add_relationship("Villain", "enemy", strength=9)
hero.advance_arc()  # initial → challenged → transformation → new_equilibrium
```

### جهان‌سازی
```python
from story_toolkit.core.world_builder import WorldBuilder

world = WorldBuilder()
world.create_world("Eldoria", "fantasy")
world.add_location("Crystal City", "Ancient metropolis", "city")
world.add_rule("magical", "Only eclipse-born can wield magic")
world.add_faction("Shadow Guild", "Secret organization", goals=["control_magic"])
```

### تولید پیرنگ
```python
from story_toolkit.generators.plot_generator import PlotGenerator

gen = PlotGenerator()
plot = gen.generate_plot("mystery", complexity=4)
print(f"Estimated chapters: {plot['estimated_length']['estimated_chapters']}")
print(f"Estimated words: {plot['estimated_length']['estimated_words']:,}")
```

### بررسی انسجام
```python
from story_toolkit.nlp.coherence_checker import CoherenceChecker

checker = CoherenceChecker()
report = checker.generate_coherence_report(story_data)

if report['plot_holes']:
    print("Plot holes found:")
    for hole in report['plot_holes']:
        print(f"  - {hole}")

for rec in report['recommendations']:
    print(f"💡 {rec}")
```

### دیالوگ با قدرت LLM (جدید)
```python
from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider

# راه‌اندازی LLM
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)

# تولید دیالوگ پیشرفته
dialogue = toolkit.generate_advanced_dialogue(
    "Hero", "Villain",
    context="conflict",
    style="dramatic",
    num_lines=10
)
```

---

## 🔧 نیازمندی‌ها

- پایتون 3.11 یا بالاتر
- وابستگی‌های ذکر شده در `requirements.txt`:
  - `nltk>=3.8.1`
  - `spacy>=3.7.0`
  - `textblob>=0.17.1`
  - `pydantic>=2.5.0`
  - `pyyaml>=6.0`

### وابستگی‌های اختیاری LLM

| پشتیبان | بسته |
|---------|------|
| OpenAI | `openai>=1.0.0` |
| Anthropic | `anthropic>=0.18.0` |
| محلی (Ollama) | `ollama>=0.1.0` |
| محلی (llama.cpp) | `llama-cpp-python>=0.2.0` |

---

## 🔄 ارتقا از نسخه 1.0.0 به 2.0.0

**هیچ تغییری ایجاد نشده است!** همه کدهای نسخه 1.0.0 بدون تغییر در نسخه 2.0.0 کار می‌کنند.

```python
# این کد نسخه 1.0.0 هنوز در نسخه 2.0.0 عالی کار می‌کند
from story_toolkit import StoryToolkit

toolkit = StoryToolkit()  # بدون LLM به طور پیش‌فرض
story = toolkit.create_story("fantasy", "courage")
# ... همه چیز مثل قبل کار می‌کند
```

برای استفاده از ویژگی‌های جدید LLM:
```python
# اختیاری: اضافه کردن LLM برای قابلیت‌های پیشرفته
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)
```

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است - برای جزئیات به فایل [LICENSE](LICENSE) مراجعه کنید.

---

## 👤 نویسنده

**میلاد رضازاده**

- گیت‌هاب: [https://github.com/miladrezanezhad](https://github.com/miladrezanezhad)
- پروژه: [https://github.com/miladrezanezhad/story-toolkit](https://github.com/miladrezanezhad/story-toolkit)

---

## 🤝 مشارکت

مشارکت‌ها پذیرفته می‌شوند! مراحل:

1. Fork کردن مخزن
2. ایجاد شاخه ویژگی (`git checkout -b feature/amazing-feature`)
3. Commit تغییرات (`git commit -m 'Add amazing feature'`)
4. Push به شاخه (`git push origin feature/amazing-feature`)
5. باز کردن Pull Request

---

## 🌟 حمایت

اگر این پروژه را مفید می‌دانید، لطفاً با دادن یک ⭐️ در گیت‌هاب از آن حمایت کنید!

---

*ساخته شده با ❤️ برای نویسندگان و برنامه‌نویسان*

## ✨ نکات برجسته نسخه 2.0.0

| ویژگی | توضیح |
|-------|-------|
| 🎯 **نشان‌ها** | Python 3.11+، مجوز، نسخه، نویسنده |
| ⚡ **شروع سریع** | کد آماده اجرا با خروجی نمونه |
| 🤖 **پشتیبانی از LLM** | OpenAI، Anthropic و مدل‌های محلی |
| 📁 **ساختار** | چیدمان پوشه پروژه با ماژول جدید llm/ |
| 📖 **مستندات** | لینک به مستندات انگلیسی و فارسی |
| 🧪 **تست‌ها** | نحوه اجرای تست‌های واحد شامل تست‌های LLM |
| 🛠️ **مثال‌ها** | قطعه کد برای هر کامپوننت |
| 🔄 **راهنمای ارتقا** | نحوه ارتقا از نسخه 1 به 2 |

