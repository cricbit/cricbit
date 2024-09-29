# Cricket Data Management System

## Project Overview

This project is a Cricket Data Management System designed to handle cricket match data from Cricsheet. It provides a robust backend infrastructure for storing, retrieving, and managing cricket match information.

## Data Source

The data for this project is sourced from [Cricsheet](https://cricsheet.org/), a website that provides ball-by-ball data for international and T20 league cricket matches in a machine-readable format.

### Cricsheet License

Cricsheet data is available under a [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/). This means you are free to use, modify, and distribute the data, provided you give appropriate credit and share any derivative works under the same license.

## Models

The system uses the following main models to represent cricket data:

1. **RawMatch**: Stores the raw JSON data for each match.
2. **MatchDetails**: Contains processed match information such as teams, dates, and venue.
3. **PlayingXI**: Represents the playing eleven for each team in a match.

These models are defined in the `domains` folder:

- `raw_matches.py`: Defines the RawMatch model
- `match_details.py`: Defines the MatchDetails model
- `playing_xi.py`: Defines the PlayingXI model

## Data Ingestion

To ingest new data into the system:

1. Prepare the Cricsheet data URL. For example:

   ```
   https://cricsheet.org/downloads/ipl_json.zip
   ```

2. Run the ingestion script:

   ```
   python ingestion.py --url https://cricsheet.org/downloads/ipl_json.zip
   ```

   This will download the ZIP file, extract the JSON files, and ingest them into the database.

3. The script will process each JSON file and populate the RawMatch, MatchDetails, and PlayingXI models accordingly.
