"""Task Automation with Python scripts (CodeAlpha Python Task 3).

Three small automations in one script:
  move-jpg   Move all .jpg files from one folder into another
  emails     Extract email addresses from a .txt file into a new file
  title      Download a webpage and save its <title>

Examples:
  python automate.py move-jpg sample_data/photos sorted_jpgs --dry-run
  python automate.py emails sample_data/contacts.txt emails.txt
  python automate.py title --out title.txt
"""
import argparse
import os
import re
import shutil
import sys

import requests

DEFAULT_URL = "https://example.com"
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def unique_path(folder, filename):
    """Return a path in folder that doesn't exist yet (adds _1, _2 ... on clashes)."""
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(folder, filename)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(folder, f"{base}_{counter}{ext}")
        counter += 1
    return candidate


def move_jpgs(source, destination, dry_run=False):
    """Move .jpg/.jpeg files from source to destination. Returns list of (old, new)."""
    if not os.path.isdir(source):
        raise FileNotFoundError(f"Source folder not found: {source}")
    if not dry_run:
        os.makedirs(destination, exist_ok=True)
    moved = []
    for name in sorted(os.listdir(source)):
        path = os.path.join(source, name)
        if os.path.isfile(path) and name.lower().endswith((".jpg", ".jpeg")):
            target = unique_path(destination, name)
            if not dry_run:
                shutil.move(path, target)
            moved.append((path, target))
    return moved


def extract_emails(text):
    """Find all emails in text, without duplicates, in order of first appearance."""
    seen = []
    for email in EMAIL_PATTERN.findall(text):
        if email.lower() not in [s.lower() for s in seen]:
            seen.append(email)
    return seen


def extract_emails_file(input_path, output_path):
    with open(input_path, encoding="utf-8") as f:
        emails = extract_emails(f.read())
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(emails) + ("\n" if emails else ""))
    return emails


def fetch_title(url=DEFAULT_URL, timeout=10):
    """Download url and return the text inside its <title> tag."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    match = TITLE_PATTERN.search(response.text)
    if not match:
        raise ValueError("No <title> tag found on the page")
    return " ".join(match.group(1).split())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Simple task automation scripts")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("move-jpg", help="move .jpg files to a new folder")
    p.add_argument("source")
    p.add_argument("destination")
    p.add_argument("--dry-run", action="store_true", help="only show what would move")

    p = sub.add_parser("emails", help="extract emails from a .txt file")
    p.add_argument("input")
    p.add_argument("output")

    p = sub.add_parser("title", help="save a webpage's title")
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--out", default="title.txt")

    args = parser.parse_args(argv)
    try:
        if args.command == "move-jpg":
            moved = move_jpgs(args.source, args.destination, args.dry_run)
            verb = "Would move" if args.dry_run else "Moved"
            for old, new in moved:
                print(f"{verb}: {old} -> {new}")
            print(f"{verb} {len(moved)} file(s).")
        elif args.command == "emails":
            emails = extract_emails_file(args.input, args.output)
            print(f"Found {len(emails)} unique email(s); saved to {args.output}")
        elif args.command == "title":
            title = fetch_title(args.url)
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(title + "\n")
            print(f"Title of {args.url}: {title}\nSaved to {args.out}")
    except requests.RequestException as e:
        print(f"Network error: could not fetch page ({e.__class__.__name__})")
        return 1
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
