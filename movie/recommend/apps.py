from django.apps import AppConfig
from .service.recommend_service import train_model_general
from .service.recommend_service import train_model_cosine

class RecommendConfig(AppConfig):
    name = 'recommend'
    def ready(self):
        train_model_general()
        train_model_cosine()
        #pass