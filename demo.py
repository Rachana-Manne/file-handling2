"""Demonstration of the FileHandler API."""

from fileutils import FileHandler, FileOperationError

handler = FileHandler()

try:
    # Text: write, append, read (the folder is created automatically)
    handler.write_text("demo_output/notes.txt", "First line\n")
    handler.append_text("demo_output/notes.txt", "Second line\n")
    print("Text file contents:")
    print(handler.read_text("demo_output/notes.txt"))

    # CSV: write, then read back
    employees = [
        {"name": "Alice", "department": "Finance", "salary": "72000"},
        {"name": "Bob", "department": "Engineering", "salary": "85000"},
    ]
    handler.write_csv("demo_output/employees.csv", employees)
    print("CSV rows:")
    for row in handler.read_csv("demo_output/employees.csv"):
        print(row)

    # Error handling: reading a file that does not exist
    handler.read_text("demo_output/missing.txt")

except FileOperationError as err:
    print(f"\nCaught FileOperationError: {err}")