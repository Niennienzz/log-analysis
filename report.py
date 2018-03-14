#!/usr/bin/env python3
import psycopg2


# Connect to the 'news' database.
def connect_news_db():
    try:
        db = psycopg2.connect("dbname=news")
        cu = db.cursor()
        return db, cu
    except:
        print("FATAL: unable to connect to the database 'news'")


# Execute query and fetch all.
def execute_query(query):
    db, cu = connect_news_db()
    cu.execute(query)
    results = cu.fetchall()
    db.close()
    return results


# Print database results.
def print_database_results(results):
    for row in results:
        print(row[0], "\t", row[1])


# Execute queries and print results.
def execute_queries_and_print(queries):
    for query in queries:
        print(query["title"])
        results = execute_query(query["plain"])
        print_database_results(results)
        print()


q1 = {
    "title": "1.What are the most popular three articles of all time?",
    "plain": '''
    SELECT Articles.Title,
        Count(*) AS Views
    FROM Articles
    INNER JOIN Log ON Log.Path = Concat('/article/', Articles.Slug)
    WHERE Log.Status = '200 OK'
    GROUP BY Articles.Title
    ORDER BY Views DESC
    LIMIT 3;'''
}

q2 = {
    "title": "2.Who are the most popular article authors of all time?",
    "plain": '''
    SELECT Authors.Name,
        Count(*) AS Views
    FROM Authors
    INNER JOIN Articles ON Authors.Id = Articles.Author
    INNER JOIN Log ON Log.Path = Concat('/article/', Articles.Slug)
    WHERE Log.Status = '200 OK'
    GROUP BY Authors.Name
    ORDER BY Views DESC;'''
}

q3 = {
    "title": "3.On which days did more than 1% of requestslead to errors?",
    "plain": '''
    SELECT Log_err.Time,
        Log_err.Percent_err
    FROM
    (SELECT Date(Log.Time) AS TIME,
        100.0 * Sum(
            CASE
            WHEN Log.Status != '200 OK' THEN 1.0
            ELSE 0.0
            END) / Count(Log.Status) AS Percent_err
    FROM Log
    GROUP BY Date(Log.Time)
    ORDER BY Percent_err DESC) AS Log_err
    WHERE Log_err.Percent_err > 1.0;'''
}

if __name__ == '__main__':
    execute_queries_and_print([q1, q2, q3])
