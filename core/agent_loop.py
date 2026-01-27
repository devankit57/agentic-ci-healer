import time
import threading

from agents.log_analyzer import extract_error
from agents.reasoner import diagnose
from agents.fixer import apply_fix
from agents.verifier import is_confident

# ---- Rate limiting & idempotency ----
_last_heal_time = 0
_healing_lock = threading.Lock()
MIN_GEMINI_INTERVAL = 15   # seconds

def _throttle_gemini_calls():
    """Prevents Gemini 429 quota errors"""
    global _last_heal_time

    now = time.time()
    if now - _last_heal_time < MIN_GEMINI_INTERVAL:
        sleep_time = MIN_GEMINI_INTERVAL - (now - _last_heal_time)
        print(f"⏳ Throttling Gemini for {sleep_time:.1f}s...")
        time.sleep(sleep_time)

    _last_heal_time = time.time()

# ------------------------------------------------

def agentic_heal(logs: str):
    """
    Robust self-healing loop with:
    - rate limiting
    - safe retries
    - confidence checks
    - error isolation
    """

    with _healing_lock:   # prevents parallel healing jobs
        for attempt in range(1, 4):   # 3 attempts max
            print(f"\n🩺 Healing attempt {attempt}/3")

            try:
                # 1) Extract error
                error_log = extract_error(logs)
                print("📄 Extracted error:", error_log)

                # 2) Throttle Gemini to avoid 429
                _throttle_gemini_calls()

                # 3) Diagnose with Gemini
                diagnosis = diagnose(error_log)
                print("🤖 Diagnosis:", diagnosis)

                # 4) Confidence check
                if not is_confident(diagnosis):
                    print("⚠️ Low confidence from Gemini.")
                    return "Low confidence. Manual review needed."

                # 5) Apply fix (creates PR)
                fix_result = apply_fix(diagnosis["fix"])
                print("🔧 Fix result:", fix_result)

                return "Fix applied. Awaiting CI rerun."

            except Exception as e:
                print(f"❌ Attempt {attempt} failed:", str(e))

                if attempt < 3:
                    print("⏳ Retrying in 10 seconds...")
                    time.sleep(10)
                else:
                    return f"Healing failed after retries: {str(e)}"

    return "Healing failed."
    