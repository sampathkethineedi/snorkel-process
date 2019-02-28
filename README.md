# snorkel-process
Process flow to generate labels on Text data using Snorkel and maintain DB to repurpose unlabelled data

## Install Snorkel

Follow steps at https://github.com/HazyResearch/snorkel#installation to install Snorkel in environment

## Snorkel Process
**usage**: snorkel_process.py [-h] -p PATH -lf LF [-r]

```python snorkel_process.py -p 'cnbc_doc.tsv' -lf 'labeling_func' -r```

Run Snorkel process

optional arguments:

  -h, --help        show this help message and exit
  
  -p PATH, --path PATH        Path to TSV file
  
  -lf LF, --label_func LF       LF python file
  
  -r, --restart       flag to restart process from beginning

## DB process

**usage**: db_process.py [-h] -n NAME

```python db_process.py -n 'test_db_2'```

Run DB process

optional arguments:

  -h, --help            show this help message and exit
  
  -n NAME, --name NAME  DB name
