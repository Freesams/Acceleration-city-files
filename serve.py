# Run:  python serve.py   then open http://localhost:8000/
import http.server, socketserver, os
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        # Unity .unityweb files are stored pre-compressed: tell the browser how
        p = self.translate_path(self.path.split("?")[0])
        if p.endswith(".unityweb") and os.path.isfile(p):
            head = open(p,"rb").read(12)
            if head[:2] == b"\x1f\x8b": self.send_header("Content-Encoding","gzip")
            elif head[:4] != b"\0asm" and not head.startswith(b"UnityWeb"): self.send_header("Content-Encoding","br")
        super().end_headers()
    def guess_type(self, path):
        if path.endswith(".wasm.unityweb"): return "application/wasm"
        if path.endswith(".js.unityweb"): return "application/javascript"
        return super().guess_type(path)
H.extensions_map.update({".download":"application/javascript"})
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with socketserver.TCPServer(("",8000),H) as s:
    print("http://localhost:8000/"); s.serve_forever()
