from agent.monitor import is_any_spike, wait_for_duration
from agent.analyze import get_logs, analyze_logs
from agent.remediate import restart_service
from agent.notify import send_slack_notification
import time

SERVICE_NAME = "apache2"  # change this to your target

def main():
    print("🔍 AI DevOps Agent started...")
    while True:
        if is_any_spike():
            print("⚠️  Spike detected. Verifying...")
            if wait_for_duration():
                print("✅ Confirmed spike. Analyzing logs...")
                logs = get_logs()
                analysis = analyze_logs(logs)

                if "Unknown" not in analysis:
                    print("🔁 Performing remediation...")
                    success = restart_service(SERVICE_NAME)
                    result = "successful" if success else "failed"

                    send_slack_notification(
                        title="[OpsBot] Spike Handled",
                        message=f"📍 *Root Cause:* {analysis}\n🔁 *Remediation:* {result}"
                    )
        time.sleep(30)

if __name__ == "__main__":
    main()
