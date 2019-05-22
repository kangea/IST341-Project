from django.apps import AppConfig

class RecommendConfig(AppConfig):
    name = 'recommend'
    def ready(self):
        #from .service.recommend_service import train_model_general
        #from .service.recommend_service import train_model_cosine
        #train_model_general()
        #train_model_cosine()
        pass