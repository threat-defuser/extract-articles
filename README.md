[![test status](https://github.com/threat-defuser/extract-articles/workflows/Test/badge.svg)](https://github.com/threat-defuser/extract-articles/actions)


# extract-articles

Code and scripts to extract data and populate the (example) database.


## Generating list of URLs

```console
$ python collect-urls.py --help

Usage: collect-urls.py [OPTIONS]

Options:
  --sites TEXT     The YML file describing the sites. This file is only read.
  --out-file TEXT  The generated output CSV file.
  --help           Show this message and exit.
```

Example:
```console
$ python collect-urls.py --sites sites.yml --out-file urls.csv
```


## Processing list of URLs

```console
$ python process-urls.py --help

Usage: process-urls.py [OPTIONS]

Options:
  --csv-file TEXT  The input CSV file containing list of URLs to process.
  --db-file TEXT   The SQLite database file.
  --help           Show this message and exit.
```

Example:
```console
$ python process-urls.py --csv-file urls.csv --db-file articles.db
```
