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
-h, --help           Show the help message and exit
-H, --host           the database host
-P, --port           the database port
-u, --user           the database user name
-p, --password       the database user password
-S, --schema         the database schema for which the view should be exported
-o, --out            the path to the output file where the export should be written to
-f, --filter         a filter condition to select only specific views. Views for import are selected 
                     from information_schema.views. Columns from this table/view can be used in the
                     filter condition
--exclude-algorithm  exclude view algorithm from export
--exclude-definer    exclude view definer from export
```
