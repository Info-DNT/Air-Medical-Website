import json
import re

log_file = r"C:\Users\Admin\.gemini\antigravity-ide\brain\d69c5f0d-fa6e-4ffc-9b14-29bfb6c233e9\.system_generated\logs\transcript.jsonl"

with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get("step_index") == 0:
            content = data.get("content", "")
            # Remove base64 data to keep it small
            content_clean = re.sub(r'data:image\/[^;]+;base64,[A-Za-z0-9+/=]+', '[BASE64_IMAGE]', content)
            print(content_clean)
            with open("scratch/user_request_clean.txt", "w", encoding="utf-8") as out:
                out.write(content_clean)
            break
