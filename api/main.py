from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routers.sentiment_analyisis import SentimentAnalysisAPI

# APP
app = FastAPI()

# MODELS
# TODO change this to a mapping automatically added
sentiment_analyisis = SentimentAnalysisAPI()
app.include_router(sentiment_analyisis.router,
                   prefix=f"/{sentiment_analyisis.MODEL_NAME}",
                   tags=[sentiment_analyisis.MODEL_NAME])

# SWAGGER CUSTOMIZATION
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FaMAF API Swagger",
        version="0.0.1",
        description="",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.famaf.unc.edu.ar/static/assets/logoFaMAF.svg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi
