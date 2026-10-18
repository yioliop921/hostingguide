import hashlib
import re
import subprocess

REPO = r"C:\Users\Home\AppData\Local\Temp\opencode\hostingguide"

raw = subprocess.check_output(
    ["git", "show", "HEAD:index.html"], cwd=REPO, shell=False
)

print("  raw bytes    :", len(raw))
print("  CRLF pairs   :", raw.count(b"\r\n"))
print("  BOM          :", raw[:3] == b"\xef\xbb\xbf")

text = raw.decode("utf-8")
print("  utf-8 decode : OK,", len(text), "chars")
print("  mojibake     :", text.count("\u00e2\u20ac"))

m = re.search(r"<title>(.*?)</title>", text, re.S)
print("  title        :", m.group(1).encode("unicode_escape").decode())

checks = {
    "dark theme --bg:#06070c": "--bg:#06070c" in text,
    "brand #7c5cff": "#7c5cff" in text,
    "new 04c section": "4c &mdash;" in text,
    "stuck troubleshooting": "stuck on the parking page" in text,
    "60s nslookup check": "nslookup -type=A" in text,
    "4c anchor target": 'id="trouble-stuck"' in text,
    "4c link to it": 'href="#trouble-stuck"' in text,
    "no light bg": "background:#fff" not in text,
}
print()
for label, ok in checks.items():
    print("   ", "PASS" if ok else "FAIL", label)

print()
print("  blob sha1 :", hashlib.sha1(raw).hexdigest())
print("  sections  :", text.count("<section"), "/", text.count("</section>"))
print("  divs      :", len(re.findall(r"<div[ >]", text)), "/", text.count("</div>"))
print("  tables    :", text.count("<table"), "/", text.count("</table>"))
