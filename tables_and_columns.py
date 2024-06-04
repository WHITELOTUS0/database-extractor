import sqlite3
from fpdf import FPDF

# Connect to the SQLite database
db_path = './db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to get columns of a table
def get_columns(table_name):
    query = f"PRAGMA table_info({table_name});"
    cursor.execute(query)
    return cursor.fetchall()

# Get the list of tables
query = "SELECT name FROM sqlite_master WHERE type='table';"
cursor.execute(query)
tables = cursor.fetchall()

# Prepare data for PDF
pdf_data = []

for table in tables:
    table_name = table[0]
    columns = get_columns(table_name)
    column_names = [col[1] for col in columns]
    pdf_data.append((table_name, column_names))

# Close the connection
conn.close()

# Create a PDF document
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set title
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="SQLite Database Tables and Columns", ln=True, align='C')

# Add table data
for table_name, column_names in pdf_data:
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 10, txt=f"Table: {table_name}", ln=True, align='L')
    pdf.set_font("Arial", size=10)
    for column_name in column_names:
        pdf.cell(200, 10, txt=f"  - {column_name}", ln=True, align='L')

# Save PDF to file
pdf_output_path = "./db_tables_and_columns.pdf"
pdf.output(pdf_output_path)

print(f"PDF created: {pdf_output_path}")
