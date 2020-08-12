from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post, Reply

User = get_user_model()


@registry.register_document
class PostDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        # 'photo': fields.FileField(),  use this type if you have a file/image
    })

    class Index:
        # Name of the Elasticsearch index
        name = 'posts'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Post  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'content',
            'created_at',
            'likes',
            'draft',
            'slug',
        ]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(PostDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Post instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, User):
            return related_instance.posts.all()
        elif isinstance(related_instance, Reply):
            return related_instance.post
