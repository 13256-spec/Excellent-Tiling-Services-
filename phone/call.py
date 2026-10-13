#!/usr/bin/env python3
"""Phone calls for Excellent Tiling Services through Bland.ai.

The API key is read from the BLAND_API_KEY environment variable (never from a file in this repo).
Numbers are Australian unless given with a country code: 0450 960 543 -> +61450960543.

Usage
  python3 phone/call.py account                       balance, plan, owned numbers
  python3 phone/call.py voices                        Australian voices available
  python3 phone/call.py owner "message to pass on"    call the owner and tell him something
  python3 phone/call.py call <contact|number> --task "what the agent should do" [--yes]
        [--first-sentence "..."] [--max-minutes 5] [--when "2026-10-14 18:30"] [--from +1...] [--record]
  python3 phone/call.py status <call_id>              outcome, summary and transcript of a call
  python3 phone/call.py list [n]                      last n calls (default 10)
  python3 phone/call.py stop <call_id>                hang up a live call

Anyone who is not in phone/contacts.json needs --yes, so a number can't be dialled by accident.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.bland.ai/v1"
HERE = os.path.dirname(os.path.abspath(__file__))
CONTACTS = os.path.join(HERE, "contacts.json")

BUSINESS = (
    "You are calling on behalf of Excellent Tiling Services, a tile and bathroom store at "
    "17A Olga Road, Maddington, Perth (excellenttilingservice.com.au, phone 0450 960 543). "
    "Showroom visits are by appointment, Monday to Saturday 4:30 pm to 9 pm. "
    "Be friendly, brief and natural, Australian spelling and manners. Never invent prices, stock or "
    "delivery dates: if asked something you were not told, say the owner will confirm by text. "
    "Never name any tile supplier. If the person asks not to be called again, apologise, agree, and end the call."
)

DEFAULT_VOICE = "amelia"           # Australian female (Bland preset)
DEFAULT_TZ = "Australia/Perth"


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def api_key():
    key = os.environ.get("BLAND_API_KEY", "").strip()
    if not key:
        die("BLAND_API_KEY is not set. Add it as a secret/environment variable in the cloud environment "
            "settings (Edit environment -> Network secrets or environment variables), then start a new session.")
    return key


def request(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"authorization": api_key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        text = e.read().decode(errors="replace")
        try:
            return {"status": "error", "http": e.code, **json.loads(text)}
        except ValueError:
            return {"status": "error", "http": e.code, "message": text[:500]}


def load_contacts():
    with open(CONTACTS) as f:
        return json.load(f)


def normalise(number):
    """Return E.164 for an Australian or international number, or None if it doesn't look like one."""
    n = re.sub(r"[^\d+]", "", number)
    if n.startswith("+"):
        return n if re.fullmatch(r"\+\d{8,15}", n) else None
    if n.startswith("0061"):
        n = "+" + n[2:]
        return n
    if n.startswith("61") and len(n) in (11,):
        return "+" + n
    if n.startswith("0") and len(n) == 10:          # 04xx xxx xxx or 08 xxxx xxxx
        return "+61" + n[1:]
    return None


def resolve(target):
    """contact name or number -> (e164, known_contact: bool, label)."""
    contacts = load_contacts()
    key = target.strip().lower()
    if key in contacts:
        return contacts[key]["number"], True, contacts[key].get("name", key)
    e164 = normalise(target)
    if not e164:
        die(f"'{target}' is not a contact in phone/contacts.json and not a valid phone number.")
    for name, c in contacts.items():
        if c["number"] == e164:
            return e164, True, c.get("name", name)
    return e164, False, e164


def place_call(number, task, first_sentence=None, max_minutes=5, when=None, from_number=None,
               record=False, voice=DEFAULT_VOICE, wait_for_greeting=True):
    body = {
        "phone_number": number,
        "task": BUSINESS + "\n\n" + task,
        "voice": voice,
        "max_duration": max_minutes,
        "wait_for_greeting": wait_for_greeting,
        "record": record,
        "timezone": DEFAULT_TZ,
        "language": "babel-en",
    }
    if first_sentence:
        body["first_sentence"] = first_sentence
    if when:
        # "YYYY-MM-DD HH:MM" in Perth time -> Bland's "YYYY-MM-DD HH:MM:SS -HH:MM"
        when = when.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", when):
            when += ":00"
        body["start_time"] = f"{when} +08:00"
    if from_number:
        body["from"] = from_number
    return request("POST", "/calls", body)


