from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CPEOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cpe_title: Optional[str] = None
    cpe_22_uri: Optional[str] = None
    cpe_23_uri: Optional[str] = None
    reference_links: Optional[List[str]] = None
    cpe_22_deprecation_date: Optional[date] = None
    cpe_23_deprecation_date: Optional[date] = None


class CPEListResponse(BaseModel):
    page: int
    limit: int
    total: int
    data: List[CPEOut]


class CPESearchResponse(BaseModel):
    data: List[CPEOut]
