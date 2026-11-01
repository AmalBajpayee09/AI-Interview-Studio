# Safe SQL practice

Launch AI Interview Studio browser companion or native UI and choose **SQL lab**. Queries run against a short, deterministic SQLite fixture consisting of `departments`, `employees` and `sales`. This is not your personal/production database. Example:

```sql
SELECT e.name, SUM(s.amount) AS revenue
FROM employees e JOIN sales s ON e.id=s.employee_id
GROUP BY e.id ORDER BY revenue DESC;
```

Backend endpoints: `GET /api/sql/schema`; `POST /api/sql/query` with `{ "query": "SELECT * FROM employees", "max_rows": 100 }`.

**Security:** Each query uses a fresh in-memory DB, initialized before setting read-only `PRAGMA query_only`. The SQLite authorizer denies writes and privileged operations; dangerous functions are denied. A progress handler cancels long-running queries; returned rows, columns and string lengths are capped. This mechanism does not isolate arbitrary extensions or native code; extension loading is never enabled. Never reuse it to execute untrusted commands against a production database.

**Testing:** joins, read-only enforcement, timeouts, output limits, Unicode and SQL schema endpoint are tested in `services/ai_worker/tests/test_upgrade.py`.
