import openai

openai.api_key = "<YOUR_OPENAI_API_KEY>"

def get_logs():
    try:
        with open("/var/log/syslog", "r") as f:
            return f.read()[-3000:]  # last 3000 chars
    except Exception as e:
        return f"Failed to read logs: {e}"

def analyze_logs(logs):
    prompt = f"""
You are an AI DevOps assistant. Analyze the following logs and identify the potential cause of high CPU, memory, or disk usage:

Logs:
{logs}

If you can identify the root cause, explain briefly.
If not, say 'Unknown'.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']
