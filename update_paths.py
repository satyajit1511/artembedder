import os

files = ['main.py', 'app/ui/main_window.py']
replacements = {
    '"music.png"': '"assets/music.png"',
    '"github.png"': '"assets/github.png"',
    '"github_light.png"': '"assets/github_light.png"',
    '"darkmode.png"': '"assets/darkmode.png"',
    '"lightmode.png"': '"assets/lightmode.png"'
}

for f_path in files:
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {f_path}")
    else:
        print(f"File not found: {f_path}")
