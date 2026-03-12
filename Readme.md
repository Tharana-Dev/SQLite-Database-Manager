```markdown
# SQLite Database Manager

A user‑friendly command‑line tool for managing SQLite databases.  
Built with Python, this tool guides you through creating tables, inserting data, updating records, deleting rows, and running queries – all without writing a single line of SQL.

---

## ✨ Features

- **Create Table** – interactively define columns, data types, and primary keys.
- **Insert Data** – add rows one by one with column‑by‑column prompts and confirmation.
- **Update Data** – change values in specific columns, with optional `WHERE` condition.
- **Delete Data** – remove rows, with optional `WHERE` and a safety warning for mass deletion.
- **Select Data** – run queries with optional:
  - Column selection
  - `JOIN` (one additional table, `INNER` or `LEFT`)
  - `WHERE` filter
  - `GROUP BY` (single column) with aggregate functions (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`)
  - `ORDER BY`
- **Multi‑table sessions** – after finishing with one table, you can switch to another without restarting.
- **Forgiving task selection** – type any part of a task name (e.g., `"cre"` for `"Create Table"`) and the tool will match it.

---

## 📦 Requirements

- Python 3.6 or higher
- `sqlite3` (built into Python)
- Optional: `tabulate` for prettier table output  
  Install with: `pip install tabulate`

No other dependencies – just pure Python.

---

## 🚀 Installation & Setup

1. Clone or download this repository.
2. Navigate to the project folder.
3. Run the tool:
   ```bash
   python main.py
   ```

The tool will ask you for a database directory and name. You can use an existing database or create a new one – it will be created automatically.

---

## 🧭 How to Use Each Function

### 1. Create Table
- Prompts for table name.
- If the table already exists, you can create a different one, skip, or quit.
- Then asks for number of columns.
- For each column, you provide:
  - Column name
  - Data type (`TEXT`, `INTEGER`, `REAL`)
  - Whether it’s the primary key (`y`/`n`)
- The table is created with `IF NOT EXISTS` to avoid errors.

### 2. Insert Data
- Asks for table name (validated).
- Shows column names.
- For each row, you enter values column by column.
- After entering a row, you see the whole row and confirm whether to add it.
- You can add multiple rows in one session.
- After finishing, the tool inserts all rows in one batch.

### 3. Update Data
- Asks for table name.
- Shows columns.
- For each update operation:
  - Choose column to change.
  - Enter new value.
  - Optionally build a `WHERE` condition:
    - Choose a column, operator (`=`, `>`, `<`, `>=`, `<=`, `!=`), and a value.
    - You can confirm the condition before execution.
  - If no `WHERE`, you are warned before updating **all rows**.
- After execution, you see how many rows were affected.
- You can perform multiple updates on the same table, then move to another table.

### 4. Delete Data
- Very similar to update, but without a `SET` part.
- Asks for table name.
- Shows columns.
- For each delete operation:
  - Optionally build a `WHERE` condition (same guided process).
  - If no `WHERE`, you are warned before deleting **all rows**.
- Reports the number of deleted rows.
- Multiple deletions on the same table, then option to switch tables.

### 5. Select and Filter Data
- Asks for table name.
- Shows columns.
- Offers optional steps (each can be skipped):
  - **Select specific columns** – enter comma‑separated column names.
  - **JOIN another table** – choose second table, join type (`INNER`/`LEFT`), and the join condition columns.
  - **WHERE** – build a condition like in update/delete.
  - **GROUP BY** – choose a grouping column, then select one or more aggregate functions (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`).
  - **ORDER BY** – choose a column and direction (`ASC`/`DESC`).
- Executes the query and displays results.
  - If `tabulate` is installed, output is shown as a grid; otherwise a simple dashed‑line table.
- After seeing results, you can query another table or exit.

---

## ⚠️ Limitations

This tool is designed to be simple and educational. It has the following limitations:

- **No primary key uniqueness check** – you can insert duplicate primary key values; SQLite will raise an error.
- **No foreign key enforcement** – SQLite supports foreign keys, but this tool does not validate them.
- **Limited JOINs** – only one join is supported, and only with `INNER` or `LEFT` join types. The join condition must be a simple equality on one column from each table.
- **GROUP BY** – only one column can be used for grouping. Aggregate functions are limited to the five provided; you cannot use expressions or `HAVING`.
- **No `HAVING` clause** – you cannot filter groups after aggregation.
- **No `DISTINCT`** – you cannot select distinct rows.
- **No `LIMIT` or `OFFSET`** – result set size is not limited.
- **Basic type validation** – values are taken as strings; SQLite will attempt to convert them, but no pre‑validation is done.
- **No transaction rollback** – each operation is committed immediately; there is no multi‑step undo.
- **Column names must be unique within a table** – the tool does not check for duplicate column names.

These limitations keep the code manageable and are excellent starting points for future enhancements.

---

## 🙏 Acknowledgements

- Inspired by the need for a beginner‑friendly SQLite interface.
- Built with Python’s standard library – `sqlite3` and `pathlib`.
- Optional table formatting provided by `tabulate`.


Enjoy managing your databases with ease!  
If you encounter any issues or have ideas for improvements, feel free to contribute.

**Tharana** – March 2026