def cmd_account(_):
    me = request("GET", "/me")
    nums = request("GET", "/inbound")
    print(json.dumps({"account": me, "owned_numbers": nums.get("inbound_numbers", nums)}, indent=2))
    bal = (me.get("billing") or {}).get("current_balance")
    if isinstance(bal, (int, float)) and bal < 5:
        print("\nNote: Bland only allows calls outside the US/Canada after at least $5 of credits has been "
              "bought (Billing in the Bland dashboard). Australian calls will be refused until then.")


def cmd_voices(_):
    d = request("GET", "/voices")
    for v in d.get("voices", []):
        blob = json.dumps(v).lower()
        if "austral" in blob:
            print(f"{v.get('name'):<12} {v.get('id')}  {v.get('description') or ''}")


def cmd_owner(a):
    number, _, label = resolve("owner")
    msg = " ".join(a.message).strip()
    if not msg:
        die("Give the message to pass on, e.g. phone/call.py owner \"The 6:30 post went out; two new orders today.\"")
    task = (f"You are Claude, the owner's assistant. You are calling {label}, your boss. Greet him by name, "
            f"give him this message, answer any quick questions about it from what you know, and say goodbye. "
            f"Message: {msg}")
    res = place_call(number, task, first_sentence=f"Hi Yamen, it's Claude from the shop with a quick update.",
                     max_minutes=a.max_minutes, when=a.when, from_number=a.from_number, record=a.record)
    report(res, label)


def cmd_call(a):
    number, known, label = resolve(a.target)
    if not known and not a.yes:
        die(f"{number} is not in phone/contacts.json. Re-run with --yes once the owner has approved this call.")
    res = place_call(number, a.task, first_sentence=a.first_sentence, max_minutes=a.max_minutes,
                     when=a.when, from_number=a.from_number, record=a.record)
    report(res, label)


def report(res, label):
    print(json.dumps(res, indent=2))
    if res.get("status") == "success":
        print(f"\nCall to {label} queued. Check it with: python3 phone/call.py status {res.get('call_id')}")
    else:
        msg = str(res.get("message", "")).lower()
        if "international" in msg or "purchase" in msg or "credit" in msg or "balance" in msg:
            print("\nBland needs a one-off purchase of at least $5 credits before it will dial Australian numbers "
                  "(Bland dashboard -> Billing). Then run this again.", file=sys.stderr)
        sys.exit(2)


def cmd_status(a):
    d = request("GET", f"/calls/{a.call_id}")
    keep = {k: d.get(k) for k in ("status", "queue_status", "answered_by", "call_length", "completed",
                                  "error_message", "summary", "recording_url", "to", "from", "created_at")}
    print(json.dumps(keep, indent=2))
    t = d.get("concatenated_transcript")
    if t:
        print("\nTranscript:\n" + t)


def cmd_list(a):
    d = request("GET", f"/calls?limit={a.n}")
    for c in d.get("calls", []):
        print(f"{c.get('created_at','')[:16]}  {c.get('to')}  {c.get('queue_status') or c.get('status')}  "
              f"{c.get('call_length') or 0:.1f} min  {c.get('call_id')}")
    if not d.get("calls"):
        print(json.dumps(d, indent=2))


def cmd_stop(a):
    print(json.dumps(request("POST", f"/calls/{a.call_id}/stop"), indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--max-minutes", type=int, default=5)
        sp.add_argument("--when", help='Perth time "YYYY-MM-DD HH:MM" to schedule; omit to call now')
        sp.add_argument("--from", dest="from_number", help="a number this account owns (E.164)")
        sp.add_argument("--record", action="store_true")

    sub.add_parser("account").set_defaults(fn=cmd_account)
    sub.add_parser("voices").set_defaults(fn=cmd_voices)
    o = sub.add_parser("owner"); o.add_argument("message", nargs="+"); common(o); o.set_defaults(fn=cmd_owner)
    c = sub.add_parser("call"); c.add_argument("target"); c.add_argument("--task", required=True)
    c.add_argument("--first-sentence"); c.add_argument("--yes", action="store_true"); common(c); c.set_defaults(fn=cmd_call)
    s = sub.add_parser("status"); s.add_argument("call_id"); s.set_defaults(fn=cmd_status)
    l = sub.add_parser("list"); l.add_argument("n", nargs="?", type=int, default=10); l.set_defaults(fn=cmd_list)
    x = sub.add_parser("stop"); x.add_argument("call_id"); x.set_defaults(fn=cmd_stop)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
