import sqlite3
import time

def create_table(conn):
    while True:
        # Get table name
        table_name = input("Enter table name: ").strip()
        if not table_name:
            print("❌ Table name cannot be empty.")
            continue

        # Check if table already exists
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        exists = cursor.fetchone() is not None

        if exists:
            print(f"⚠️ Table '{table_name}' already exists.")
            # Ask user what to do
            while True:
                choice = input(
                    "Do you want to:\n"
                    "1. Create a different table\n"
                    "2. Skip this task\n"
                    "3. Quit\n"
                    "Enter 1, 2, or 3: "
                ).strip()
                if choice == '1':
                    # Go back to ask for new table name
                    break   
                elif choice == '2':
                    print("Skipping table creation.")
                    return
                elif choice == '3':
                    print("Exiting table creation.")
                    return
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            continue
        else:
            break

    # Get number of columns
    while True:
        try:
            num_cols = int(input("How many columns? "))
            if num_cols > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Enter a number.")

    # Collect column definitions
    columns = []  # will store tuples (name, dtype, is_pk)
    for i in range(num_cols):
        print(f"\nColumn {i+1}:")
        name = input("  Name: ").strip()
        dtype = input("  Type (TEXT/INTEGER/REAL): ").strip().upper()
        pk = input("  Primary key? (y/n): ").strip().lower()
        is_pk = (pk == 'y')
        columns.append((name, dtype, is_pk))

    # Build CREATE TABLE SQL
    col_defs = []
    for name, dtype, is_pk in columns:
        def_str = f"{name} {dtype}"
        if is_pk:
            def_str += " PRIMARY KEY"
        col_defs.append(def_str)

    sql = f"CREATE TABLE IF NOT EXISTS {table_name} (" + ", ".join(col_defs) + ")"

    # Execute
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print(f"✅ Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"❌ Error creating table: {e}")

def insert_data(conn):
    while True:
        print("\n" + "=" * 50)
        print("➕ INSERT OPERATION")
        print("=" * 50)

        while True:
            table_name = input("📋 Enter table name to insert into (or 'exit' to quit): ").strip()
            if table_name.lower() == 'exit':
                print("👋 Exiting insert function.")
                return
            if not table_name:
                print("❌ Table name cannot be empty. Please enter a valid name.")
                continue

            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if not cursor.fetchone():
                print(f"❌ Table '{table_name}' does not exist. Check the name and try again.")
            else:
                print(f"✅ Table '{table_name}' found.")
                break

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        col_names = [col[1] for col in columns_info]
        print(f"\n📌 Columns in '{table_name}': {', '.join(col_names)}")

        rows = []
        row_num = 1
        while True:
            print(f"\n{'─' * 40}")
            print(f"🆕 ROW {row_num}")
            print(f"{'─' * 40}")
            row_values = []
            for col in col_names:
                value = input(f"   {col}: ").strip()
                row_values.append(value)

            print(f"\n📝 Your entry: {row_values}")
            confirm = input("✅ Add this row to the database? (y/n): ").strip().lower()
            if confirm == 'y':
                rows.append(row_values)
                print(f"   Row {row_num} added.")
                row_num += 1
            else:
                print("   Row discarded.")

            cont = input("➕ Add another row? (y/n): ").strip().lower()
            if cont != 'y':
                break

        if rows:
            placeholders = ','.join(['?'] * len(col_names))
            sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            try:
                cursor.executemany(sql, rows)
                conn.commit()
                print(f"\n✅ Successfully inserted {len(rows)} row(s) into '{table_name}'.")
            except sqlite3.Error as e:
                print(f"❌ Database error while inserting: {e}")
        else:
            print("ℹ️  No rows were inserted.")

        another = input("\n📁 Do you want to insert into another table? (y/n): ").strip().lower()
        if another != 'y':
            break

    print("👋 Exiting insert function. Back to main menu.")

    
def update_data(conn):
    while True:   # Outer loop – allows switching tables
        # --- Step 1: Table selection ---
        while True:
            print("\n" + "="*50)
            table_name = input("📋 Enter the name of the table you want to update (or type 'exit' to quit): ").strip()
            if table_name.lower() == 'exit':
                print("👋 Exiting update function. Back to main menu.")
                return
            if not table_name:
                print("❌ Table name cannot be empty. Please enter a valid name.")
                continue

            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if not cursor.fetchone():
                print(f"❌ Table '{table_name}' does not exist. Check the name and try again.")
            else:
                print(f"✅ Table '{table_name}' found.")
                break   # table exists

        # --- Step 2: Get column info ---
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        col_names = [col[1] for col in columns_info]
        print(f"\n📌 Columns in '{table_name}': {', '.join(col_names)}")

        # --- Step 3: Inner loop for multiple updates on this table ---
        while True:
            print("\n" + "─"*40)
            print("🔄 NEW UPDATE OPERATION")
            print("─"*40)
            
            # ---- Choose column to update ----
            while True:
                col = input("✏️  Which column do you want to change? ").strip()
                if col not in col_names:
                    print(f"❌ Column '{col}' is not in the table. Please choose from: {', '.join(col_names)}")
                else:
                    break
            
            # ---- New value ----
            new_value = input(f"🔢 Enter the new value for '{col}': ").strip()
            # (You can add type validation later)

            # ---- WHERE condition (optional) ----
            use_where = input("🎯 Do you want to update only specific rows? (y/n): ").strip().lower()
            where_clause = ""
            where_value = None

            if use_where == 'y':
                print("\nLet's build the condition to select which rows to update.")
                print(f"Available columns: {', '.join(col_names)}")
                
                # Column for condition
                while True:
                    where_col = input("   Column name (e.g., 'ID'): ").strip()
                    if where_col not in col_names:
                        print(f"❌ Column '{where_col}' doesn't exist. Try again.")
                    else:
                        break
                
                # Operator
                operator = input("   Operator (=, >, <, >=, <=, !=): ").strip()
                if operator not in ['=', '>', '<', '>=', '<=', '!=']:
                    print("⚠️  Invalid operator. Using '='.")
                    operator = '='
                
                # Value
                where_val = input("   Value to match: ").strip()
                
                # Show full condition and confirm
                print(f"\n📐 Your condition: {where_col} {operator} {where_val}")
                confirm_cond = input("Is this correct? (y/n): ").strip().lower()
                if confirm_cond == 'y':
                    where_clause = f"WHERE {where_col} {operator} ?"
                    where_value = where_val
                else:
                    print("Condition discarded. The update will apply to ALL rows.")
                    # No WHERE clause
            else:
                # No WHERE – warn about updating all rows
                print("\n⚠️  WARNING: You are about to update ALL rows in this table.")
                confirm_all = input("Are you absolutely sure? (y/n): ").strip().lower()
                if confirm_all != 'y':
                    print("Update cancelled.")
                    # Ask if they want another update on same table
                    again = input("Do you want to perform another update on this table? (y/n): ").strip().lower()
                    if again != 'y':
                        break
                    else:
                        continue
                # else, proceed with no WHERE

            # ---- Build and execute the UPDATE ----
            sql = f"UPDATE {table_name} SET {col} = ? {where_clause}"
            params = [new_value]
            if where_value is not None:
                params.append(where_value)

            try:
                cursor.execute(sql, params)
                conn.commit()
                print(f"✅ Success! {cursor.rowcount} row(s) updated.")
            except sqlite3.Error as e:
                print(f"❌ Database error: {e}")

            # ---- Ask if they want another update on the same table ----
            again = input("\n🔄 Do you want to perform another update on this table? (y/n): ").strip().lower()
            if again != 'y':
                break   # exit inner loop

        # ---- After finishing updates on this table, ask if they want to update a different table ----
        another_table = input("\n📁 Do you want to update a different table? (y/n): ").strip().lower()
        if another_table != 'y':
            break   # exit outer loop

    print("👋 Exiting update function. Back to main menu.")
    
def delete_data(conn):
    while True: 
        while True:
            print("\n" + "="*50)
            table_name = input("🗑️  Enter table name to delete from (or 'exit' to quit): ").strip()
            if table_name.lower() == 'exit':
                print("👋 Exiting delete function.")
                return
            if not table_name:
                print("❌ Table name cannot be empty.")
                continue

            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if not cursor.fetchone():
                print(f"❌ Table '{table_name}' does not exist.")
            else:
                print(f"✅ Table '{table_name}' found.")
                break
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        col_names = [col[1] for col in columns_info]
        print(f"\n📌 Columns: {', '.join(col_names)}")

        while True:
            print("\n" + "─"*40)
            print("🗑️  NEW DELETE OPERATION")
            print("─"*40)

            # --- Build WHERE condition (optional) ---
            use_where = input("🎯 Do you want to delete only specific rows? (y/n): ").strip().lower()
            where_clause = ""
            where_value = None

            if use_where == 'y':
                print("\nLet's build the condition to select which rows to delete.")
                # Column for condition
                while True:
                    where_col = input("   Column name (e.g., 'ID'): ").strip()
                    if where_col not in col_names:
                        print(f"❌ Column '{where_col}' doesn't exist. Try again.")
                    else:
                        break
                # Operator
                operator = input("   Operator (=, >, <, >=, <=, !=): ").strip()
                if operator not in ['=', '>', '<', '>=', '<=', '!=']:
                    print("⚠️  Invalid operator. Using '='.")
                    operator = '='
                # Value
                where_val = input("   Value to match: ").strip()
                # Confirm condition
                print(f"\n📐 Your condition: {where_col} {operator} {where_val}")
                confirm_cond = input("Is this correct? (y/n): ").strip().lower()
                if confirm_cond == 'y':
                    where_clause = f"WHERE {where_col} {operator} ?"
                    where_value = where_val
                else:
                    print("Condition discarded. The delete will apply to ALL rows (with confirmation).")
                    # Fall through to all‑rows warning
                    use_where = 'n'   # treat as no WHERE

            if use_where != 'y':
                # No WHERE – warn about deleting all rows
                print("\n⚠️  WARNING: You are about to delete ALL rows from this table.")
                confirm_all = input("Are you absolutely sure? (y/n): ").strip().lower()
                if confirm_all != 'y':
                    print("Delete cancelled.")
                    # Ask if they want another delete on same table
                    again = input("Do you want to perform another delete on this table? (y/n): ").strip().lower()
                    if again != 'y':
                        break
                    else:
                        continue
                # else proceed with no WHERE (delete all)

            # --- Build and execute DELETE ---
            sql = f"DELETE FROM {table_name} {where_clause}"
            params = [where_value] if where_value is not None else []

            try:
                cursor.execute(sql, params)
                conn.commit()
                print(f"✅ Success! {cursor.rowcount} row(s) deleted.")
            except sqlite3.Error as e:
                print(f"❌ Database error: {e}")

            # --- Ask if they want another delete on same table ---
            again = input("\n🔄 Do you want to perform another delete on this table? (y/n): ").strip().lower()
            if again != 'y':
                break

        # --- Ask if they want to delete from another table ---
        another_table = input("\n📁 Do you want to delete from a different table? (y/n): ").strip().lower()
        if another_table != 'y':
            break

    print("👋 Exiting delete function.")

def select_data(conn):
    """
    Interactive query tool for SQLite databases.
    Allows selecting specific columns, filtering with WHERE,
    joining another table, grouping with aggregate functions,
    and ordering results.
    """
    while True:
        # 1. Get and validate table name
        while True:
            print("\n" + "=" * 50)
            table_name = input("📊 Enter table name to query (or 'exit' to quit): ").strip()
            if table_name.lower() == 'exit':
                print("👋 Exiting select function.")
                return
            if not table_name:
                print("❌ Table name cannot be empty.")
                continue

            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if not cursor.fetchone():
                print(f"❌ Table '{table_name}' does not exist.")
            else:
                print(f"✅ Table '{table_name}' found.")
                break

        # 2. Get column information (for validation and display)

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        col_names = [col[1] for col in columns_info]
        print(f"\n📌 Columns in '{table_name}': {', '.join(col_names)}")

        # 3. Column selection (optional)
        select_columns = "*"  # default: all columns
        choose_cols = input("\nDo you want to select specific columns? (y/n): ").strip().lower()
        if choose_cols == 'y':
            while True:
                cols_input = input("Enter column names (comma‑separated): ").strip()
                if not cols_input:
                    print("❌ No columns entered.")
                    continue
                # Split by comma and clean each name
                selected = [c.strip() for c in cols_input.split(',')]
                # Validate each column exists in the table
                invalid = [c for c in selected if c not in col_names]
                if invalid:
                    print(f"❌ Invalid column(s): {', '.join(invalid)}")
                else:
                    select_columns = ', '.join(selected)
                    break

        # 4. JOIN clause (optional) – simplified: one join, INNER/LEFT

        join_clause = ""
        use_join = input("\n🔗 Do you want to join another table? (y/n): ").strip().lower()
        if use_join == 'y':
            # Get second table name
            while True:
                join_table = input("   Enter name of table to join: ").strip()
                if not join_table:
                    print("❌ Table name cannot be empty.")
                    continue
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (join_table,)
                )
                if not cursor.fetchone():
                    print(f"❌ Table '{join_table}' does not exist.")
                else:
                    break

            # Get join type
            join_type = input("   Join type (INNER or LEFT): ").strip().upper()
            if join_type not in ['INNER', 'LEFT']:
                print("⚠️  Invalid type. Using INNER.")
                join_type = 'INNER'

            # Get column info for the second table (to validate join columns)
            cursor.execute(f"PRAGMA table_info({join_table})")
            join_columns_info = cursor.fetchall()
            join_col_names = [col[1] for col in join_columns_info]
            print(f"   Columns in '{join_table}': {', '.join(join_col_names)}")

            # Get join condition: left table column
            while True:
                left_col = input(f"   Column from '{table_name}' to join on: ").strip()
                if left_col not in col_names:
                    print(f"❌ Column '{left_col}' does not exist in '{table_name}'. Try again.")
                else:
                    break
            # Get right table column
            while True:
                right_col = input(f"   Column from '{join_table}' to join on: ").strip()
                if right_col not in join_col_names:
                    print(f"❌ Column '{right_col}' does not exist in '{join_table}'. Try again.")
                else:
                    break

            # Build the JOIN clause
            join_clause = f"{join_type} JOIN {join_table} ON {table_name}.{left_col} = {join_table}.{right_col}"
            print(f"✅ JOIN clause: {join_clause}")

