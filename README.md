# Wikipedia Daily Events Database

This project scrapes daily events (births, deaths, events, and holidays) from Wikipedia and stores them in a PostgreSQL database.

## Features

- Wikipedia data scraping (Turkish)
- Year-based event tracking
- PostgreSQL database integration
- Automatic backup system (JSON)
- Error handling and logging

## Database Structure

### Tables

1. `gun` (day) table
   - `id`: Unique identifier
   - `gun`: Day (1-31)
   - `ay`: Month (1-12)

2. `olay` (event), `dogum` (birth), `olum` (death) tables
   - `id`: Unique identifier
   - `gun_id`: Reference to day table
   - `gun`: Day (1-31)
   - `ay`: Month (1-12)
   - `yil`: Year of the event
   - `icerik`: Event details

3. `tatil` (holiday) table
   - `id`: Unique identifier
   - `gun_id`: Reference to day table
   - `gun`: Day (1-31)
   - `ay`: Month (1-12)
   - `icerik`: Holiday details

## Setup

1. Install PostgreSQL and create a database:
```sql
CREATE DATABASE wikipedia_days;
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Configure database connection:
   - Update connection details in `create_table.py` and `json_to_postgre.py`

## Usage

1. Create database tables:
```bash
python create_table.py
```

2. Scrape data from Wikipedia:
```bash
python scrape.py
```

3. Import data to PostgreSQL:
```bash
python json_to_postgre.py
```

## Notes

- Data scraping process may take time
- Automatic backup every 10 days
- February is set to 29 days
- Full Turkish character support
- Data is scraped from Turkish Wikipedia

## Project Structure

- `scrape.py`: Wikipedia scraping script
- `create_table.py`: Database table creation
- `json_to_postgre.py`: Data import to PostgreSQL
- `requirements.txt`: Required Python packages
- Generated files:
  - `turkce_tum_gunler.json`: Scraped data backup 