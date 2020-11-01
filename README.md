Bug Hunter - AXM
==============================

Repository which includes the work for the first part of TAED-2, a course included in the Data Science &amp; Engineering degree at UPC. The software includes pre-trained models and prediction scripts to predict whether a commit is potentially fault-inducing or not, as well as the possibility to test it on real repositories using a simple CLI command.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.https://github.com/AlbertDominguez/AXM
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

## Replication

First of all, create a fresh anaconda environment using Python 3.8, activate it and clone the repository.

```{bash}
$ conda create --name bug-hunter python=3.8
$ conda activate bug-hunter
$ git clone https://github.com/AlbertDominguez/AXM.git
```

Once inside the repository, install the dependencies.

```{bash}
$ cd AXM
$ pip install -r requirements.txt
```

Note that the technical debt dataset must be downloaded from the [Technical Debt Dataset repository](https://github.com/clowee/The-Technical-Debt-Dataset) in the SQLite format in order to continue. Moreover, it must be placed inside the path `data/raw` with the name `technicalDebtDataset.db`.


The repository comes with some pre-trained models, including the final one (random forest). In order to replicate the training pipeline to get exactly the random forest model, a view must be created in the SQLite database. It can be done using Python's sqlite3 package or any DB manager, on our case we did it using DBeaver. The statement to create the view can be found in `src/data/view_definition.sql`. After the view is created, the preprocessed dataset can be created as a CSV with the following command:

```{bash}
$ cd src/data && python make_dataset.py && cd ../..
```

Once the dataset is ready, simply run the following training script. The confusion matrices for the train and validation data are written to the standard output to check the metrics, while the model is dumped to the `models` directory as *random_forest.joblib* file.

```{bash}
$ cd src/models && python train_model.py && cd ../..
```

In order to test the model with the commits of this repository, one can run

```{bash}
$ cd src/features && python commit_extraction.py && cd ../..
```

to generate a JSON file containing the features of the commits present in the repository. Then, on this output JSON, launch the inference pipeline as follows (replace the JSON file with the one generated by the previous script, which is by default dumped in th e `data/processed` folder):

```{bash}
$ cd src/models && python predict_model.py [JSON_OUTPUT_PATH] random_forest && cd ../..
```
which will display, in the standard output, whether every commit is fault-inducing or not.

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
