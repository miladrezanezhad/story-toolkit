"""
Web Dashboard Server for Story Development Toolkit.
Inspired by Google Gemini - Single Page Application with REST API.
Built entirely on Python standard library (no extra dependencies required).

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

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from story_toolkit import (
    StoryToolkit, LLMFactory, LLMProvider, BaseLLMBackend,
    TemplateManager, Character, WorldBuilder
)
from story_toolkit.nlp.coherence_checker import CoherenceChecker
from story_toolkit.nlp.text_analyzer import TextAnalyzer
from story_toolkit.exporters import ExportConfig, HTMLTemplate, PDFStyle


class StoryDashboardHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Gemini-style Story Toolkit Web Dashboard"""

    # Global toolkit instances cache
    toolkit_instance = None
    active_config = {
        "provider": "mock",
        "model": "mock",
        "api_key": "",
        "temperature": 0.7,
        "max_tokens": 1200,
        "db_path": "stories.db"
    }

    @classmethod
    def get_toolkit(cls):
        """Get or initialize StoryToolkit with current settings"""
        provider_name = cls.active_config.get("provider", "mock").lower()
        api_key = cls.active_config.get("api_key", "").strip() or None
        model = cls.active_config.get("model", "").strip() or None
        temp = float(cls.active_config.get("temperature", 0.7))

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
                temperature=temp
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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status=204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

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
                        "created_at": s.created_at.isoformat() if hasattr(s.created_at, 'isoformat') else str(s.created_at)
                    }
                    for s in stories
                ]
            except Exception as e:
                story_list = []
            self._set_headers()
            self.wfile.write(json.dumps({"stories": story_list}).encode("utf-8"))
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

            # 2. Settings update
            elif path == "/api/settings":
                for key in ["provider", "model", "api_key", "temperature", "max_tokens", "db_path"]:
                    if key in body:
                        self.active_config[key] = body[key]

                # Force re-instantiation
                StoryDashboardHandler.toolkit_instance = None
                new_tk = self.get_toolkit()
                self._set_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "config": self.active_config,
                    "llm_status": new_tk.get_llm_status()
                }).encode("utf-8"))
                return

            # 3. Create full story / novel
            elif path == "/api/story/create":
                genre = body.get("genre", "fantasy")
                theme = body.get("theme", "courage")
                num_chapters = int(body.get("num_chapters", 4))
                words_per_chapter = int(body.get("words_per_chapter", 300))
                protagonist = body.get("protagonist", None)
                antagonist = body.get("antagonist", None)
                save_db = body.get("save_to_memory", True)

                story = tk.generate_novel(
                    genre=genre,
                    theme=theme,
                    num_chapters=num_chapters,
                    words_per_chapter=words_per_chapter,
                    protagonist_name=protagonist,
                    antagonist_name=antagonist,
                    use_llm=True
                )

                if save_db and tk._memory:
                    sid = tk._memory.create_story(
                        name=f"{genre.capitalize()}: {theme.capitalize()} Chronicle",
                        genre=genre,
                        theme=theme,
                        description=f"Generated {num_chapters}-chapter novel"
                    )
                    story["memory_id"] = sid

                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "story": story}).encode("utf-8"))
                return

            # 4. Generate Character
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

            # 5. Generate Dialogue
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

            # 6. Apply Template
            elif path == "/api/templates/apply":
                tname = body.get("template", "hero_journey")
                genre = body.get("genre", "fantasy")
                theme = body.get("theme", "adventure")

                story = tk.use_template(tname, genre=genre, theme=theme)
                self._set_headers()
                self.wfile.write(json.dumps({"success": True, "story": story}).encode("utf-8"))
                return

            # 7. Check Coherence & Analyze Text
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

            # 8. Export Story
            elif path == "/api/export":
                story_data = body.get("story", {})
                fmt = body.get("format", "html")
                filename = body.get("filename", "exported_story")

                out_path = tk.export_story(story_data, format=fmt, filename=filename)

                # Read content for preview/download if text/html
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
            novel = tk.generate_novel(
                genre=genre,
                theme=theme,
                num_chapters=3,
                words_per_chapter=250,
                use_llm=True
            )
            return {
                "type": "story",
                "reply": f"Complete 3-chapter narrative draft created for **{genre.capitalize()} / {theme.capitalize()}**:",
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
