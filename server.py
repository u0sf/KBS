from __future__ import annotations

import html
import os
import secrets
import time
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from kb import KB

PORT = 5173
COOKIE_NAME = "sts_session"
SESSION_TTL_SEC = 60 * 60  # 1 hour


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, dict] = {}

    def _now(self) -> float:
        return time.time()

    def gc(self) -> None:
        now = self._now()
        dead = [sid for sid, s in self._sessions.items() if now - s.get("t", 0) > SESSION_TTL_SEC]
        for sid in dead:
            self._sessions.pop(sid, None)

    def get_or_create(self, sid: str | None) -> tuple[str, dict]:
        self.gc()
        if sid and sid in self._sessions:
            s = self._sessions[sid]
            s["t"] = self._now()
            return sid, s

        sid = secrets.token_urlsafe(24)
        s = {"t": self._now(), "history": [], "nodeId": KB["startNodeId"], "answerId": None, "resultId": None}
        self._sessions[sid] = s
        return sid, s

    def save(self, sid: str, s: dict) -> None:
        s["t"] = self._now()
        self._sessions[sid] = s


SESSIONS = SessionStore()


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def get_node(node_id: str) -> dict:
    node = KB["nodes"].get(node_id)
    if not node:
        raise KeyError(f"Unknown node id: {node_id}")
    return node


def get_result(result_id: str) -> dict:
    res = KB["results"].get(result_id)
    if not res:
        raise KeyError(f"Unknown result id: {result_id}")
    return res


def estimate_pct(history_len: int, estimate_total: int = 6) -> int:
    denom = max(history_len + 1, estimate_total)
    return max(0, min(100, round((history_len / denom) * 100)))


def render_shell(
    stage_html: str,
    *,
    category: str,
    progress_text: str,
    pct: int,
    back_disabled: bool,
    next_disabled: bool,
    next_text: str,
) -> str:
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>StS — نظام خبير لمشاكل الكمبيوتر</title>
    <meta name="description" content="نظام خبير (Knowledge-Based) لتشخيص مشاكل الكمبيوتر واللاب توب عبر أسئلة متسلسلة وإرشادات عملية." />
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <div class="bg"></div>
    <div class="shell">
      <header class="header">
        <div class="brand">
          <div class="logo" aria-hidden="true">StS</div>
          <div class="brandText">
            <div class="title">Smart Tech Support</div>
            <div class="subtitle">Knowledge-Based Troubleshooter</div>
          </div>
        </div>
        <div class="headerActions">
          <form method="post" action="/restart">
            <button class="btn ghost" type="submit">بدء جديد</button>
          </form>
        </div>
      </header>

      <main class="card" role="main">
        <section class="hero">
          <h1 class="h1">شخّص المشكلة خطوة بخطوة</h1>
          <p class="p">
            جاوب على الأسئلة بالترتيب، وفي النهاية هتاخد تشخيص محتمل + خطوات حل عملية وآمنة لمشاكل شائعة في الكمبيوتر واللاب توب.
          </p>
        </section>

        <section class="panel">
          <div class="progressRow">
            <div class="progressMeta">
              <span class="pill">{esc(category) if category else "—"}</span>
              <span class="muted">{esc(progress_text) if progress_text else ""}</span>
            </div>
            <div class="progressBar" aria-hidden="true">
              <div class="progressFill" style="width:{pct}%"></div>
            </div>
          </div>

          <div class="stage" aria-live="polite">
            {stage_html}
          </div>

          <div class="navRow">
            <form method="post" action="/back">
              <button class="btn ghost" type="submit" {"disabled" if back_disabled else ""}>رجوع</button>
            </form>
            <div class="spacer"></div>
            <form method="post" action="/next">
              <button class="btn primary" type="submit" {"disabled" if next_disabled else ""}>{esc(next_text)}</button>
            </form>
          </div>
        </section>
      </main>

      <footer class="footer">
        <div class="muted">
          ملاحظة: الخطوات المقترحة عامة. لو فيه ريحة حرق/سخونة شديدة أو كهرباء غير مستقرة، افصل الجهاز فورًا.
        </div>
      </footer>
    </div>
  </body>
