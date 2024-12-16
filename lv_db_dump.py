import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "lv"
DB_USER = "postgres"
DB_PASSWORD = "root"

# File path for the Excel file
EXCEL_FILE = r"C:\Users\Lenovo\Downloads\LV_Initial.xlsx"

# Map Excel headers to database columns
COLUMN_MAPPING = {
    "Code_name": "code",
    "MAIN-Category": "main_cat",
    "SUB-Category": "sub_cat",
    "BRAND": "brand",
    "Model number": "model",
    "Housing Size (mm)": "housing_size",
    "Function Specific": "function",
    "Range": "range",
    "Output": "output",
    "Supply Voltage": "voltage",
    "Connection": "connection",
    "Material": "material",
    "Images": "images",
    "PDF": "pdf"
}

# Read Excel data
def read_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        # Rename columns to match database column names
        df = df.rename(columns=COLUMN_MAPPING)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

# Insert data into the database
def insert_data_to_db(df, connection):
    try:
        # Convert DataFrame to list of tuples
        records = df.where(pd.notnull(df), None).to_dict("records")
        values = [
            (
                record.get("code"),
                record.get("main_cat"),
                record.get("sub_cat"),
                record.get("brand"),
                record.get("model"),
                record.get("housing_size"),
                record.get("function"),
                record.get("range"),
                record.get("output"),
                record.get("voltage"),
                record.get("connection"),
                record.get("material"),
                record.get("images"),
                record.get("pdf"),
            )
            for record in records
        ]

        # SQL Query to insert data
        insert_query = """
            INSERT INTO products (
                code, main_cat, sub_cat, brand, model, housing_size,
                function, range, output, voltage, connection, material, images, pdf
            )
            VALUES %s
        """

        # Insert data in bulk
        with connection.cursor() as cursor:
            execute_values(cursor, insert_query, values)
            connection.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()

# Main function
def main():
    # Read data from Excel
    df = read_excel(EXCEL_FILE)
    if df is None:
        return

    # Connect to the database
    try:
        connection = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        print("Database connection established.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return

    # Insert data into the database
    try:
        insert_data_to_db(df, connection)
    finally:
        connection.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
