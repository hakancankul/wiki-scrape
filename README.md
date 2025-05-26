# Wikipedia Daily Events Database

This project scrapes daily events (births, deaths, events, and holidays) from Wikipedia and stores them in a PostgreSQL/Supabase database.

## Features

- Wikipedia data scraping (Turkish)
- Year-based event tracking
- PostgreSQL/Supabase database integration
- Automatic backup system (JSON)
- Error handling and logging
- Optimized bulk data import
- Transaction management for data integrity

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
   Create a `.env` file with the following variables:
   ```
   DB_HOST=your_host
   DB_PORT=your_port
   DB_NAME=your_database
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

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
python bulk_data_import.py
```

## Performance Optimizations

- Bulk data import using `psycopg2.extras.execute_values`
- In-memory data processing without intermediate CSV files
- Separate transactions for each table import
- Efficient error handling and rollback mechanisms
- Optimized memory usage for large datasets

## Notes

- Data scraping process may take time
- Automatic backup every 10 days
- February is set to 29 days
- Full Turkish character support
- Data is scraped from Turkish Wikipedia
- SSL connection required for Supabase

## Project Structure

- `scrape.py`: Wikipedia scraping script
- `create_table.py`: Database table creation
- `bulk_data_import.py`: Optimized data import to PostgreSQL/Supabase
- `requirements.txt`: Required Python packages
- Generated files:
  - `turkce_tum_gunler.json`: Scraped data backup

## Required Python Packages

- `psycopg2-binary`: PostgreSQL database adapter
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests for scraping
- `beautifulsoup4`: HTML parsing 