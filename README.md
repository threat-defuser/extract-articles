# extract-data

Code and scripts to extract data and populate the (example) database.

- Status: experimental


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
$ python collect-urls.py --sites sites.yml --out-file generated.csv
```
