from app import config
from app.schemas import AIModel

models_map: dict[str, AIModel] = {
    'gpt-4o': AIModel(name='gpt-4o', provider='openai'),
    'gpt-4o-mini': AIModel(name='gpt-4o-mini', provider='openai'),
    'gpt-4-turbo': AIModel(name='gpt-4-turbo', provider='openai'),
    'gpt-4': AIModel(name='gpt-4', provider='openai'),
    'gpt-3.5-turbo': AIModel(name='gpt-3.5-turbo', provider='openai'),
    'claude-3-5-sonne': AIModel(name='claude-3-5-sonnet-20241022', provider='anthropic'),
    'claude-3-5-haiku': AIModel(name='claude-3-5-haiku-20241022', provider='anthropic'),
    'claude-3-opus-20': AIModel(name='claude-3-opus-20240229', provider='anthropic'),
    'gemini-3-pro-preview': AIModel(name='gemini-3-pro-preview', provider='google_genai'),
    'gemini-3-flash-preview': AIModel(name='gemini-3-flash-preview', provider='google_genai'),
    'gemini-2.5-pro': AIModel(name='gemini-2.5-pro', provider='google_genai'),
    'gemini-2.5-flash': AIModel(name='gemini-2.5-flash', provider='google_genai'),
}


def get_model_by_name(name: str) -> AIModel | None:
    model = models_map.get(name)

    if model is None:
        return None

    if model.provider == 'openai' and config.openai_api_key is None:
        return None

    if model.provider == 'anthropic' and config.openai_api_key is None:
        return None

    if model.provider == 'google_genai' and config.openai_api_key is None:
        return None

    return model


def list_available_models() -> list[AIModel]:
    models = []

    for model in models_map.values():
        if model.provider == 'openai' and config.openai_api_key is None:
            continue
        elif model.provider == 'anthropic' and config.anthropic_api_key is None:
            continue
        elif model.provider == 'google_genai' and config.google_api_key is None:
            continue

        models.append(model)

    return models