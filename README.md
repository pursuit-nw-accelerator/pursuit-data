# Data analysis pipeline

## Setting up
1. install node dependencies: `npm install`
1. TODO: install python dependencies using `conda` and `environment.yml`
1. Make sure the empty directories `codetrack/` and `csv/` are placed inside the `datalake` directory.
1. Create a json file of your class roster and save to `rosters/roster.json`. Use the example file `rosters/roster.example.json` as a template. The fields `id` (codetrack id), `email`, `name`, and `cohort` must be present.


## Getting the initial data
The goal here is to get all the past Codetrack data for your class so you can catch up.
1. Run `node getInitialData.js` to generate the JSON files of Codetrack progress. These are pulled from the Codetrack API. This script will capture all past data for your learners.

## Adding new data
After there is new weekly data in Codetrack (I think this is on Mondays), run `node getWeeklyStats.js` to get this data.

## Transferring data to the data lake
1. After adding, run `python datalake/main.py` to package the data into the parquet file format. (This is a column oriented format that doesn't take up a lot of space and is meant to be queried more quickly)
1. TODO: Manually delete the csv files you've packaged into parquet. TODO: make the deletion part of the script
1. You can now launch the notebook: `jupyter lab`. This will open the interactive Jupyter lab notebook in your browser. You can open the `analysis.ipynb` file and run analysis on the latest data.