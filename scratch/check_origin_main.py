import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_origin_main():
    try:
        # Get list of HTML files on origin/main
        files_data = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'origin/main']).decode('utf-8')
        html_files = [f.strip() for f in files_data.splitlines() if f.strip().endswith('.html')]
    except Exception as e:
        print(f"Error listing files: {e}")
        return

    # Garbled character patterns to look for
    garbled_patterns = [
        'ðŸš¨', 'ðŸ“ž', 'ðŸ’¬', 'ðŸ†˜', 'âœ‰ï¸', 'Ã¢â‚¬â€œ', 'Ã¢â‚¬â„¢', 'âœ…', 'â Œ',
        'ðŸ”’', 'ðŸ“¦', 'âœ…ï¸', 'Ã¢Â Å’', 'Ã¢Å“â€¦', 'ðŸš€', 'ðŸ‘¦'
    ]

    print(f"Checking {len(html_files)} files in origin/main...")
    found_any = False

    for f in html_files:
        try:
            content = subprocess.check_output(['git', 'show', f'origin/main:{f}']).decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error showing {f}: {e}")
            continue

        file_found = []
        for pattern in garbled_patterns:
            if pattern in content:
                count = content.count(pattern)
                file_found.append((pattern, count))
                found_any = True
        
        if file_found:
            print(f"File: {f}")
            for pattern, count in file_found:
                print(f"  - Pattern '{pattern}' found {count} times")

    if not found_any:
        print("Success! No garbled characters found in origin/main.")

if __name__ == '__main__':
    check_origin_main()
