#!/usr/bin/python3
"""
A script that converts Markdown files to HTML format. It checks for
the existence of the Markdown file and handles command-line arguments
appropriately.
"""

import sys
import os
import hashlib


def md5_hash(text):
    """Convert text to its MD5 hash."""
    return hashlib.md5(text.encode()).hexdigest()


def convert_markdown_to_html(markdown_text):
    """Convert Markdown text to HTML format."""
    html_lines = []
    lines = markdown_text.splitlines()
    inside_list = False

    for line in lines:
        # Handle headings
        if line.startswith("#"):
            heading_level = line.count("#")
            heading_text = line[heading_level:].strip()
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")

        # Handle unordered lists
        elif line.startswith("- ") or line.startswith("* "):
            if not inside_list:
                html_lines.append("<ul>")
                inside_list = True
            item_text = line[2:].strip()
            html_lines.append(f"<li>{item_text}</li>")

        # Handle ordered lists
        elif line.startswith("1. "):
            if not inside_list:
                html_lines.append("<ol>")
                inside_list = True
            item_text = line[3:].strip()
            html_lines.append(f"<li>{item_text}</li>")

        else:
            if inside_list:
                html_lines.append("</ul>")
                inside_list = False
            elif line.strip() == "":
                continue  # Skip empty lines

            # Handle special Markdown syntax
            if line.startswith("[[") and line.endswith("]]"):
                content = line[2:-2]
                line = md5_hash(content)
            elif line.startswith("((") and line.endswith("))"):
                content = line[2:-2]
                line = content.replace("c", "").replace("C", "")

            # Handle bold and emphasis
            line = line.replace("**", "<b>", 1).replace("**", "</b>", 1)  # For bold
            line = line.replace("__", "<em>", 1).replace(
                "__", "</em>", 1
            )  # For emphasis

            # Handle paragraphs
            if line.strip():  # Only add non-empty lines
                html_lines.append(f"<p>{line.strip()}</p>")

    if inside_list:
        html_lines.append("</ul>")  # Close the unordered list if it was opened
    if html_lines and html_lines[-1].startswith("<ol>"):
        html_lines.append("</ol>")  # Close the ordered list if it was opened

    return "\n".join(html_lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)

    with open(markdown_file, "r") as f:
        markdown_text = f.read()

    html_content = convert_markdown_to_html(markdown_text)

    with open(output_file, "w") as f:
        f.write(html_content)

    exit(0)


if __name__ == "__main__":
    main()
