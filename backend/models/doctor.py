from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime


class DoctorAddress(BaseModel):
    representation: str = Field(..., alias="representation")
    latitude: float = Field(..., alias="latitude")
    longitude: float = Field(..., alias="longitude")

    class Config:
        allow_population_by_field_name = True


class DoctorContactInformation(BaseModel):
    email: EmailStr = Field(..., alias="email")
    phone: str = Field(..., alias="phone")
    address: DoctorAddress = Field(..., alias="address")

    class Config:
        allow_population_by_field_name = True


class DoctorAvailability(BaseModel):
    days: List[str] = Field(..., alias="days")
    hours: str = Field(..., alias="hours")

    class Config:
        allow_population_by_field_name = True


class DoctorProfile(BaseModel):
    specialization: str = Field(..., alias="specialization")
    education: str = Field(..., alias="education")
    experience: str = Field(..., alias="experience")
    awards: List[str] = Field(..., alias="awards")
    languages: List[str] = Field(..., alias="languages")
    availability: DoctorAvailability = Field(..., alias="availability")

    class Config:
        allow_population_by_field_name = True


class Doctor(BaseModel):
    id: str = Field(..., alias="id")
    dateCreated: datetime = Field(..., alias="dateCreated")
    dateUpdated: datetime = Field(..., alias="dateUpdated")
    isVerified: bool = Field(..., alias="isVerified")
    dp: str = Field(..., alias="dp")
    name: str = Field(..., alias="name")
    role: str = Field(..., alias="role")
    appointmentURL: str = Field(..., alias="appointmentURL")
    profile: DoctorProfile = Field(..., alias="profile")
    contactInformation: DoctorContactInformation = Field(
        ..., alias="contactInformation"
    )

    class Config:
        allow_population_by_field_name = True
