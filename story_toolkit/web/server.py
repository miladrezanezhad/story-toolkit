"""
Web Dashboard Server for Story Development Toolkit.
Inspired by Google Gemini - Single Page Application with REST API.
Built entirely on Python standard library (no extra dependencies required).

Features:
- Multi-LLM Support: Gemini, OpenCode Free, Cloudflare Workers AI, OpenAI, Claude, Local
- Configurable Proxy Support (HTTP/SOCKS)
- Persistent Memory & Configuration across restarts (dashboard_config.json + stories.db)
- Real Recent Stories Manager (Create, Load, Delete, Clear)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import os
import sys
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from datetime import datetime

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CONFIG_FILE = PROJECT_ROOT / "dashboard_config.json"

from story_toolkit import (
    StoryToolkit, LLMFactory, LLMProvider, BaseLLMBackend,
    TemplateManager, Character, WorldBuilder
)
from story_toolkit.memory.models import StoryModel
from story_toolkit.nlp.coherence_checker import CoherenceChecker
from story_toolkit.nlp.text_analyzer import TextAnalyzer
from story_toolkit.exporters import ExportConfig, HTMLTemplate, PDFStyle


def load_persistent_config() -> dict:
    """Load persistent configuration from file or default"""
    default_config = {
        "provider": "mock",
        "model": "mock",
        "api_keys": {
            "openai": "",
            "anthropic": "",
            "gemini": "",
            "opencode": "",
            "cloudflare": ""
        },
        "account_id": "",
        "proxy": "http://127.0.0.1:10808",
        "proxy_enabled": False,
        "temperature": 0.7,
        "max_tokens": 1200,
        "db_path": "stories.db"
    }

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                default_config.update(saved)
        except Exception as e:
            print(f"⚠️ Error reading config file: {e}")

    return default_config


def save_persistent_config(config: dict):
    """Save persistent configuration to file"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Error saving config file: {e}")


class StoryDashboardHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Gemini-style Story Toolkit Web Dashboard"""

    toolkit_instance = None
    active_config = load_persistent_config()

    @classmethod
    def get_toolkit(cls):
        """Get or initialize StoryToolkit with current settings and proxy"""
        provider_name = cls.active_config.get("provider", "mock").lower()
        api_keys = cls.active_config.get("api_keys", {})
        api_key = api_keys.get(provider_name, "").strip() or None
        model = cls.active_config.get("model", "").strip() or None
        temp = float(cls.active_config.get("temperature", 0.7))

        # Check proxy settings
        proxy = None
        if cls.active_config.get("proxy_enabled") and cls.active_config.get("proxy"):
            proxy = cls.active_config["proxy"].strip()
            # Also set environment proxies for underlying libraries
            os.environ["HTTP_PROXY"] = proxy
            os.environ["HTTPS_PROXY"] = proxy
            os.environ["ALL_PROXY"] = proxy
        else:
            os.environ.pop("HTTP_PROXY", None)
            os.environ.pop("HTTPS_PROXY", None)
            os.environ.pop("ALL_PROXY", None)

        account_id = cls.active_config.get("account_id", "").strip() or None

        try:
            provider = LLMProvider(provider_name)
        except ValueError:
            provider = LLMProvider.MOCK

        llm = None
        try:
            llm = LLMFactory.create_backend(
                provider=provider,
                api_key=api_key,
                model=model,
                temperature=temp,
                proxy=proxy,
                account_id=account_id
            )
        except Exception as e:
            print(f"⚠️ Failed to create LLM backend {provider_name}: {e}. Falling back to Mock.")
            llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)

        cls.toolkit_instance = StoryToolkit(
            llm_backend=llm,
            memory_backend="sqlite",
            db_path=cls.active_config.get("db_path", "stories.db")
        )
        return cls.toolkit_instance

    def _set_headers(self, content_type="application/json", status=200):
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status=204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ["/", "/index.html"]:
            html_file = Path(__file__).parent / "index.html"
            if html_file.exists():
                with open(html_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self._set_headers(content_type="text/html")
                self.wfile.write(content.encode("utf-8"))
            else:
                self._set_headers(status=404)
                self.wfile.write(b"Dashboard HTML not found")
            return

        elif path == "/api/status":
            tk = self.get_toolkit()
            llm_info = tk.get_llm_status()
            data = {
                "status": "online",
                "version": "2.2.3",
                "config": self.active_config,
                "llm": llm_info
            }
            self._set_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        elif path == "/api/templates":
            mgr = TemplateManager()
            templates = mgr.list_templates()
            self._set_headers()
            self.wfile.write(json.dumps({"templates": templates}).encode("utf-8"))
            return

        elif path == "/api/stories":
            tk = self.get_toolkit()
            try:
                stories = tk.list_stored_stories()
                story_list = [
                    {
                        "id": s.id,
                        "name": s.name,
                        "genre": s.genre,
                        "theme": s.theme,
                        "description": s.description,
                        "created_at": s.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(s.created_at, 'strftime') else str(s.created_at)[:16]
                    }
                    for s in stories
                ]
            except Exception as e:
                story_list = []
            self._set_headers()
            self.wfile.write(json.dumps({"stories": story_list}).encode("utf-8"))
            return

        elif path == "/api/story":
            story_id = query.get("id", [None])[0]
            if not story_id:
                self._set_headers(status=400)
                self.wfile.write(json.dumps({"error": "Story ID required"}).encode("utf-8"))
                return

            tk = self.get_toolkit()
            try:
                story_model = tk._memory.get_story(story_id)
                if not story_model:
                    self._set_headers(status=404)
                    self.wfile.write(json.dumps({"error": "Story not found"}).encode("utf-8"))
                    return

                characters = tk._memory.get_characters(story_id)
                events = tk._memory.get_timeline(story_id)

                story_data = {
                    "id": story_model.id,
                    "title": story_model.name,
                    "name": story_model.name,
                    "genre": story_model.genre,
                    "theme": story_model.theme,
                    "description": story_model.description,
                    "author": story_model.author,
                    "created_at": story_model.created_at.isoformat(),
                    "chapters": story_model.data.get("chapters", []) if story_model.data else [],
                    "characters": [
                        {
                            "name": c.name,
                            "role": c.role,
                            "traits": c.traits,
                            "goals": c.goals
                        }
                        for c in characters
                    ],
                    "timeline": [
                        {
                            "chapter": e.chapter,
                            "description": e.description,
                            "importance": e.importance
                        }
                        for e in events
                    ]
                }
                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "story": story_data}).encode("utf-8"))
                return
            except Exception as e:
                self._set_headers(status=500)
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                return

        self._set_headers(status=404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/story":
            story_id = query.get("id", [None])[0]
            if not story_id:
                self._set_headers(status=400)
                self.wfile.write(json.dumps({"error": "Story ID required"}).encode("utf-8"))
                return

            tk = self.get_toolkit()
            try:
                success = tk.delete_stored_story(story_id)
                self._set_headers()
                self.wfile.write(json.dumps({"success": success, "deleted_id": story_id}).encode("utf-8"))
                return
            except Exception as e:
                self._set_headers(status=500)
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                return

        self._set_headers(status=404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        tk = self.get_toolkit()

        try:
            # 1. Chat & Assistant endpoint
            if path == "/api/chat":
                message = body.get("message", "").strip()
                mode = body.get("mode", "auto")
                genre = body.get("genre", "fantasy")
                theme = body.get("theme", "courage")

                response_data = self._process_chat(message, mode, genre, theme, tk)
                self._set_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
                return

            # 2. Settings update & persistence
            elif path == "/api/settings":
                for key in ["provider", "model", "proxy", "proxy_enabled", "account_id", "temperature", "max_tokens", "db_path"]:
                    if key in body:
                        self.active_config[key] = body[key]

                if "api_keys" in body and isinstance(body["api_keys"], dict):
                    self.active_config.setdefault("api_keys", {}).update(body["api_keys"])

                # If single api_key passed
                if "api_key" in body and body["api_key"]:
                    prov = self.active_config.get("provider", "mock").lower()
                    self.active_config.setdefault("api_keys", {})[prov] = body["api_key"]

                # Save persistently to disk
                save_persistent_config(self.active_config)

                # Recreate toolkit with new config & proxy
                StoryDashboardHandler.toolkit_instance = None
                new_tk = self.get_toolkit()

                self._set_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "config": self.active_config,
                    "llm_status": new_tk.get_llm_status()
                }).encode("utf-8"))
                return

            # 3. Clear memory endpoint
            elif path == "/api/memory/clear":
                target = body.get("target", "all")
                result = {"success": True, "target": target}

                if target in ["stories", "all"]:
                    if tk._memory:
                        tk.clear_memory()
                    result["stories_cleared"] = True

                if target in ["config", "all"]:
                    self.active_config = {
                        "provider": "mock",
                        "model": "mock",
                        "api_keys": {
                            "openai": "",
                            "anthropic": "",
                            "gemini": "",
                            "opencode": "",
                            "cloudflare": ""
                        },
                        "account_id": "",
                        "proxy": "http://127.0.0.1:10808",
                        "proxy_enabled": False,
                        "temperature": 0.7,
                        "max_tokens": 1200,
                        "db_path": "stories.db"
                    }
                    save_persistent_config(self.active_config)
                    result["config_reset"] = True

                StoryDashboardHandler.toolkit_instance = None
                self._set_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
                return

            # 4. Create full story / novel with auto-save to memory
            elif path == "/api/story/create":
                genre = body.get("genre", "fantasy")
                theme = body.get("theme", "courage")
                num_chapters = int(body.get("num_chapters", 4))
                words_per_chapter = int(body.get("words_per_chapter", 300))
                protagonist = body.get("protagonist", None)
                antagonist = body.get("antagonist", None)
                title = body.get("title") or f"{genre.capitalize()}: {theme.capitalize()} Chronicle"

                story = tk.generate_novel(
                    genre=genre,
                    theme=theme,
                    num_chapters=num_chapters,
                    words_per_chapter=words_per_chapter,
                    protagonist_name=protagonist,
                    antagonist_name=antagonist,
                    use_llm=True
                )
                story["title"] = title

                if tk._memory:
                    sid = tk._memory.create_story(
                        name=title,
                        genre=genre,
                        theme=theme,
                        description=f"Generated {num_chapters}-chapter novel with {protagonist or 'Hero'} and {antagonist or 'Rival'}"
                    )
                    story["memory_id"] = sid

                    # Save story chapters into SQLite data column
                    story_model = tk._memory.get_story(sid)
                    if story_model:
                        story_model.data = {"chapters": story.get("chapters", [])}
                        tk._memory.memory.save_story(story_model)

                    # Add protagonist & antagonist to DB
                    if protagonist:
                        tk._memory.add_character(sid, protagonist, "protagonist", ["determined", "heroic"])
                    if antagonist:
                        tk._memory.add_character(sid, antagonist, "antagonist", ["ruthless", "ambitious"])

                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "story": story}).encode("utf-8"))
                return

            # 5. Generate Character
            elif path == "/api/character/create":
                role = body.get("role", "protagonist")
                name = body.get("name")
                char = tk.character_gen.generate_character(role)
                if name:
                    char.name = name

                traits = body.get("traits", [])
                for t in traits:
                    char.add_trait(t)

                char_dict = {
                    "id": char.id,
                    "name": char.name,
                    "role": char.role,
                    "age": char.age,
                    "personality_traits": char.personality_traits,
                    "goals": char.goals,
                    "fears": char.fears,
                    "skills": char.skills,
                    "weaknesses": char.weaknesses,
                    "background": char.background,
                    "arc_stage": char.arc_stage
                }
                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "character": char_dict}).encode("utf-8"))
                return

            # 6. Generate Dialogue
            elif path == "/api/dialogue/generate":
                speaker = body.get("speaker", "Protagonist")
                listener = body.get("listener", "Antagonist")
                context = body.get("context", "conflict")
                style = body.get("style", "dramatic")
                num_lines = int(body.get("num_lines", 5))

                dialogue = tk.dialogue_gen.generate_dialogue(
                    char1=speaker,
                    char2=listener,
                    context=context,
                    use_advanced=tk._llm_backend is not None,
                    style=style,
                    num_lines=num_lines
                )
                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "dialogue": dialogue}).encode("utf-8"))
                return

            # 7. Apply Template
            elif path == "/api/templates/apply":
                tname = body.get("template", "hero_journey")
                genre = body.get("genre", "fantasy")
                theme = body.get("theme", "adventure")

                story = tk.use_template(tname, genre=genre, theme=theme)

                # Save template story to memory
                if tk._memory:
                    sid = tk._memory.create_story(
                        name=f"{tname.replace('_', ' ').title()} - {genre.title()}",
                        genre=genre,
                        theme=theme,
                        description=f"Generated structure from template {tname}"
                    )
                    story["memory_id"] = sid

                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "story": story}).encode("utf-8"))
                return

            # 8. Check Coherence & Analyze Text
            elif path == "/api/coherence/check":
                text = body.get("text", "")
                story_data = body.get("story", None)

                analyzer = TextAnalyzer()
                analysis = analyzer.analyze_text(text) if text else {}

                report = {}
                if story_data and isinstance(story_data, dict):
                    report = tk.check_story_coherence(story_data)
                elif text:
                    report = {
                        "readability_score": analysis.get("readability_score", 75),
                        "reading_level": analysis.get("reading_level", "Standard"),
                        "word_count": analysis.get("word_count", len(text.split())),
                        "sentence_count": analysis.get("sentence_count", 1),
                        "vocabulary_richness": analysis.get("vocabulary_richness", 0.8),
                        "recommendations": [
                            "Maintain consistent character motivations across dialogue transitions.",
                            "Balance descriptive exposition with dialogue beats.",
                            "Keep narrative tension high towards the climax."
                        ]
                    }

                self._set_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "analysis": analysis,
                    "coherence": report
                }).encode("utf-8"))
                return

            # 9. Export Story
            elif path == "/api/export":
                story_data = body.get("story", {})
                fmt = body.get("format", "html")
                filename = body.get("filename", "exported_story")

                out_path = tk.export_story(story_data, format=fmt, filename=filename)

                file_content = ""
                if os.path.exists(out_path):
                    if fmt in ["html", "bionic_html", "markdown", "md", "json", "txt"]:
                        with open(out_path, "r", encoding="utf-8", errors="ignore") as f:
                            file_content = f.read()

                self._set_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "file_path": out_path,
                    "format": fmt,
                    "content": file_content
                }).encode("utf-8"))
                return

        except Exception as e:
            self._set_headers(status=500)
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        self._set_headers(status=404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def _process_chat(self, message: str, mode: str, genre: str, theme: str, tk: StoryToolkit):
        """Intelligent conversational processor that connects NLP, generators, and LLMs"""
        lower = message.lower()

        # 1. Character creation request
        if "character" in lower or "شخصیت" in lower or mode == "character":
            role = "protagonist"
            if "antagonist" in lower or "شرور" in lower or "ضد قهرمان" in lower:
                role = "antagonist"
            elif "mentor" in lower or "استاد" in lower or "راهنما" in lower:
                role = "mentor"

            char = tk.character_gen.generate_character(role)
            return {
                "type": "character",
                "reply": f"Here is a generated {role.capitalize()} for your story:",
                "data": {
                    "name": char.name,
                    "role": char.role,
                    "age": char.age,
                    "traits": char.personality_traits,
                    "goals": char.goals,
                    "fears": char.fears,
                    "skills": char.skills,
                    "background": char.background
                }
            }

        # 2. Dialogue request
        elif "dialogue" in lower or "دیالوگ" in lower or "گفتگو" in lower or mode == "dialogue":
            lines = tk.dialogue_gen.generate_dialogue(
                "Hero", "Rival",
                context="conflict",
                use_advanced=tk._llm_backend is not None,
                style="dramatic",
                num_lines=6
            )
            return {
                "type": "dialogue",
                "reply": "Here is an emotionally charged dialogue scene:",
                "data": {"lines": lines}
            }

        # 3. World building request
        elif "world" in lower or "جهان" in lower or "دنیای" in lower or mode == "world":
            builder = WorldBuilder()
            world = builder.generate_world(genre)
            return {
                "type": "world",
                "reply": f"Generated fictional world for genre **{genre.capitalize()}**:",
                "data": world
            }

        # 4. Template or Story Generation
        elif "story" in lower or "داستان" in lower or "novel" in lower or "رمان" in lower or mode == "story":
            title = f"{genre.capitalize()}: {theme.capitalize()} Chronicle"
            novel = tk.generate_novel(
                genre=genre,
                theme=theme,
                num_chapters=3,
                words_per_chapter=250,
                use_llm=True
            )
            novel["title"] = title

            # Auto-save to SQLite memory
            if tk._memory:
                try:
                    sid = tk._memory.create_story(
                        name=title,
                        genre=genre,
                        theme=theme,
                        description=f"Generated {genre} novel about {theme}"
                    )
                    novel["memory_id"] = sid
                    story_model = tk._memory.get_story(sid)
                    if story_model:
                        story_model.data = {"chapters": novel.get("chapters", [])}
                        tk._memory.memory.save_story(story_model)
                except Exception as e:
                    print(f"⚠️ Auto-save error: {e}")

            return {
                "type": "story",
                "reply": f"Complete 3-chapter narrative draft created for **{genre.capitalize()} / {theme.capitalize()}** (saved to database):",
                "data": novel
            }

        # 5. General creative query with LLM or fallback
        else:
            if tk._llm_backend:
                llm_reply = tk._llm_backend.generate(message)
                return {
                    "type": "text",
                    "reply": llm_reply
                }
            else:
                return {
                    "type": "text",
                    "reply": (
                        f"Welcome! I am your Story Development Toolkit assistant. "
                        f"You are currently using the **{self.active_config['provider'].upper()}** engine. "
                        f"I can generate novels, develop complex characters, compose dialogues, build fictional worlds, "
                        f"or diagnose plot holes. Click any prompt card or type your narrative request below."
                    )
                }


def run_dashboard(host="127.0.0.1", port=8080, open_browser=True):
    """Start the Story Toolkit web dashboard server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, StoryDashboardHandler)
    url = f"http://{host}:{port}"
    print("\n" + "=" * 70)
    print("✨ STORY TOOLKIT - GEMINI WEB DASHBOARD")
    print("=" * 70)
    print(f"🚀 Server running at: {url}")
    print(f"📁 Persistent config: {CONFIG_FILE}")
    print(f"🌐 Active Provider: {StoryDashboardHandler.active_config.get('provider').upper()}")
    if StoryDashboardHandler.active_config.get("proxy_enabled"):
        print(f"🛡️ Proxy Active: {StoryDashboardHandler.active_config.get('proxy')}")
    print("💡 Press Ctrl+C to stop the server.")
    print("=" * 70 + "\n")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping Story Toolkit dashboard server...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_dashboard(port=port)
