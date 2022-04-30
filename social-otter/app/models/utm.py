from typing import Optional
from pydantic import BaseModel


class UTM(BaseModel):
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    utm_term: Optional[str]
    utm_content: Optional[str]
