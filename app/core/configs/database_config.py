from pydantic import BaseModel, Field


class DataBaseConfig(BaseModel):
    """Настройки базы данных — только валидация данных"""

    DBMS : str = Field(default="postgresql")
    driver : str = Field(default="asyncpg")
    user: str= Field(...)
    password : str= Field(...)
    host : str= Field(...)
    port : int = Field(...)
    db_name : str= Field(...)

    @property
    def connection_string(self) -> str:
        return f"{self.DBMS}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
