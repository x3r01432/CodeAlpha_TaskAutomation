# CodeAlpha Task Automation

CodeAlpha Python Programming internship task, by Steven Rios.

## Overview
One script, `automate.py`, with three automations as subcommands:
- `move-jpg`: moves all `.jpg`/`.jpeg` files from a folder into a new folder (`shutil`), renaming on name clashes (`photo_1.jpg`), with a `--dry-run` preview.
- `emails`: extracts email addresses from a `.txt` file with a regex, removes duplicates (case-insensitive) and saves them to another file.
- `title`: downloads a webpage (default `https://example.com`) with `requests` (10 s timeout) and saves its `<title>`; network errors print a friendly message.

Sample inputs are in `sample_data/` (`photos/` and `contacts.txt`).

## How to run
Requires Python 3.8+.
```bash
pip install -r requirements.txt
python automate.py move-jpg sample_data/photos sorted_jpgs --dry-run
python automate.py move-jpg sample_data/photos sorted_jpgs
python automate.py emails sample_data/contacts.txt emails.txt
python automate.py title --out title.txt   # or --url https://...
```
Run the tests:
```bash
python -m unittest -v
```

## Sample output
Captured from a scripted run with piped input (typed answers are not echoed when piped).
```text
Would move: sample_data/photos/beach.jpg -> sorted_jpgs/beach.jpg
Would move: sample_data/photos/family.jpeg -> sorted_jpgs/family.jpeg
Would move: sample_data/photos/sunset.JPG -> sorted_jpgs/sunset.JPG
Would move 3 file(s).
Found 3 unique email(s); saved to /tmp/emails.txt
alice.johnson@example.com
bob_smith@mail.example.org
support@codealpha.example
Title of https://example.com: Example Domain
Saved to /tmp/title.txt
```

## Concepts used
- `os` and `shutil` for file handling
- `re` regular expressions
- `requests` for HTTP, with timeout and error handling
- `argparse` subcommands
- `unittest` with temp folders and mocked `requests.get`

## LinkedIn demo script (60-90 s)
1. (0-10s) Intro: "CodeAlpha Task 3: automating tasks with Python."
2. (10-30s) Run `move-jpg ... --dry-run`, then the real move; show `sorted_jpgs/`.
3. (30-50s) Open `contacts.txt` (duplicates and invalid entries), run `emails`, open `emails.txt`.
4. (50-70s) Run `title`, open `title.txt`.
5. (70-85s) Run the tests and thank @CodeAlpha.

## License
MIT, see [LICENSE](LICENSE).
