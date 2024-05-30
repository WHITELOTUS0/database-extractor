import sqlite3
from fpdf import FPDF

# Connect to the SQLite database
db_path = './db.sqlite3'  # Update this path to your SQLite database file
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to get columns, primary keys, and foreign keys of a table
def get_table_info(table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    foreign_keys = cursor.fetchall()

    return columns, foreign_keys

# Get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Prepare data for PDF
pdf_data = []

for table in tables:
    table_name = table[0]
    columns, foreign_keys = get_table_info(table_name)
    column_info = []
    primary_keys = []

    for col in columns:
        col_dict = {
            "name": col[1],
            "type": col[2],
            "notnull": col[3],
            "default_value": col[4],
            "pk": col[5]
        }
        column_info.append(col_dict)
        if col[5] != 0:
            primary_keys.append(col[1])

    foreign_key_info = []
    for fk in foreign_keys:
        fk_dict = {
            "id": fk[0],
            "seq": fk[1],
            "table": fk[2],
            "from": fk[3],
            "to": fk[4],
            "on_update": fk[5],
            "on_delete": fk[6],
            "match": fk[7]
        }
        foreign_key_info.append(fk_dict)

    pdf_data.append({
        "table_name": table_name,
        "columns": column_info,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_key_info
    })

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
for table in pdf_data:
    table_name = table["table_name"]
    columns = table["columns"]
    primary_keys = table["primary_keys"]
    foreign_keys = table["foreign_keys"]

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 10, txt=f"Table: {table_name}", ln=True, align='L')

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="  Columns:", ln=True, align='L')
    for col in columns:
        col_details = f"    - {col['name']} ({col['type']}), "
        col_details += f"NotNull: {'Yes' if col['notnull'] else 'No'}, "
        col_details += f"Default: {col['default_value']}, "
        col_details += f"Primary Key: {'Yes' if col['pk'] else 'No'}"
        pdf.cell(200, 10, txt=col_details, ln=True, align='L')

    if primary_keys:
        pdf.cell(200, 10, txt="  Primary Keys:", ln=True, align='L')
        for pk in primary_keys:
            pdf.cell(200, 10, txt=f"    - {pk}", ln=True, align='L')

    if foreign_keys:
        pdf.cell(200, 10, txt="  Foreign Keys:", ln=True, align='L')
        for fk in foreign_keys:
            fk_details = f"    - From: {fk['from']} To: {fk['to']} (Table: {fk['table']}), "
            fk_details += f"On Update: {fk['on_update']}, On Delete: {fk['on_delete']}, Match: {fk['match']}"
            pdf.cell(200, 10, txt=fk_details, ln=True, align='L')

# Save PDF to file
pdf_output_path = "./db_tables_and_columns_with_keys.pdf"  # Update this path to where you want to save the PDF
pdf.output(pdf_output_path)

print(f"PDF created: {pdf_output_path}")
