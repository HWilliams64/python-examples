import sqlite3

TABLE_NAME = "records"
DB_NAME = "accounting.sqlite"


def table_exists(conn: sqlite3.Connection) -> bool:
    """
    Creates a DB table that will hold the financial records.

    Args:
        conn (sqlite3.Connection): A database connection

    Returns:
        bool: True if the table exists. False otherwise.
    """

    global TABLE_NAME

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",
        (TABLE_NAME,),
    )
    return bool(cursor.fetchone())


def create_table(conn: sqlite3.Connection):
    """
    Creates the records table

    Args:
        conn (sqlite3.Connection): A database connection
    """

    global TABLE_NAME

    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            type TEXT,
            amount REAL,
            note TEXT
        )
    """
    )


def list_records(conn: sqlite3.Connection):
    """List the records in the DB

    Args:
        conn (sqlite3.Connection): A database connection
    """

    num = ""

    while not num.isdigit():
        num = input(
            "Please enter a number of records in past you'd like to list (Press ENTER"
            " default 10): "
        ).strip()

        num = num or "10"

    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT id, type, amount, note FROM {TABLE_NAME} ORDER BY id ASC LIMIT {num}
        """
    )

    results = cursor.fetchall()

    if not len(results):
        print("There are no records.")
    else:
        for row in results:
            print(
                f'[{row["id"]}] {row["type"]} ${row["amount"]} for'
                f' {row["note"].lower()}'
            )


def add_record(conn: sqlite3.Connection):
    """Adds a record to the DB

    Args:
        conn (sqlite3.Connection): A database connection
    """

    def _input_type():
        v = input("Specify the record's type (debit/credit): ").strip().lower()

        if v not in ("debit", "credit"):
            print(f"The type {v} is not recognized. Try again.")
            return _input_type()

        return v

    def _input_amount():
        v = input("Specify the dollar amount: ").strip().lower().replace("$", "")

        if not v.replace(".", "").isdigit():
            print(f"The number {v} is not recognized. Try again.")
            return _input_amount()

        return v

    r_type = _input_type()
    r_amount = _input_amount()
    r_note = input(
        "Please specify a description of the record (Press ENTER to skip):\n"
    )

    cursor = conn.cursor()
    cursor.execute(
        f"""
        INSERT INTO {TABLE_NAME} (type, amount, note) values (?, ?, ?)
        """,
        (r_type, r_amount, r_note),
    )


def create_table(conn: sqlite3.Connection):
    """
    Creates the records table

    Args:
        conn (sqlite3.Connection): A database connection
    """

    global TABLE_NAME

    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            type TEXT,
            amount REAL,
            note TEXT
        )
    """
    )


def remove_record(conn: sqlite3.Connection):
    """Removes a specific record from the DB

    Args:
        conn (sqlite3.Connection): A database connection
    """

    r_id = ""

    while not r_id.isdigit():
        r_id = input(
            "Enter the record ID of the record you'd like to remove (Press ENTER go"
            " back): "
        ).strip()

        if not len(r_id):
            return

    cursor = conn.cursor()
    cursor.execute(
        f"""
        DELETE FROM {TABLE_NAME}
        WHERE id = {r_id}
        """
    )


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


if __name__ == "__main__":
    try:
        with sqlite3.connect(
            DB_NAME,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=False,
        ) as conn:

            conn.row_factory = dict_factory

            if not table_exists(conn):
                create_table(conn)

            while True:
                print()
                print("Please type a command:")
                print("l - List records")
                print("a - Add a record")
                print("r - Remove a record")
                print("q - Quit")
                command = input()

                if command == "l":
                    list_records(conn)
                elif command == "a":
                    add_record(conn)
                elif command == "r":
                    remove_record(conn)
                elif command == "q":
                    break
                else:
                    print("Unknown command: %s" % command)
    except KeyboardInterrupt:
        pass
