# Log Analysis

## Project Overview
> In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

As part of the Udacity \<Full Stack Developer\> Nanodegree, the intent of this project is to practice the [OLAP](https://en.wikipedia.org/wiki/Online_analytical_processing) (contrasted to [OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing)) capability of database by using complex queries.

> Online analytical processing, or OLAP, is an approach to answering multi-dimensional analytical queries swiftly in computing. OLAP is part of the broader category of business intelligence, which also encompasses relational database, report writing and data mining. [Wikipedia](https://en.wikipedia.org/wiki/Online_analytical_processing)

## Environment Setup
* Install [Python3](https://www.python.org/).
* Install [VirtualBox](https://www.virtualbox.org/).
* Install [Vagrant](https://www.vagrantup.com/).
* Download the [Vagrantfile](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile) from Udacity.
* Download the [SQLFile](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) from Udacity.
* Make a new vagrant directory on your machine, put the Vagrantfile, the SQLFile (newsdata.sql), and the Python script (report.py) in there.
* Within the vagrant directory, launch the virtual machine using the following command:
```
    $ vagrant up
```
* Login to the virtual machine using the following command:
```
    $ vagrant ssh
```
* Load the database using the following command:
```
    psql -d news -f newsdata.sql
```
* NOTE: The shared directory in the virtual machine is under root /vagrant.

## Run the Python Program
* From the vagrant directory __inside the virtual machine__:
```
    python3 report.py
```

## Summary
As mentioned above, the intent of this project is to practice complex queries. However, in my mind as a backend developer, the data layer (code-to-database layer) should be slim and simple in order to serve the purpose of fast transactions for an application. In one of my projects at work, several simple tables are loaded into memory upon application start. This may sound a bit crazy but the in-memory cache-like model generates fast responses in many cases. Inserts, updates, or deletes go to the database. But __get__ operations can be served from memory directly. We also keep an in-memory index for these tables given the fact that they are simple but not necessarily small. Also, even mature databases have bottleneck dealing with complex indexes and relationships. For future both OLTP/OLAP capable databases, [TiDB](https://www.pingcap.com/en/) and [CockroachDB](https://www.cockroachlabs.com/) are interesting projects to be kept an eye on them. Cheers :-)