"""Sample: AI vs human nuance (Roland's podcast-style recording, 30 Oct 2026). 0:00-0:35."""
OUT = "faceless-nuance-sample.mp4"
P = "display:inline-block;font:700 38px Jakarta;padding:16px 30px;border-radius:40px;background:rgba(255,216,77,.12);border:2px solid #FFD84D;color:#FFD84D;margin:14px 16px 0 0"
S = []


def sc(a, b, img, html, tint=None):
    S.append({"a": a, "b": b, "img": img, "html": html, "tint": tint})


sc(0.0, 5.8, "people-call.png", "<div class='L' style='top:300px'><div class='k' data-at='0.1'>Respect has a language</div>"
   "<div class='h2' data-at='0.3'>There's a way you speak to an <span class='yel'>elder</span> in Nigeria.</div></div>")
sc(5.8, 9.8, "people-market.png", "<div class='L' style='top:300px'><div class='k' data-at='0'>You read the room first</div>"
   f"<span style='{P}' data-at='0.6'>Age</span><span style='{P}' data-at='2.0'>Where they're from</span><span style='{P}' data-at='3.4'>Who they are</span></div>")
sc(9.8, 17.3, "people-mentor.png", "<div class='L' style='width:1100px;top:270px'><div class='k' data-at='0'>Same message. Different respect.</div>"
   "<div class='box' data-at='1.2'><div class='t'>To an elder</div><div class='d'>“Good morning, sir. Please, how was your night?” 🙇🏾</div></div>"
   "<div class='box' data-at='3.9'><div class='t'>To a peer</div><div class='d'>“How far? You good?” 👋🏾</div></div></div>")
sc(17.3, 20.0, "paper-robot.jpg", "<div class='L' style='top:330px'><div class='k' data-at='0'>But AI?</div>"
   "<div class='h' data-at='0.2'>Doesn't get the</div><div class='h red pop' data-at='1.6' style='transform-origin:0 50%'>nuance.</div></div>")
sc(20.0, 23.8, "glass-dome-brain.jpg", "<div class='L' style='top:300px'><div class='k' data-at='0'>Not anti-AI</div>"
   "<div class='h2' data-at='0.2'>Lots of room for improvement.</div>"
   "<div class='bar' style='margin-top:50px'><div class='n'>AI today</div><div class='t' data-w='420' data-at='1.4' style='background:#FFD84D'><div class='v'>getting there</div></div></div></div>")
sc(23.8, 30.7, "typewriter-app.jpg", "<div class='L' style='top:300px'><div class='k' data-at='0.6'>Right now</div>"
   "<div class='h2' data-at='2.5'>Humans should still own the <span class='yel'>critical thinking.</span></div></div>")
sc(30.7, 35.5, "chrome-hourglass.jpg", "<div class='L' style='top:320px'><div class='h2' data-at='0.9'>Intelligence is expensive.</div>"
   "<div class='h yel pop' data-at='3.1' style='margin-top:30px;transform-origin:0 50%'>Originality is expensive.</div></div>")

CAPS = [
    (0.0, 5.8, "There's a certain way you speak to an elderly person in Nigeria."),
    (5.8, 9.8, "You handle the conversation based on who they are,"),
    (9.8, 15.1, "where they're from. You wouldn't talk to a younger person like that."),
    (15.1, 17.3, "Or a leader like that."),
    (17.3, 20.0, "I don't think AI understands these nuances."),
    (20.0, 23.8, "Not discrediting AI. There's lots of room for improvement."),
    (23.8, 30.2, "But right now, humans should still sit with critical thinking."),
    (30.7, 35.5, "Intelligence is expensive. Originality is expensive."),
]

SPEC = {"audio": "/home/claude/money_audio/roland-rec2.wav", "t0": 0.0, "t1": 35.5,
        "label": "AI VS HUMAN NUANCE", "scenes": S, "captions": CAPS}
