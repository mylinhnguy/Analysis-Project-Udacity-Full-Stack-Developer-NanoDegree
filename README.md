# Project Overview

In this project, to build a reporting tool that will use information from a large newspaper database of a web server log 
to discover and analyze what kind of articles the site's readers like.
The database with over a million rows is explored by building complex SQL queries to draw business conclusions from data. 
The database could have come from a real-world web application. It contains newspaper articles, as well as the web server log for the site. 
The log has a database row for each time a reader loaded a web page. 

The project drives following conclusions:
-  Most popular three articles of all time.
-  Most popular article authors of all time.
-  Days on which more than 1% of requests lead to errors.

## How to Run
  PreRequisites:

  ```
  Python3
  VirtualBox
  Vagrant
  ```
## Setup Project:
1. Download and install VirtualBox 
1. Download and install Vagrant
2. Download or Clone fullstack-nanodegree-vm repository. https://github.com/udacity/fullstack-nanodegree-vm
3. Download the data https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
4. Unzip this file after downloading it. The file inside is called newsdata.sql.
5. Copy the newsdata.sql file and content of this current repository

## Launching the Virtual Machine:
1. Launch the Vagrant VM inside Vagrant sub-directory in the downloaded fullstack-nanodegree-vm repository 
   - `vagrant up`
2. Log into this using command
   - `vagrant ssh`
3. Change directory to the /vagrant directory by typing 
   - `cd /vagrant` and ls.

## Setting up the database:
1. Load the data in local database using the command:
   - `psql -d news -f newsdata.sql`

2. Connect to database.
   - `psql -d news`

The database includes three tables:    
    ```
    The authors table includes information about the authors of articles.
    The articles table includes the articles themselves.
    The log table includes one entry for each time a user has accessed the site.
    ```

## Creating Views:
1.
    ```
    create or replace view popular_authors as select authors.name,
    count(articles.author) as views from articles, authors, log
    where concat('/article/',articles.slug) = log.path and articles.author = authors.id
    group by authors.name order by views desc
    ```
2.
    ```
    create or replace view popular_authors as select authors.name,
    count(articles.author) as views from articles, authors, log
    where concat('/article/',articles.slug) = log.path and articles.author = authors.id
    group by authors.name order by views desc
    ```
3.
    ```
    create or replace view log_errors as select Date, Total_Views, Total_Error,
    (Total_Error::float*100)/Total_Views::float as Percent from
    (select time::date as Date, count(status) as Total_Views,va
    sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Total_Error
    from log group by time::date) as result
    where (Total_Error::float*100)/Total_Views::float > 1.0 order by Percent desc;
    ```
## Running the queries:
    From the vagrant directory inside the virtual machine, run analysisProject.py to generate the analysis report:
    - `$ python3 analysisProject.py`  

## Example Output:
    Reporting results...

    ```
    1.The most popular three articles of the time:
    1) "Candidate is jerk, alleges rival" - 338647 views
    2) "Bears love berries, alleges bear" - 253801 views
    3) "Bad things gone, say good people" - 170098 views

    2.The most popular article authors of the time:
    "Ursula La Multa" - 507594 views
    "Rudolf von Treppenwitz" - 423457 views
    "Anonymous Contributor" - 170098 views
    "Markoff Chaney" - 84557 views

    3.Days with more than 1% of requests lead to errors:
    2016-07-17 - 2.26% errors
    ```



