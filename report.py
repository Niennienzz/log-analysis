#!/usr/bin/env python3
import psycopg2


# Print results nicely.
def print_results(results):
    for row in results:
        print(row[0], "\t", row[1])


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


if __name__ == '__main__':
    # 1. What are the most popular three articles of all time?
    results = execute_query('''
        SELECT Articles.Title,
            Count(*) AS Views
        FROM Articles
        INNER JOIN Log ON Articles.Slug = Ltrim(Log.Path, '/article/')
        WHERE Log.Status = '200 OK'
        GROUP BY Articles.Title
        ORDER BY Views DESC
        LIMIT 3;''')
    print("1. What are the most popular three articles of all time?")
    print_results(results)
    print()

    # 2. Who are the most popular article authors of all time?
    results = execute_query('''
        SELECT Authors.Name,
            Count(*) AS Views
        FROM Authors
        INNER JOIN Articles ON Authors.Id = Articles.Author
        INNER JOIN Log ON Articles.Slug = Ltrim(Log.Path, '/article/')
        WHERE Log.Status = '200 OK'
        GROUP BY Authors.Name
        ORDER BY Views DESC;''')
    print("2. Who are the most popular article authors of all time?")
    print_results(results)
    print()

    # 3. On which days did more than 1% of requests lead to errors?
    # This is a hard one to me... References:
    # https://www.postgresql.org/docs/current/static/functions-conditional.html
    # http://www.postgresqltutorial.com/postgresql-subquery/
    # https://github.com/ddavignon/logs-analysis/blob/master/newsdata.py
    # https://github.com/sagarchoudhary96/Log-Analysis/blob/master/logs.py
    results = execute_query('''
        SELECT Log_err.Time,
            Log_err.Percent_err
        FROM
            (SELECT Date(Log.Time) as Time,
                100.0 * Sum(
                    CASE WHEN Log.Status != '200 OK' THEN 1.0
                    ELSE 0.0
                    END) / Count(Log.Status) AS Percent_err
            FROM Log
            GROUP BY Date(Log.Time)
            ORDER BY Percent_err DESC) AS Log_err
        WHERE Log_err.Percent_err > 1.0;''')
    print('''3. On which days did more than 1% of requestslead to errors?''')
    print_results(results)
    print()
