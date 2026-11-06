import http.server
import functools


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Fonts and images rarely change; caching them avoids the text
        # flashing in on every page while still showing HTML/CSS edits.
        if self.path.split("?")[0].lower().endswith((".ttf", ".woff2", ".jpg", ".jpeg", ".png")):
            self.send_header("Cache-Control", "max-age=3600")
        else:
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    handler = functools.partial(NoCacheHandler, directory="docs")
    http.server.test(HandlerClass=handler, port=8000)
