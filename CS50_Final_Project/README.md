# ZaYerbani
#### Video Demo:
#### Description:
A common challenge for Yerba Mate enthusiasts is identifying a trustworthy source for product reviews. Addressing this need, I introduced "ZaYerbani", a platform where users can discover, rate, and track Yerba Mate products.

### dynamic.py:
I initiated the project with a web scraping program written in Python, leveraging Selenium to extract URLs of Yerba Mate products from the website: poyerbani.pl. The script is adept at automatically navigating through multiple pages, collecting product URLs until the site has been fully scraped.

### scraper.py:
This script takes the URLs from dynamic.py, delves into each URL, and extracts specific product information for our database. The gathered data is then saved into a CSV file named products.csv.

### insert.py:
Using this script, I established an SQL database within zayerbani.db. This approach allowed me to review the CSV data before committing it to SQL.

### zayerbani.db:
This houses a relational database dedicated to Yerba Mate reviews. It comprises five tables. While some tables were created primarily to hone my SQL skills, it might be more efficient to store certain information in app.py's memory for quicker access.

### helpers.py:
This file offers a suite of helper functions designed to optimize the main application's processes. These functions handle tasks such as user authentication, data retrieval, and data formatting. Notably, some functions were initially intended for a different project involving the Spotify API. However, due to data access limitations, I pivoted to the ZaYerbani project.

### app.py:
Serving as the primary gateway for the Flask web application, this file manages HTTP requests, routing, user authentication, and database interactions. I encountered issues with page refresh post-submission, so I opted to redirect users to the search page after submitting a review.

### script.js:
This JavaScript file contains several functions aimed at enhancing user experience, such as toggling visibility of specific page elements.

### style.css:
This stylesheet played a pivotal role, especially in designing the review button, ensuring the website's aesthetic appeal.

### templates:
These are the envisioned HTML pages for the website.

### garbages:
This section encompasses auxiliary files required for various purposes, like chrome-linux64 for web scraping, and remnants from the initial Spotify API project.



