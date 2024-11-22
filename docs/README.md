# User Guide

## Dependencies

To install the dependencies, run:

```bash
sudo apt-get install texlive-base texlive-latex-recommended texlive-latex-extra texlive-science texlive-font-utils texlive-lang-spanish texlive-publishers texlive-pictures abntex biber
```

## Building the user guide

To generate the user guide, run:

```bash
make build
```

To remove intermediate files and clean up the directory, run:

```bash
make cleanup
```
