# test_project.py
import csv
import unittest
from unittest.mock import MagicMock, patch

from project import extract_text, clean, search_text, output_format


def make_fake_page(rows):
    """Build a fake PDF page that contains one table with the given rows."""
    table = MagicMock()
    table.extract.return_value = rows        # table.extract() gives back our rows

    tabs = MagicMock()
    tabs.tables = [table]                    # page.find_tables().tables -> [table]

    page = MagicMock()
    page.find_tables.return_value = tabs     # page.find_tables() -> tabs
    return page


class TestExtractText(unittest.TestCase):

    @patch("project.pprint")                 # silence the printing during tests
    @patch("project.pymupdf.open")
    def test_single_page(self, mock_open, mock_pprint):
        rows = [["Event", "Date"], ["Registration", "5 Jan"]]

        fake_pdf = MagicMock()
        fake_pdf.__len__.return_value = 1                 # PDF has 1 page
        fake_pdf.__getitem__.return_value = make_fake_page(rows)
        mock_open.return_value = fake_pdf                 # pymupdf.open() returns our fake PDF

        result = extract_text()

        self.assertEqual(result, rows)                    # all rows come back as one flat list
        fake_pdf.close.assert_called_once()               # the PDF was closed

    @patch("project.pprint")
    @patch("project.pymupdf.open")
    def test_multiple_pages(self, mock_open, mock_pprint):
        page1 = make_fake_page([["A", "1"]])
        page2 = make_fake_page([["B", "2"]])

        fake_pdf = MagicMock()
        fake_pdf.__len__.return_value = 2                 # PDF has 2 pages
        fake_pdf.__getitem__.side_effect = [page1, page2] # page 0 -> page1, page 1 -> page2
        mock_open.return_value = fake_pdf

        result = extract_text()

        self.assertEqual(result, [["A", "1"], ["B", "2"]])


@patch("project.sys.argv", ["project.py", "name"])
def test_search_text():
    text = [
        ["name", "Michael"],
        ["Age", 23],
        ["loCation", "Ghana"]
    ]

    assert search_text(text) == {
        "name": "Michael"
    }


def test_output_format_print(capsys):
    text = {
        "Activity": "Python",
        "Results": "Passed"
    }

    output_format(1, text)

    captured = capsys.readouterr()

    assert "Activity: Python" in captured.out
    assert "Results: Passed" in captured.out


def test_output_format_csv(tmp_path, monkeypatch, capsys):
    text = {
        "Activity": "Python",
        "Results": "Passed"
    }

    monkeypatch.chdir(tmp_path)

    output_format(2, text)

    file_path = tmp_path / "results.csv"

    assert file_path.exists()

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert rows == [
        {"Activity": "Activity", "Results": "Python"},
        {"Activity": "Results", "Results": "Passed"}
    ]

    captured = capsys.readouterr()
    assert "Results Exported." in captured.out

def test_clean():
    assert clean("Hello World,   ") == "Hello World"
    assert clean("Hello World---") == "Hello World"
    assert clean("Hello World—") == "Hello World"
    assert clean("Hello World–") == "Hello World"
    assert clean("Hello World") == "Hello World"
    assert clean("") == ""

if __name__ == "__main__":
    unittest.main()