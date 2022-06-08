# MySQL View Export

This is a simple python 3 application to export database views from a schema in MySQL:


## Usage

```bash
python mysql-view-export.py -H mysql.example.com -P 3306 -u myuser -o dump.sql
```

**Arguments:**

All cli arguments are optional. The application will prompt for user input if any of the
parameters is missing

```text
-h, --help         Show the help message and exit
-H, --host         the database host
-P, --port         the database port
-u, --user         the database user name
-p, --password     the database user password
-o, --out          the path to the output file where the export should be written to
```