#join clause is with limitations.

        # 5. WHERE clause (optional) – as before
        
        where_clause = ""
        where_value = None
        use_where = input("\n🎯 Do you want to filter rows with a WHERE condition? (y/n): ").strip().lower()
        if use_where == 'y':
            print("\nLet's build the WHERE condition.")
            # Column for condition
            while True:
                where_col = input("   Column name: ").strip()
                if where_col not in col_names:
                    print(f"❌ Column '{where_col}' doesn't exist. Try again.")
                else:
                    break
            # Operator
            operator = input("   Operator (=, >, <, >=, <=, !=): ").strip()
            if operator not in ['=', '>', '<', '>=', '<=', '!=']:
                print("⚠️  Invalid operator. Using '='.")
                operator = '='
            # Value
            where_val = input("   Value to match: ").strip()
            # Confirm condition
            print(f"\n📐 Your condition: {where_col} {operator} {where_val}")
            if input("Is this correct? (y/n): ").strip().lower() == 'y':
                where_clause = f"WHERE {where_col} {operator} ?"
                where_value = where_val
            else:
                print("Condition discarded. Querying all rows.")

        # 6. GROUP BY clause (optional) – allows single column grouping with aggregates
        group_by_clause = ""
        use_group = input("\n📊 Do you want to group rows (GROUP BY)? (y/n): ").strip().lower()
        if use_group == 'y':
            # Choose grouping column
            while True:
                group_col = input("   Column to group by: ").strip()
                if group_col not in col_names:
                    print(f"❌ Column '{group_col}' does not exist. Try again.")
                else:
                    break

            # Choose aggregate functions (multiple allowed, comma‑separated)
            print("\n   Available aggregate functions:")
            print("     1. COUNT(*)")
            print("     2. SUM(column)")
            print("     3. AVG(column)")
            print("     4. MAX(column)")
            print("     5. MIN(column)")
            agg_input = input("   Enter numbers of functions to include (e.g., 1,3): ").strip()
            # Parse choices
            choices = [c.strip() for c in agg_input.split(',') if c.strip().isdigit()]
            agg_funcs = []
            for ch in choices:
                if ch == '1':
                    agg_funcs.append("COUNT(*)")
                elif ch == '2':
                    col = input("      Column for SUM: ").strip()
                    if col in col_names:
                        agg_funcs.append(f"SUM({col})")
                    else:
                        print(f"⚠️ Column '{col}' invalid. Skipping SUM.")
                elif ch == '3':
                    col = input("      Column for AVG: ").strip()
                    if col in col_names:
                        agg_funcs.append(f"AVG({col})")
                    else:
                        print(f"⚠️ Column '{col}' invalid. Skipping AVG.")
                elif ch == '4':
                    col = input("      Column for MAX: ").strip()
                    if col in col_names:
                        agg_funcs.append(f"MAX({col})")
                    else:
                        print(f"⚠️ Column '{col}' invalid. Skipping MAX.")
                elif ch == '5':
                    col = input("      Column for MIN: ").strip()
                    if col in col_names:
                        agg_funcs.append(f"MIN({col})")
                    else:
                        print(f"⚠️ Column '{col}' invalid. Skipping MIN.")
            if agg_funcs:
                select_expressions = f"{group_col}, " + ", ".join(agg_funcs)
                select_columns = select_expressions
                group_by_clause = f"GROUP BY {group_col}"
            else:
                print("⚠️ No valid aggregate functions selected. GROUP BY cancelled.")
                use_group = 'n'

        # 7. ORDER BY clause (optional) – as before
        order_clause = ""
        use_order = input("\n🔤 Do you want to order the results? (y/n): ").strip().lower()
        if use_order == 'y':
            while True:
                order_col = input("   Column name to order by: ").strip()
                if order_col not in col_names:
                    print(f"❌ Column '{order_col}' doesn't exist. Try again.")
                else:
                    break
            order_dir = input("   Direction (ASC or DESC): ").strip().upper()
            if order_dir not in ['ASC', 'DESC']:
                print("⚠️  Invalid direction. Using ASC.")
                order_dir = 'ASC'
            order_clause = f"ORDER BY {order_col} {order_dir}"

        # 8. Build and execute the final SQL
        sql = f"SELECT {select_columns} FROM {table_name} {join_clause} {where_clause} {group_by_clause} {order_clause}"
        # Parameters are only needed for WHERE (and possibly HAVING in the future)
        params = [where_value] if where_value is not None else []

        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            if not rows:
                print("ℹ️  No rows found.")
            else:
                if select_columns == '*':
                    headers = col_names
                else:
                    headers = [h.strip() for h in select_columns.split(',')]

                # Use tabulate if available, otherwise a simple print
                try:
                    from tabulate import tabulate
                    print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))
                except ImportError:
                    # Fallback formatting
                    print("\n" + "-" * 60)
                    print(" | ".join(headers))
                    print("-" * 60)
                    for row in rows:
                        print(" | ".join(str(val) for val in row))
                    print("-" * 60)
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")

        another_table = input("\n📁 Do you want to query a different table? (y/n): ").strip().lower()
        if another_table != 'y':
            break

    print("👋 Exiting select function.")


