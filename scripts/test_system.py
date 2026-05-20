"""
PhishGuard - System Test Script
=================================
Tests all backend API endpoints and validates ML model predictions.

Run:  python3 scripts/test_system.py
      (make sure backend is running: python3 backend/backend.py)
"""

import json
import sys
import time

try:
    import urllib.request
    import urllib.error
except ImportError:
    print("urllib not available")
    sys.exit(1)

BASE = "http://localhost:5000"

def post(path, payload):
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(f"{BASE}{path}", data=data,
           headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read()), r.status
    except Exception as e:
        return {"error": str(e)}, 0

def get(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=5) as r:
            return json.loads(r.read()), r.status
    except Exception as e:
        return {"error": str(e)}, 0

def pr(ok, label, detail=""):
    sym = "✅" if ok else "❌"
    print(f"  {sym}  {label}", f"→ {detail}" if detail else "")

print("=" * 55)
print("  PHISHGUARD SYSTEM TEST")
print("=" * 55)

# Health check
print("\n[1] Health Check")
r, code = get("/health")
pr(code==200 and r.get("status")=="online", "Backend online", f"Model: {r.get('model','?')}")

# Stats endpoint
print("\n[2] Stats Endpoint")
r, code = get("/stats")
pr(code==200 and "scanned" in r, "Stats returned", f"Scanned so far: {r.get('scanned',0)}")

# Test cases
print("\n[3] Prediction Tests")

cases = [
    {
        "name": "Legitimate Email",
        "expected": "ham",
        "payload": {
            "subject": "Team meeting tomorrow",
            "body": "Hi Sarah, just following up on our project discussion. Please find the agenda attached. Let me know if you have any questions. Best regards, Michael"
        }
    },
    {
        "name": "Spam Email",
        "expected": "spam",
        "payload": {
            "subject": "Congratulations! You won!",
            "body": "CONGRATULATIONS! You have been selected as our lucky winner! Claim your FREE prize of $5000 cash now! Click here to redeem before it expires. Limited time offer. Act NOW! Make money from home working just 2 hours a day. 100% guaranteed income!"
        }
    },
    {
        "name": "Phishing Email",
        "expected": "phishing",
        "payload": {
            "subject": "Urgent: Your account has been suspended",
            "body": "Dear Chase Customer, we have detected unusual activity on your account. Your account has been temporarily suspended. Please verify your identity immediately by clicking the link below and entering your credentials. Enter your credit card number and social security number to restore access."
        }
    },
    {
        "name": "Empty body (should fail)",
        "expected": None,
        "payload": {"subject": "Test", "body": ""}
    },
]

for case in cases:
    r, code = post("/predict", case["payload"])
    if case["expected"] is None:
        pr(code == 400, case["name"], "Correctly rejected empty body")
    else:
        got = r.get("label", "?")
        ok  = got == case["expected"]
        pr(ok, case["name"], f"Expected: {case['expected']} | Got: {got} | Confidence: {r.get('confidence','?')}%")

# Response time test
print("\n[4] Response Time Test (10 requests)")
times = []
for _ in range(10):
    t = time.time()
    post("/predict", {"subject": "Test", "body": "Hi team, the quarterly report is ready for review. Please find attached. Best regards."})
    times.append((time.time()-t)*1000)

avg = sum(times)/len(times)
pr(avg < 500, f"Average response time", f"{avg:.1f}ms (target <500ms)")
pr(max(times) < 1000, f"Max response time", f"{max(times):.1f}ms")

print("\n" + "=" * 55)
print(f"  Tests complete | Avg latency: {avg:.1f}ms")
print("=" * 55)
