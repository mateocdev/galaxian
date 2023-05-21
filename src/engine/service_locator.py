from src.engine.services.configs_service import ConfigsService
from src.engine.services.fonts_service import FontsService
from src.engine.services.globals_service import GlobalsService
from src.engine.services.images_service import ImagesService
from src.engine.services.sounds_service import SoundsService


class ServiceLocator:
    images_service: ImagesService = ImagesService()
    sounds_service: SoundsService = SoundsService()
    fonts_service: FontsService = FontsService()
    globals_service: GlobalsService = GlobalsService()
    configs_service: ConfigsService = ConfigsService()
