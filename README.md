# Travel Scraper Project

Welcome to the **Travel Scraper** project! This project scrapes hotel property information from [trip.com](https://uk.trip.com/) using **Scrapy** and **Scrapy-Selenium**, stores the extracted data into a **PostgreSQL database** using **SQLAlchemy**, and saves hotel images locally. The project has been designed to be **dynamic**, efficient, and easy to use.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Setup Instructions](#setup-instructions)
6. [How to Run](#how-to-run)
7. [Database Structure](#database-structure)
8. [Acceptance Criteria](#acceptance-criteria)
9. [Testing](#testing)
10. [Additional Notes](#additional-notes)

---

## Project Overview
The goal of this project is to scrape hotel property details from **trip.com** and store the following information into a PostgreSQL database:

- Hotel Title
- Rating
- Location
- Latitude and Longitude
- Room Types
- Prices
- Image URLs

The scraped images are stored locally, and their paths are referenced in the database for retrieval.

---

## Features
- **Web Scraping**: Uses **Scrapy** with Selenium to fetch dynamic content.
- **Data Storage**: Stores hotel data into a **PostgreSQL database** using **SQLAlchemy**.
- **Image Handling**: Saves images locally and references them in the database.
- **Dynamic Table Creation**: Tables are automatically created on the fly.
- **Clean and Modular Code**: Designed for readability and easy extensibility.
- **Dockerized Environment**: Includes `Dockerfile` and `docker-compose.yml` for easy deployment.

---

## Project Structure
```plaintext
TRAVEL_SCRAPER/
├── .scrapy/                     # Scrapy cache
├── images/                      # Directory to store hotel images
│   ├── full/                    # Full-size images
│   └── images/                  # Processed images
├── tripcom_scraper/             # Scraper module
│   ├── spiders/                 # Contains the main spider
│   │   └── tripcom_spider.py    # Spider to scrape hotel data
│   ├── items.py                 # Data structure for scraped items
│   ├── pipelines.py             # Handles database and image storage
│   ├── middlewares.py           # Custom middlewares
│   ├── models.py                # SQLAlchemy models for database
│   ├── __init__.py
│   └── settings.py              # Scrapy settings
├── map.html                     # HTML for testing
├── map2.html                    # Another test HTML
├── rooms.html                   # Room types test HTML
├── structure.html               # Structure file for testing
├── docker-compose.yml           # Docker setup for scraper, DB, and pgAdmin
├── Dockerfile                   # Dockerfile for the scraper service
├── requirements.txt             # Python dependencies
├── scrapy.cfg                   # Scrapy configuration
└── README.md                    # Project guidelines (this file)
```

---

## Prerequisites
Make sure you have the following installed:
- **Docker** & **Docker Compose**
- **Python 3.8+**
- PostgreSQL client tools (optional, for manual DB checks)

---

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd TRAVEL_SCRAPER
   ```

2. **Install dependencies**:
   If not using Docker:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Docker environment**:
   ```bash
   docker-compose up --build
   ```
   This will:
   - Start the PostgreSQL database on port `5433`.
   - Run the Scrapy spider container.
   - Launch pgAdmin on port `5051`.

4. **Database Configuration**:
   The database runs with the following credentials:
   - **Host**: `db`
   - **Port**: `5433`
   - **User**: `myuser`
   - **Password**: `mypassword`
   - **Database**: `tripcom_data`

   Update `DATABASE_URL` in `docker-compose.yml` or `settings.py` if needed.

---

## How to Run
1. **Run the Scrapy Spider**:
   To start the scraping process:
   ```bash
   docker-compose exec scraper scrapy crawl tripcom_spider
   ```

2. **Access pgAdmin**:
   Open pgAdmin at [http://localhost:5051](http://localhost:5051) and log in:
   - **Email**: `admin@tripcom.com`
   - **Password**: `admin`

3. **View Scraped Data**:
   Query the database using pgAdmin or any PostgreSQL client:
   ```sql
   SELECT * FROM hotels;
   ```

---

## Database Structure
The following table structure is used:

| Column        | Type           | Description                     |
|---------------|----------------|---------------------------------|
| id            | SERIAL PRIMARY | Unique ID                       |
| title         | TEXT           | Hotel title                     |
| location      | TEXT           | Hotel location                  |
| latitude      | FLOAT          | Latitude coordinate             |
| longitude     | FLOAT          | Longitude coordinate            |
| rating        | FLOAT          | Hotel rating                    |
| room_type     | JSON           | List of room types and prices   |
| image_urls    | TEXT           | Image URLs                      |
| images        | JSON           | Saved image paths               |

---

## Acceptance Criteria
- [x] Use Scrapy Spider for scraping.
- [x] Store data into PostgreSQL using SQLAlchemy.
- [x] Automatically create database tables and save images locally.
- [x] Provide a public repository with documentation.
- [x] Code coverage of at least 60%.

---

## Testing
1. **Unit Tests**: Ensure the data pipeline and models work correctly.
2. **Integration Tests**: Run the scraper end-to-end and verify data storage.
3. **Manual Verification**: Check the database and image storage after scraping.

---

## Additional Notes
- The project uses **Scrapy-Selenium** to load dynamic content.
- Images are stored in the `images/` directory.
- Adjust the `wait_time` parameter in `tripcom_spider.py` if the website loads slowly.

---

## Author
**Your Name**  
Email: yourname@example.com  
LinkedIn: [Your LinkedIn Profile](#)

---

## License
This project is licensed under the MIT License.

---

Happy Scraping! 🕸️
