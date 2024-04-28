# Pursuit data pipeline

## Contents

- [About](#about)
- [Setting up](#setup)
- [Usage](#usage)

## <a id="about"></a> About 
The current goal of this project is to make it easier to see what's going on with your learners' Codetrack performance so that we can celebrate high achievers and reduce the time to detect fellows who are struggling or disengaging.

A secondary goal is to be a proof of concept for a more industry-standard way of handling data. That means that:

- all of the data that we might ever care about should be stored in a single place (not scattered across different Airtables and spreadsheets) 
- new data should be regularly moved to this single place
- the data should be stored in a way optimized for big data queries (compressed column-oriented storage)
- we should be able use this data for many uses including dashboards, reports, ML models, notifications, etc.

This repo contains scripts that puts class data into a single place where it can be queried using [Pyspark](https://spark.apache.org/docs/latest/api/python/reference/index.html) in a Python notebook. You can use this to get data about your learners into a single place and get insights on it.

At the moment there are many manual steps, only Codetrack data is pulled, and the data is kept on your local filesystem rather than in S3 or somewhere in the cloud. All of these shortcomings can be addressed over time.


## <a id="setup"></a>Setting up

### Setting up 1: Python environment

To set up the Python env for this project:
1. [Install Anaconda](https://docs.anaconda.com/free/anaconda/install/) and make sure this includes the `conda` CLI.
1. Navigate to the project root (where `environment.yml` lives)
1. Create the environment: `conda env create -f environment.yml`
1. This should create a new environment named `pursuit-data`.
1. Activate the environment: `conda activate pursuit-data`

[Go here](#envs) for more information on Python dependency management.

### Setting up 2: Roster data
Create a json file of your class roster and save to `rosters/roster.json`. Use the example file `rosters/roster.example.json` as a template. The fields `id` (codetrack id), `email`, `name`, and `cohort` must be present.

At the moment this is unforunately a manual process. I did this by copying my class guest list from Google calendar. That gets you a big comma-separated string which you can split into name and email address. That still leaves you having to look up codetrack ids and cohorts manually in Codetrack. Everyone's profile page has their codetrack user id in the URL.

### Setting up 3: Codetrack data
Create a `.env` file and set `API_URL=<codetrack back end api base URL>` with no trailing slashes. Contact me if you do not know the URL for the back end.

## <a id="usage"></a> Usage

### Ingesting data
[Go here](#pipeline) for more information on how the pipeline works.

When setting up your class for the first time, you can get the entire Codetrack history (of weekly scores) for your learners.
```
python codetrack_ingest_historical.py
```
Once that is done, you can run this script after new weekly data comes out (usually on Mondays). To avoid duplicating data, first make sure that the most recent weekly score will really be new data. You could check the Codetrack website to see if the progress graphs have updated or if a new week has started on the leaderboard.
```
python codetrack_ingest_weekly.py
```

### Data analysis
An example Jupyter notebook using Pyspark is in the root of the project: `analysis.ipynb`. This will give you the skeleton of how to set up a spark session and how to read the parquet data into a "data frame" (a table on steroids). There are many other things you can do with Spark and this data, I just don't know how to do it.

To launch the notebook, navigate to the project root and run this command: `jupyter lab`.

This will open the interactive Jupyter lab notebook in your browser. You can open the `analysis.ipynb` file and run analysis on the latest data.


### <a id="envs"></a> Python dependency management and troubleshooting

_Anaconda_

This project uses [Anaconda](https://docs.anaconda.com/free/anaconda/install/) to manage the dependencies ("packages") and version of Python used for the project. In my opinion Anaconda is a lot easier to set up and get up and running than alternatives like `pip`. Pip also doesn't have a concept of environments, which means when you install something it is globally installed and that will cause problems.

_Environments_

Dependency management in Python is different from the world of npm, usually in a more frustrating way. The general idea is that you will create an "environment" that has the dependencies that you need. You can "activate" that environment for your specific project. This project has a `environment.yml` file that defines all of the dependencies you'll need for this project's environment, including the version of Python. In that way, the `envrionment.yml` file is sort of like `package-lock.json`.

A conda environment is not exactly tied to a specific project repo. This is because unlike npm, which saves all dependencies in a `node_modules` directory **inside** your project, Anaconda installs all of your dependencies **outside** your project root (something like `~/opt/anaconda3/envs/<environment name>`). Activating an environment means taking over the `PATH` envvars and such so that when you type `python main.py`, your machine will run the version of python installed in the environment directory.

_Troubleshooting_

Because of this, you always have to remember to activate the right environment for your project. One of the most common problems is forgetting to do this and wondering why libraries and modules can't be found.

You can see the active environment by running `conda env list` in the terminal. There will be a `*` next to the active environment. You may also want to look up ways to add the active environment to your command line prompt.

If you use VS Code there is a related thing where you need to select the Python interpreter for the right environment, or else you'll get annoying squigglies.

### <a id="pipeline"></a> About the pipeline
These scripts pull data from the Codetrack API and save them in the [`.parquet` file format](https://parquet.apache.org/) (compressed columnar storage optimized for fast lookup). The data is partitioned inside the `codetrack/data` directory of your machine by year, month, and then cohort. This makes it faster to filter your data by those properties.

In between fetching data from the API and writing it to the parquet files, the data is converted to a table using the [PyArrow library](https://arrow.apache.org/docs/15.0/python/). Arrow tables are in-memory tables that are formatted similar to the parquet format (column-oriented) and the library has built-in methods for writing and partitioning parquet files from arrow tables.

Arrow tables are typed and expect all of your data to conform to the same schema of columns and data types. You can define the schema or let arrow infer it for you. Sometimes it doesn't infer exactly what you want, so you can tell it to recast the table to the schema that you want.

In general, putting data that follow the same schema into the same table and parquet file will make this experience sort of enjoyable. Trying to combine different schemas into a single dataset, or throwing lots of semi-structured or unstructured data together, will make you hate this.
