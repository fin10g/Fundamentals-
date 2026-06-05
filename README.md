# CA1: Building a Distributed Web Application Using Cloud Computing

**Student:** Fintan Geraghty
**Student ID:** 25105066
**Email:** [fintang4@gmail.com](mailto:fintang4@gmail.com)
**Programme:** 1SDC1 – Cloud Computing, Software Development & DevOps
**Module:** CT5169 – Fundamentals of Cloud Computing
**Submission Date:** 19/04/2026

---

# Overview

This project demonstrates a distributed web application built using Flask, MySQL, Docker, and AWS EC2. The application allows users to search Wikipedia through a web interface while distributing processing across three separate virtual machines.

The architecture consists of:

1. **Flask VM** – Hosts the web application and user interface.
2. **MySQL VM** – Stores and retrieves cached search results.
3. **Wikipedia VM (AWS EC2)** – Performs Wikipedia searches when results are not found in the cache.

The application follows a cache-first approach to improve performance and reduce unnecessary Wikipedia requests.

---

# Architecture

## Workflow

1. A user enters a search term through the Flask web interface.
2. The Flask application checks the MySQL database for an existing result.
3. If a cached result exists:

   * The result is returned directly from MySQL.
4. If no cached result exists:

   * Flask connects to the AWS EC2 instance using Paramiko.
   * The `wiki.py` script retrieves data from Wikipedia.
   * The result is displayed to the user.
   * The result is stored in MySQL for future searches.

---

# Flask Application

The Flask application acts as the central controller of the system.

### Responsibilities

* Accept user search requests through a web browser.
* Connect to the MySQL VM.
* Retrieve cached search results.
* Connect to the AWS EC2 Wikipedia VM when required.
* Store newly retrieved results in the database.
* Render search results in the browser.

### Deployment

The application was developed using PyCharm on the host machine and transferred to the Flask VM using SCP:

```bash
scp -r -P 2222 FundamentalsAssignment student@127.0.0.1:~/flaskProjects/wikidb1
```

The Nano text editor was used for quick modifications directly on the VM.

---

# Wikipedia VM (AWS EC2)

The Wikipedia search functionality is hosted on an AWS EC2 Ubuntu instance.

### Notes

* The EC2 instance IP address changes whenever the instance is restarted.
* The public IP address stored in the Flask application must therefore be updated when reconnecting.
* Flask uses Paramiko SSH connections to execute `wiki.py` remotely.

### wiki.py

```python
import wikipedia
import sys

def searchWikipedia(term):
    pageIds = wikipedia.search(term)
    pages = []

    for pageId in pageIds:
        try:
            page = wikipedia.page(pageId)
            pages.append(page)
        except:
            print("Oops: could not parse the page:", pageId)
            pass

    if len(pages) >= 0:
        for page in pages:
            print(
                "title: " + page.title +
                " URL: " + page.url +
                " Content: " + page.content
            )
    else:
        return "No results!"

arguments = "".join(sys.argv[1:])
searchWikipedia(arguments)
```

### Functionality

The script:

1. Searches Wikipedia for the supplied term.
2. Retrieves matching pages.
3. Extracts:

   * Title
   * URL
   * Content
4. Returns the data to the Flask application.

---

# MySQL VM

A dedicated Ubuntu VM hosts a Docker container running MySQL.

### Docker Setup

The database server was deployed using:

```bash
sudo docker run --name "mysqlwikidb" \
-e MYSQL_ROOT_HOST=% \
-e MYSQL_ROOT_PASSWORD=mypassword \
-d -p 7888:3306 \
mysql/mysql-server:latest
```

Using Docker simplified deployment and avoided the need to install MySQL directly on the VM.

---

# Database Schema

The following table was created to store Wikipedia search results:

```sql
CREATE TABLE wiki (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(255) NOT NULL,
    result LONGTEXT NOT NULL
);
```

### Table Description

| Column | Description       |
| ------ | ----------------- |
| id     | Unique identifier |
| item   | Search term       |
| result | Wikipedia content |

The `LONGTEXT` datatype was selected to accommodate large Wikipedia page content.

---

# Database Integration

The Flask application uses the MySQL Connector library to:

### Retrieve Cached Results

When a search term already exists in the database:

```python
result = row[2]
```

The stored result is extracted and rendered directly in the browser.

### Store New Results

When a result is retrieved from Wikipedia:

```sql
INSERT INTO wiki (item, result)
VALUES (...)
```

The result is saved for future searches.

---

# VM Configuration

## Flask VM Port Forwarding

| Name  | Protocol | Host Port | Guest Port |
| ----- | -------- | --------- | ---------- |
| Flask | TCP      | 3000      | 8888       |
| HTTP  | TCP      | 8080      | 3000       |
| SSH   | TCP      | 2222      | 22         |

---

## MySQL VM Port Forwarding

| Name  | Protocol | Host Port | Guest Port |
| ----- | -------- | --------- | ---------- |
| SSH   | TCP      | 2222      | 22         |
| MySQL | TCP      | 7888      | 3306       |
| HTTP  | TCP      | 8080      | 3000       |

---

# Challenges Encountered

## MySQL Connectivity Issues

Initially, the Flask application could not connect to the MySQL VM.

### Cause

The incorrect IP address (`10.0.2.2`) was being used.

### Solution

Running:

```bash
ifconfig
```

on the MySQL VM revealed the correct network address. Testing the available addresses eventually identified the correct host for the database connection.

---

## HTML Formatting Problems

Wikipedia results were initially formatted using HTML inside a `join()` statement to preserve spacing.

### Problem

When results were retrieved from MySQL, the application attempted to render the entire tuple object as a string, causing formatting issues.

### Solution

Instead of converting the tuple directly, the application extracts the content from the `result` column before rendering.

This allowed both live Wikipedia results and cached database results to display correctly in the browser.

---

# Conclusion

This project successfully demonstrates a distributed cloud-based application using multiple virtual machines and services.

Key technologies used include:

* Flask
* Python
* MySQL
* Docker
* AWS EC2
* Paramiko
* Wikipedia API

The solution implements a simple caching architecture where search results are stored in a database after the first lookup, reducing repeated requests to Wikipedia and improving performance.

# Steps to start application.

Start EC2 instance.
find public ip

Start CT5169_VM04
ssh: sudo docker start mysqlwiki
ssh: sudo docker exec -it mysqlwiki /bin/sh
sh-4.4# mysql -u root -p (mypassword)
mysql> USE wiki

Start CT5169_VM02
scp -r -P 2222 FundamentalsAssignment student@127.0.0.1:~/flaskProjects/wikidb1
OR
ssh: cd ~/flaskProjects/wikidb1
ssh: nano app.py
    CHANGE INSTANCE IP
    ^X y ENTER
ssh: python3 app.py

Browser
http://127.0.0.1:3000/search
Search: Paul Thomas Anderson

mysql vm ip: 192.168.56.6
