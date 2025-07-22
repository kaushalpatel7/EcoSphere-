from django.apps import AppConfig


class EnvAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'env_app'
    # label = 'env_app'  # Add this line to ensure unique label