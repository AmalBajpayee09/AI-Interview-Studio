"""Self-contained read-only SQLite practice dataset. Never connects to user databases.

SQLite authorizer restricts the grammar, a time budget stops runaway recursive
CTEs, and limits cap rows, columns and response size. Not an OS process sandbox.
"""
from __future__ import annotations
import sqlite3
import time

SCHEMA = '''
CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
 department_id INTEGER, salary INTEGER NOT NULL, hired TEXT NOT NULL,
 FOREIGN KEY (department_id) REFERENCES departments(id));
CREATE TABLE sales (id INTEGER PRIMARY KEY, employee_id INTEGER NOT NULL,
 amount INTEGER NOT NULL, sold_at TEXT NOT NULL,
 FOREIGN KEY(employee_id) REFERENCES employees(id));
INSERT INTO departments VALUES (1,'Engineering'), (2,'Sales'), (3,'Design');
INSERT INTO employees VALUES
 (1,'Asha',1,95000,'2022-01-10'),(2,'Ravi',1,85000,'2023-03-14'),
 (3,'Meera',2,72000,'2021-07-01'),(4,'John',2,68000,'2024-02-02'),
 (5,'Tara',3,77000,'2023-08-19'),(6,'Omar',NULL,62000,'2024-09-20');
INSERT INTO sales VALUES
 (1,3,12000,'2025-01-10'),(2,3,9000,'2025-01-20'),
 (3,4,16000,'2025-02-01'),(4,3,7000,'2025-02-11'),
 (5,4,8000,'2025-02-15');
'''

SCHEMA_GUIDE = [
 {'table':'departments','columns':['id INTEGER PRIMARY KEY','name TEXT NOT NULL']},
 {'table':'employees','columns':['id INTEGER PRIMARY KEY','name TEXT','department_id INTEGER (nullable)','salary INTEGER','hired TEXT (ISO date)']},
 {'table':'sales','columns':['id INTEGER PRIMARY KEY','employee_id INTEGER','amount INTEGER','sold_at TEXT (ISO date)']}
]

class SQLPracticeError(ValueError):
    pass


def execute_readonly(query: str, max_rows: int = 100, timeout_ms: int = 300) -> dict:
    if not isinstance(query, str) or not query.strip() or len(query) > 10000:
        raise SQLPracticeError('Query must contain 1–10,000 characters')
    if not 1 <= max_rows <= 100:
        raise SQLPracticeError('max_rows must be between 1 and 100')
    # SELECT and WITH (including recursive CTEs) are admitted only after SQLite
    # authorizer verification. The prefix check is for helpful error messages.
    if query.lstrip().split(None,1)[0].upper() not in ('SELECT','WITH'):
        raise SQLPracticeError('Only read-only SELECT and WITH queries are permitted')
    start = time.perf_counter()
    con = sqlite3.connect(':memory:', timeout=0.1)
    try:
        con.executescript(SCHEMA)
        con.execute('PRAGMA query_only=ON')
        con.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 500000)
        con.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 10000)
        con.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 30)
        # Do not permit SQL to install extensions, open external files, create
        # virtual tables, change pragmas, or mutate the dataset.
        allowed={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION}
        for symbolic in ('SQLITE_RECURSIVE',):
            if hasattr(sqlite3,symbolic): allowed.add(getattr(sqlite3,symbolic))
        forbidden_functions={'load_extension','randomblob','zeroblob','writefile','readfile'}
        def authorizer(action,p1,p2,db_name,trigger):
            if action == sqlite3.SQLITE_FUNCTION and (p2 or p1 or '').lower() in forbidden_functions:
                return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY
        con.set_authorizer(authorizer)
        deadline=start+timeout_ms/1000
        con.set_progress_handler(lambda: 1 if time.perf_counter() >= deadline else 0, 500)
        try:
            cursor=con.execute(query)
            columns=[d[0] for d in cursor.description or []]
            if not columns: raise SQLPracticeError('Expected a query returning a result set')
            records=cursor.fetchmany(max_rows+1)
        except sqlite3.Error as exc:
            if time.perf_counter() >= deadline or 'interrupted' in str(exc).lower():
                raise SQLPracticeError('Query exceeded the practice time limit') from exc
            raise SQLPracticeError(f'SQL query rejected: {exc}') from exc
        result=[]
        for record in records[:max_rows]:
            result.append([v[:1000] if isinstance(v,str) else v for v in record])
        return {'columns':columns,'rows':result,'row_count':len(result),
                'truncated':len(records)>max_rows,
                'elapsed_ms':round((time.perf_counter()-start)*1000,2),
                'dataset':'Built-in training dataset (no user database access)',
                'verified':'Executed against the bundled SQLite practice data'}
    finally:
        con.close()
