# IMDb Series Scraper

IMDb Series Scraper is a Python script designed to scrape episode data from IMDb for a given TV series. It fetches details such as episode titles, thumbnails, and descriptions, and saves them in a JSON file.

## Project Structure

```
.
├── main.py
└── requirements.txt
```

## Dependencies

The project dependencies are listed in the `requirements.txt` file. They include:

- `beautifulsoup4`
- `requests`

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the script, execute the following command:

```bash
python main.py
```

Follow the on-screen prompts to search for a series or get episode data for a specific series by its IMDb ID.

### Menu Options

1. **Find series**: Search for TV series on IMDb by entering a query.
2. **Get series data**: Enter the IMDb ID of a series to fetch and save its episode data in a JSON file.
3. **Exit**: Exit the script.

### Example Workflow

1. **Find a series**:
   - Select option `1` and enter a search query.
   - The script will display a list of series with their respective IMDb IDs.

2. **Get series data**:
   - Select option `2` and enter the IMDb ID of the desired series (e.g., `tt0386676`).
   - The script will fetch the episode data for all seasons and save it in a JSON file named after the series in the `data` directory.

## Output

The script creates a directory named `data` (if it doesn't already exist) and saves the scraped episode data in a JSON file with the following structure:

```json
[
    {
        "title": "series_name"
    },
    {
        "season_number": 1,
        "episodes": [
            {
                "title": "Episode 1",
                "thumbnail": "url_to_thumbnail",
                "description": "Episode description"
            },
            ...
        ]
    },
    ...
]
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for parsing HTML.
- [Requests](https://docs.python-requests.org/en/master/) for making HTTP requests.
