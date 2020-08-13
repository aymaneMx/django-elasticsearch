# Django, Docker and ElasticSearch

Simple project to test Elasticsearch with Django, build on docker.

## Build/run the project

```bash
docker-compose up -d --build
```

Now visit http://127.0.0.1:8000/ 

## Test Elasticsearch in shell

Run:

```bash
docker-compose run web python manage.py load_posts 20
```

Now, let's hop into the interactive Python shell and play around with ElasticSearch queries:

```bash
docker-compose run web python manage.py shell
```

I gathered here a list of examples of use you may need:

```python
search = PostDocument.search()

# Filter by single field equal to a value
search = search.query('match', draft=False)

# Filter by single field containing a value
search = search.filter('match_phrase', title="value")

# Add the query to the Search object
from elasticsearch_dsl import Q

q = Q("multi_match", query='python django', fields=['title', 'content'])
search = search.query(q)

# Query combination
or_q = Q("match", title='python') | Q("match", title='django')
and_q = Q("match", title='python') & Q("match", title='django')

# Exclude items from your query
search = search.exclude('match', draft=True)

# Filter documents that contain terms within a provided range.
# eg: the posts created for the past day
search = search.filter('range', created_at={"gte": "now-1d"})

# Ordering
# prefixed by the - sign to specify a descending order.
search = search.sort('-likes', 'created_at')
```
