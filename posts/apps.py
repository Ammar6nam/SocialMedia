from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'

class CustomMathFiltersConfig(AppConfig):
    label = 'custom_mathfilters'
    name = 'mathfilters'