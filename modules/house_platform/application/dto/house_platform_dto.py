from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class HousePlatformCreateRequest(BaseModel):
    title: Optional[str] = None
    address: Optional[str] = None
    deposit: Optional[int] = None
    domain_id: Optional[int] = 1
    rgst_no: Optional[str] = None
    sales_type: Optional[str] = None
    monthly_rent: Optional[int] = None
    room_type: Optional[str] = None
    contract_area: Optional[float] = None
    exclusive_area: Optional[float] = None
    floor_no: Optional[int] = None
    all_floors: Optional[int] = None
    lat_lng: Optional[Dict[str, Any]] = None
    manage_cost: Optional[int] = None
    can_park: Optional[bool] = None
    has_elevator: Optional[bool] = None
    image_urls: Optional[str] = None
    pnu_cd: Optional[str] = None
    is_banned: Optional[bool] = False
    residence_type: Optional[str] = None
    gu_nm: Optional[str] = None
    dong_nm: Optional[str] = None
    snapshot_id: Optional[str] = None

class HousePlatformUpdateRequest(BaseModel):
    title: Optional[str] = None
    address: Optional[str] = None
    deposit: Optional[int] = None
    rgst_no: Optional[str] = None
    sales_type: Optional[str] = None
    monthly_rent: Optional[int] = None
    room_type: Optional[str] = None
    contract_area: Optional[float] = None
    exclusive_area: Optional[float] = None
    floor_no: Optional[int] = None
    all_floors: Optional[int] = None
    lat_lng: Optional[Dict[str, Any]] = None
    manage_cost: Optional[int] = None
    can_park: Optional[bool] = None
    has_elevator: Optional[bool] = None
    image_urls: Optional[str] = None
    pnu_cd: Optional[str] = None
    is_banned: Optional[bool] = None
    residence_type: Optional[str] = None
    gu_nm: Optional[str] = None
    dong_nm: Optional[str] = None
    snapshot_id: Optional[str] = None

class HousePlatformResponse(BaseModel):
    house_platform_id: int
    title: Optional[str]
    address: Optional[str]
    deposit: Optional[int]
    domain_id: Optional[int]
    rgst_no: Optional[str]
    sales_type: Optional[str]
    monthly_rent: Optional[int]
    room_type: Optional[str]
    contract_area: Optional[float]
    exclusive_area: Optional[float]
    floor_no: Optional[int]
    all_floors: Optional[int]
    lat_lng: Optional[Dict[str, Any]]
    manage_cost: Optional[int]
    can_park: Optional[bool]
    has_elevator: Optional[bool]
    image_urls: Optional[str]
    pnu_cd: Optional[str]
    is_banned: Optional[bool]
    residence_type: Optional[str]
    gu_nm: Optional[str]
    dong_nm: Optional[str]
    registered_at: Optional[datetime]
    crawled_at: Optional[datetime]
    snapshot_id: Optional[str]
    abang_user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True