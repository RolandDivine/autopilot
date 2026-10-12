"""Upload a PDF and an image to LinkedIn WITHOUT publishing a post. Proves media uploads work."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot.linkedin_client import LinkedInClient  # noqa: E402

c = LinkedInClient()
ok = True
for kind, path in (("images", "tests/assets/sample.png"), ("documents", "tests/assets/sample.pdf")):
    try:
        urn = c._upload(kind, path)
        st = c.s.get(f"{c.base}/rest/{kind}/{__import__('urllib.parse').parse.quote(urn)}", timeout=30)
        status = st.json().get("status") if st.ok else f"HTTP {st.status_code} {st.text[:200]}"
        print(f"::notice title={kind}::uploaded {urn} status={status}")
    except Exception as e:
        ok = False
        print(f"::error title={kind} upload failed::{str(e)[:500]}".replace("\n", " "))
sys.exit(0 if ok else 1)
