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
docker-compose run web python manage.py migrate

docker-compose run web python manage.py load_posts 20
```

Now, let's hop into the interactive Python shell and play around with ElasticSearch queries:

```bash
docker-compose run web python manage.py shell
```

```
from posts.documents import PostDocument
posts = PostDocument.search()
for hit in posts:
    print(hit.title)
```

Check out the [article](https://obytes.com/blog/building-a-full-text-search-app-using-django-docker-and-elasticsearch) for this project, for more examples of use.  
