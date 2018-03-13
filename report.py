#!/usr/bin/env python3
import psycopg2


# Print results nicely.
def print_results(results):
    for row in results:
        print(row)


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
        SELECT articles.title,
            Count(*) AS views
        FROM articles
        INNER JOIN log ON articles.slug = LTRIM(log.path, '/article/')
        WHERE log.status = '200 OK'
        GROUP BY articles.title,
                log.path
        ORDER BY views DESC
        LIMIT 3''')
    print_results(results)

    # 2. Who are the most popular article authors of all time?
    results = execute_query('''
        SELECT authors.name,
            Count(*) AS views
        FROM authors
        INNER JOIN articles ON authors.id = articles.author
        INNER JOIN log ON articles.slug = LTRIM(log.path, '/article/')
        WHERE log.status = '200 OK'
        GROUP BY authors.name
        ORDER BY views DESC''')
    print_results(results)

    # 3. On which days did more than 1% of requests lead to errors?
    results = execute_query(''' ''')
    print_results(results)
