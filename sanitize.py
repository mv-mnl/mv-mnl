import re

def sanitize_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    replacements = [
        ("viktor@serhiienko", "{{ NAME_HEADER }}"),
        ("Linux (Pop!_OS 22.04 LTS)", "{{ OS }}"),
        ("None, Inc.", "{{ HOST }}"),
        ("Student (Paul Cornu High School) Operator", "{{ KERNEL }}"),
        ("VIM 8.2.2121, VSCode 1.114.0", "{{ IDE }}"),
        ("Rust, Python, NextJS, C++", "{{ LANG_PROG }}"),
        ("HTML, CSS, JSON, LaTeX", "{{ LANG_COMP }}"),
        ("English, French, Russian, German", "{{ LANG_REAL }}"),
        ("Programming Projects, Learning ML", "{{ HOBBY_SW }}"),
        ("Embedded Systems, Arduino Projects", "{{ HOBBY_HW }}"),
        ("Loving learning Maths, Physics ect..", "{{ HOBBY_OTH }}"),
        ("viktorserhiienko12@gmail.com", "{{ EMAIL_PERS }}"),
        ("viktorsrhk@gmail.com", "{{ EMAIL_WORK }}"),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    # Handle INSTA and DISCORD specifically since they are the same value originally
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "Instagram" in line and "viktor_srhk" in line:
            lines[i] = line.replace("viktor_srhk", "{{ INSTA }}")
        elif "Discord" in line and "viktor_srhk" in line:
            lines[i] = line.replace("viktor_srhk", "{{ DISCORD }}")
    
    content = '\n'.join(lines)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

sanitize_file("template_dark.svg")
sanitize_file("template_light.svg")
print("Sanitized successfully.")
