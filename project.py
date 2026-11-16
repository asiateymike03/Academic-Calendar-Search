import csv
import pymupdf
from pprint import pprint
import re
import sys

def main():
    # Validating command-line argument
    if len(sys.argv) <= 1 or len(sys.argv) >= 3:
        sys.exit("Command-line arguments provided are incorrect.")

    try:
        extracted_text = extract_text()
        results = search_text(extracted_text)
        try:
            output_choice = int(input(f"1) Print in console \n2) Export data as CSV \nEnter preferred selection: ")) 
        except ValueError:
            sys.exit("Selected choice should be a integer")
        output_format(output_choice, results)    
    except FileNotFoundError:
        print("Folder does not exist.")

table_details = {}

def extract_text() -> list:
    # accessing pdf file
    pdfFile = pymupdf.open("UG Distance Education Calendar 2026_2027.pdf")

    table_details = {}
    # extracting pdf table info
    for page_num in range(len(pdfFile)):
        page = pdfFile[page_num]
        tabs = page.find_tables()

        if tabs.tables:
            page_tables_list = []
            for table in tabs.tables:
                page_tables_list.append(table.extract())
            table_details[page_num + 1] = page_tables_list
    pdfFile.close()

    # group results
    groups = []
    for _, y in table_details.items():
        for z in y:
            for j in z:
                groups.append(j)
    return groups


def search_text(text: list)-> dict:
    textRegex = re.compile(re.escape(sys.argv[1]), re.IGNORECASE)

    # search keywords
    selected_texts = {
        keyword[0]: keyword[1] 
        for keyword in text 
        if keyword and isinstance(keyword[0], str) and textRegex.search(keyword[0])
        }
    return selected_texts


def output_format(choice_number: int, text: str):
    # print in terminal
    if choice_number == 1:
        print("\nActivity: Results")
        for keys, values in text.items():
            print(f"{clean(keys)}: {clean(values)}")
    # export to csv
    elif choice_number == 2:
        with open("results.csv", "w", newline="", encoding="utf-8") as csvFile:
            writer = csv.DictWriter(
                csvFile, 
                fieldnames=["Activity", "Results"]
                )
            
            writer.writeheader()

            for values,keys in text.items():
                writer.writerow(
                    {
                        "Activity": clean(values),
                        "Results" : clean(keys)
                    }
                )
        print("Results Exported.")
    else:
        print('Wrong number selected. Kindly select 1 or 2 and retry.')


def clean(text: str)-> str:
    if not isinstance(text, str):
        return text
    # Remove trailing run of whitespace, commas, hyphens, en/em dashes
    return re.sub(r'[\s,\-–—]+$', '', text)

if __name__ == '__main__':
    main()