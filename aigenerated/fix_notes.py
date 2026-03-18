import re
import sys

with open('apptainer_hpc_workshop.md', 'r') as f:
    lines = f.readlines()

new_lines = []
in_speaker_note = False
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if the line is exactly "<!-- speaker_note:" followed by newline
    if re.match(r'^<!--\s*speaker_note:\s*\|?\s*$', line):
        new_lines.append("<!--\n")
        new_lines.append("speaker_note: |\n")
        in_speaker_note = True
        i += 1
        continue
    
    # Check if it's "<!--" and the next line is "speaker_note: |"
    if re.match(r'^<!--\s*$', line) and i+1 < len(lines) and re.match(r'^\s*speaker_note:\s*\|?\s*$', lines[i+1]):
        new_lines.append("<!--\n")
        new_lines.append("speaker_note: |\n")
        in_speaker_note = True
        i += 2
        continue

    # Note: What if the speaker note is like:
    # <!-- speaker_note:
    # TEXT
    # -->
    # This falls under the first condition `^<!--\s*speaker_note:\s*\|?\s*$`.
    
    # Now for inside the speaker note block
    if in_speaker_note:
        if line.strip() == '-->':
            in_speaker_note = False
            new_lines.append(line)
        else:
            if line.strip(): # if not empty
                new_lines.append(f"    {line.lstrip()}")
            else:
                new_lines.append("\n")
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

with open('apptainer_hpc_workshop.fixed.md', 'w') as f:
    f.writelines(new_lines)
