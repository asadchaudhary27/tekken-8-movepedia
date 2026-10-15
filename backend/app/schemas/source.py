from typing import Optional
from pydantic import BaseModel, ConfigDict


class DataSourceBase(BaseModel):
    name: str
    base_url: str
    license_type: str
    approval_status: str
    rate_limit_policy: str
    is_active: bool = True


class DataSourceResponse(DataSourceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