</html>"""


def render_question(node: dict, *, selected_answer_id: str | None, error: str | None = None) -> str:
    opts = []
    for opt in node.get("options", []):
        is_sel = selected_answer_id == opt["id"]
        opts.append(
            f"""
            <label class="opt" data-selected="{ "true" if is_sel else "false" }">
              <input type="radio" name="answer" value="{esc(opt["id"])}" {"checked" if is_sel else ""} />
              <div class="optMain">
                <div class="optLabel">{esc(opt.get("label",""))}</div>
                {f'<div class="optDesc">{esc(opt.get("desc",""))}</div>' if opt.get("desc") else ""}
              </div>
            </label>
            """
        )

    err_html = (
        '<div class="badge warn" style="margin-top:6px">لازم تختار إجابة قبل ما تكمل.</div>' if error else ""
    )
    return f"""
      <form method="post" action="/pick">
        <h2 class="qTitle">{esc(node.get("title",""))}</h2>
        {f'<p class="qHelp">{esc(node.get("help",""))}</p>' if node.get("help") else ""}
        {err_html}
        <div class="options" role="radiogroup" aria-label="خيارات الإجابة">
          {''.join(opts)}
        </div>
        <input type="hidden" name="nodeId" value="{esc(node["id"])}" />
        <button type="submit" class="btn" style="margin-top:12px">حفظ الإجابة</button>
      </form>
    """


def render_result(res: dict, *, steps_count: int, category: str) -> str:
    badge_class = "warn" if res.get("severity") == "warn" else "ok"
    badge_text = "تحذير" if res.get("severity") == "warn" else "إرشادات"
    steps = "".join(f"<li>{esc(s)}</li>" for s in res.get("steps", []))
    extra = res.get("extra")
    return f"""
      <div class="resultHeader">
        <div>
          <h2 class="qTitle">{esc(res.get("title",""))}</h2>
          <p class="qHelp">{esc(res.get("summary",""))}</p>
        </div>
        <span class="badge {badge_class}">{esc(badge_text)}</span>
      </div>

      <div class="badge" style="margin-top:10px">
        <span class="mini">الإجابات السابقة:</span>
        <span>{esc(str(steps_count) + " خطوة") if steps_count else "—"}</span>
      </div>

      <h3 class="qTitle" style="font-size:15px; margin-top:10px">خطوات مقترحة</h3>
      <ul class="list">{steps}</ul>
      {f'<p class="mini" style="margin-top:10px">{esc(extra)}</p>' if extra else ""}
    """


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/styles.css":
            return self._serve_file("styles.css", content_type="text/css; charset=utf-8")

        if parsed.path == "/":
            return self._render_page()

        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/pick", "/next", "/back", "/restart"):
            return self._handle_action(parsed.path)
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def _get_session(self) -> tuple[str, dict]:
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        sid = cookie.get(COOKIE_NAME)
        sid_val = sid.value if sid else None
        sid_val, s = SESSIONS.get_or_create(sid_val)
        return sid_val, s

    def _set_session_cookie(self, sid: str) -> None:
        c = SimpleCookie()
        c[COOKIE_NAME] = sid
        c[COOKIE_NAME]["path"] = "/"
        c[COOKIE_NAME]["httponly"] = True
        self.send_header("Set-Cookie", c.output(header="").strip())

    def _read_form(self) -> dict[str, str]:
        n = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(n).decode("utf-8", errors="replace")
        q = parse_qs(raw, keep_blank_values=True)
        return {k: (v[0] if v else "") for k, v in q.items()}

    def _redirect(self, location: str, sid: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER)
        self._set_session_cookie(sid)
        self.send_header("Location", location)
        self.end_headers()

    def _handle_action(self, path: str) -> None:
        sid, s = self._get_session()
        form = self._read_form()

        if path == "/restart":
            s["history"] = []
            s["nodeId"] = KB["startNodeId"]
            s["answerId"] = None
            s["resultId"] = None
            SESSIONS.save(sid, s)
            return self._redirect("/", sid)

        if path == "/back":
            hist = s.get("history", [])
            if hist:
                last = hist.pop()
                s["nodeId"] = last.get("nodeId")
                s["answerId"] = last.get("answerId")
                s["resultId"] = None
                s["history"] = hist
                SESSIONS.save(sid, s)
            return self._redirect("/", sid)

        if path == "/pick":
            node_id = form.get("nodeId") or s.get("nodeId") or KB["startNodeId"]
            node = get_node(node_id)
            answer_id = form.get("answer") or None
            if answer_id and any(o["id"] == answer_id for o in node.get("options", [])):
                s["nodeId"] = node_id
                s["answerId"] = answer_id
                s["resultId"] = None
                SESSIONS.save(sid, s)
            return self._redirect("/", sid)

        if path == "/next":
            if s.get("resultId"):
                return self._redirect("/", sid)

            node = get_node(s.get("nodeId") or KB["startNodeId"])
            answer_id = s.get("answerId")
            if not answer_id:
                return self._render_page(error="missing_answer", sid=sid, session=s)

            opt = next((o for o in node.get("options", []) if o["id"] == answer_id), None)
            if not opt:
                s["answerId"] = None
                SESSIONS.save(sid, s)
                return self._render_page(error="missing_answer", sid=sid, session=s)

            hist = s.get("history", [])
            hist.append({"nodeId": node["id"], "answerId": answer_id})
            s["history"] = hist

            if "result" in opt:
                s["resultId"] = opt["result"]
                SESSIONS.save(sid, s)
                return self._redirect("/", sid)

            nxt = opt.get("next")
            if nxt:
                s["nodeId"] = nxt
                s["answerId"] = None
                s["resultId"] = None
                SESSIONS.save(sid, s)
                return self._redirect("/", sid)

            return self._redirect("/", sid)

        self.send_error(HTTPStatus.BAD_REQUEST, "Bad Request")

    def _serve_file(self, filename: str, *, content_type: str) -> None:
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, filename)
        if not os.path.isfile(path):
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _render_page(self, error: str | None = None, sid: str | None = None, session: dict | None = None) -> None:
        sid, s = (sid, session) if (sid and session) else self._get_session()

        history = s.get("history", [])
        node_id = s.get("nodeId") or KB["startNodeId"]
        answer_id = s.get("answerId")
        result_id = s.get("resultId")

        if result_id:
            res = get_result(result_id)
            stage = render_result(res, steps_count=len(history), category="")
            category = "النتيجة"
            progress_text = "تم التشخيص"
            pct = 100
            next_disabled = True
            next_text = "تم"
        else:
            node = get_node(node_id)
            stage = render_question(node, selected_answer_id=answer_id, error=error)
            category = node.get("category") or "—"
            progress_text = f"سؤال {len(history) + 1}"
            pct = estimate_pct(len(history))
            next_disabled = not bool(answer_id)
            next_text = "التالي"

        page = render_shell(
            stage,
            category=category,
            progress_text=progress_text,
            pct=pct,
            back_disabled=len(history) == 0,
            next_disabled=next_disabled,
            next_text=next_text,
        )

        data = page.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self._set_session_cookie(sid)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"StS server running on http://localhost:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

