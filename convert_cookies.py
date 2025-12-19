import json
import os

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read JSON cookies
with open(os.path.join(script_dir, 'cookies.json'), 'r', encoding='utf-8') as f:
    cookies = json.load(f)

# Write Netscape format
with open(os.path.join(script_dir, 'cookies.txt'), 'w', encoding='utf-8') as f:
    f.write("# Netscape HTTP Cookie File\n")
    f.write("# This is a generated file! Do not edit.\n\n")

    for cookie in cookies:
        domain = cookie.get('domain', '')
        flag = 'TRUE' if not cookie.get('hostOnly', False) else 'FALSE'
        path = cookie.get('path', '/')
        secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
        expiration = str(int(cookie.get('expirationDate', 0)))
        name = cookie.get('name', '')
        value = cookie.get('value', '')

        # Netscape format: domain\tflag\tpath\tsecure\texpiration\tname\tvalue
        line = f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n"
        f.write(line)

print("Cookies converted to Netscape format: cookies.txt")
