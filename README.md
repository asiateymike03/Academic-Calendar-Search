# Project Title: Academic Calendar Search

#### Video Demo:  <URL HERE>

#### Description:
A small command-line tool that searches the tables inside a PDF academic calendar for a keyword and returns the matching rows. It was written for the *UG Distance Education Calendar 2026/2027*, but it works with any PDF whose key information is laid out in tables. Instead of scrolling through pages of dates, you type a keyword such as `registration` or `examination` and get back every activity that matches, along with its associated date or details. You can print the results to the console or save them to a CSV file.

## Features
- Extracts every table from every page of the PDF using PyMuPDF's table finder.
- Performs a case-insensitive search on the first column (the activity or event name).
- Shows the matching rows in the console, or exports them to `results.csv`.
- Cleans trailing whitespace, commas, hyphens, and dashes from extracted cells.
- Validates command-line input and menu choices, exiting with a clear message on bad input.

## Requirements
- Python 3.8 or newer
- [PyMuPDF]
- [Pytest]

## Installation Guide
 
- Navigate to your project folder
```bash
cd path/to/your/project_folder
```

- First create a virtual environment:
```bash
python3 -m venv .venv
```

- Activate virtual environment:
```bash
source .venv/bin/activate
```

- Install the dependency with:
```bash
pip install -r requirements.txt
```

- Verify installation
```bash
pip list
```

## Project Structure

```
- README.md
- project.py    (main project file)                     
- UG Distance Education Calendar 2026_2027.pdf  (test file) 
- results.csv   (csv result)                                
- requirements.txt
- test_project.py   (unit tests)
```

The PDF must sit in the same directory you run the script from, and its name must match the one in the code exactly.

## Usage

Run the script with a single search keyword:

```bash
python calendar_search.py "registration"
```

```
1) Print in console
2) Export data as CSV
Enter preferred selection:
```

### Option 1: Print in console

Each match is printed on its own line in the form `Activity: Result`:

```
Online Registration: 14 September 2026
Late Registration: 28 September 2026
```

### Option 2: Export as CSV

Matches are written to `results.csv` in the current directory with two columns, `Activity` and `Results`. The file is overwritten each time you export, so rename it if you want to keep earlier results. It is saved with UTF-8 encoding and opens correctly in Excel, Google Sheets, and LibreOffice.

## How It Works

The script is organised into four functions plus a `clean()` helper.

1. **`main()`** - checks that exactly one command-line argument was supplied, calls the other functions in order, and handles menu input.
2. **`extract_text()`** - opens the PDF, loops through each page, and calls `page.find_tables()`. Every detected table is extracted into a list of rows, and all rows from all pages are flattened into a single list.
3. **`search_text()`** - compiles the keyword into a case-insensitive regular expression (escaped with `re.escape`, so special characters are treated literally). It keeps any row whose first cell is a string containing the keyword, and builds a dictionary mapping the first cell to the second.
4. **`output_format()`** - prints the dictionary or writes it to CSV depending on your choice.
5. **`clean()`** - strips trailing whitespace, commas, hyphens, en dashes, and em dashes, which PDF extraction often leaves behind. Non-string values such as `None` are passed through unchanged.

## Error Handling

### Situation - Behaviour 
- No keyword or more than one argument | Exits with "Command-line arguments provided are incorrect." |
- Non-numeric menu entry | Exits with "Selected choice should be a integer" |
- Menu number other than 1 or 2 | Prints a message asking you to retry |
- PDF not found | Prints "Folder does not exist." |

## Limitations

- **Hardcoded filename.** The PDF path is written directly into `extract_text()`. To use a different file, edit that line or extend the script to accept the path as an argument.
- **Duplicate activities.** Results are stored in a dictionary keyed by the activity name, so two rows with the same first cell will overwrite each other and only the last survives. Switching to a list of `(activity, result)` tuples would fix this.

## Suggested Improvements

- Accept the PDF path as a second command-line argument or use `argparse`.
- Search all columns rather than only the first.
- Return a list instead of a dictionary to preserve duplicates.
- Print a "No matches found" message when the search returns nothing.

## Troubleshooting

**"Folder does not exist."** The PDF could not be found. Confirm it is in the directory you are running the script from and that the filename matches exactly, including spaces and underscores.

**`AttributeError: 'Page' object has no attribute 'find_tables'`.** Your PyMuPDF version is too old. Run `pip install --upgrade pymupdf`.

**Empty or missing results.** Try a shorter keyword, since the match is a substring search on the first column only. If that still fails, the PDF's tables may not be detectable.
