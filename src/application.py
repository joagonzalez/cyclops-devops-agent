"""
Main Application class that extends FastAPI behavior.
"""

from fastapi import FastAPI

from src.api.calculator import router as calculator
from src.api.health import router as health
from src.config.settings import PROMPT, config

# from src.api.users import router as users
# from src.api.calculator import router as calculator
# from src.services.databaseService import database
# from src.database import SessionLocal, Base, engine


class Application(FastAPI):
    """
    Wrapper class for FASTAPI
    """

    def __init__(self) -> None:
        """SWAGGER CONFIGURATION"""
        super().__init__(
            title=config["API"]["TITLE"],
            description=config["API"]["DESCRIPTION"],
            version=config["API"]["VERSION"],
            docs_url=config["SWAGGER"]["DOCS_URL"],
            redoc_url=config["SWAGGER"]["REDOC_URL"],
        )

    def bootstrap(self) -> None:
        """SERVER CONFIGURATION"""
        self.debug = config["SERVER"]["DEBUG"]
        self.configure_endpoints()
        # self.configureDB()
        print(PROMPT)

    def configure_endpoints(self) -> None:
        """REGISTER API ROUTERS"""
        # self.include_router(authentication)
        # self.include_router(users, prefix='/users')
        self.include_router(calculator, prefix="/calculator")
        self.include_router(health, prefix="/health")

    # def configureDB(self):
    #     ''' INIT SQLITE DB '''
    #     Base.metadata.create_all(engine)
    #     db = SessionLocal()
    #     database.init_defaults(db)


if __name__ == "__main__":
    pass
