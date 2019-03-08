# snorkel-process
Process flow to generate labels on Text data using Snorkel and maintain DB to repurpose unlabelled data

## Install Snorkel

Follow steps at https://github.com/HazyResearch/snorkel#installation to install Snorkel in environment

## Snorkel Process
**usage**: snorkel_process.py [-h] -n NAME -p PATH -lf LF [-r]

```python snorkel_process.py -n 'cnbc_test' -p 'cnbc_doc.tsv' -lf 'labeling_func' -r```

Run Snorkel process

Arguments:

  -h, --help        show this help message and exit
  
  -n, --name NAME        Name of the process
  
  -p PATH, --path PATH        Path to TSV file
  
  -lf LF, --label_func LF       LF python file
  
  -r, --restart       flag to restart process from beginning
