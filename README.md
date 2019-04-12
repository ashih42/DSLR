# DSLR
Predict the [Hogwarts House](https://harrypotter.fandom.com/wiki/Hogwarts_Houses) from a student's **academic scores** by implementing [Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression) in Python. (42 Silicon Valley)

<p float="left">
  <img src="https://github.com/ashih42/DSLR/blob/master/Screenshots/histogram.png" width="280" />
  <img src="https://github.com/ashih42/DSLR/blob/master/Screenshots/scatterplot.png" width="280" />
  <img src="https://github.com/ashih42/DSLR/blob/master/Screenshots/bad_features.png" width="200" />
</p>

In addition, I include student's **name, birth date, etc.** as relevant features, for perhaps the [Sorting Hat](https://harrypotter.fandom.com/wiki/Sorting_Hat) works in amazingly superstitious ways...

## Prerequisites

You have `python3` installed.

## Installing

```
./setup/setup.sh
```

## Running

### Describing Data
```
python3 describe.py data.csv
```

### Histograms
```
python3 histogram.py data.csv
```

### Scatter Plots
```
python3 scatter_plot.py data.csv
```

### Scatter Plot Matrix
```
python3 pair_plot.py data.csv
```

### Training
```
python3 train.py data.csv
```
* Export environment variable `DSLR_VERBOSE`=`TRUE` to enable verbose logging.

### Predicting
```
python3 predict.py data.csv weights.dat
```
