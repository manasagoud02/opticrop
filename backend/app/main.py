import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

from .auth import create_access_token, get_current_user, get_password_hash, verify_password
from .database import create_user, fetch_recommendation_history, init_db, save_recommendation
from .ml import evaluate_crop, recommend_crops

app = FastAPI(title="OptiCrop API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class RecommendationRequest(BaseModel):
    nitrogen: float = Field(ge=0.0)
    phosphorous: float = Field(ge=0.0)
    potassium: float = Field(ge=0.0)
    temperature: float = Field(ge=0.0)
    humidity: float = Field(ge=0.0)
    ph: float = Field(ge=0.0)
    rainfall: float = Field(ge=0.0)


class EvaluateRequest(BaseModel):
    crop_name: str
    nitrogen: float = Field(ge=0.0)
    phosphorous: float = Field(ge=0.0)
    potassium: float = Field(ge=0.0)
    temperature: float = Field(ge=0.0)
    humidity: float = Field(ge=0.0)
    ph: float = Field(ge=0.0)
    rainfall: float = Field(ge=0.0)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/register")
def register(request: RegisterRequest) -> Dict[str, Any]:
    from .database import fetch_user_by_email

    if fetch_user_by_email(str(request.email)):
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = create_user(request.name, str(request.email), get_password_hash(request.password))
    token = create_access_token(str(user_id))
    return {"token": token, "user": {"id": user_id, "name": request.name, "email": str(request.email)}}


@app.post("/auth/login")
def login(request: LoginRequest) -> Dict[str, Any]:
    from .database import fetch_user_by_email

    user = fetch_user_by_email(str(request.email))
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user["id"]))
    return {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}


@app.post("/recommend")
def recommend(payload: RecommendationRequest, current_user=Depends(get_current_user)) -> Dict[str, Any]:
    results = recommend_crops(payload.model_dump())
    top_crop = results[0] if results else None
    if top_crop:
        save_recommendation(current_user["id"], top_crop["crop_name"], top_crop["score"], top_crop["reason"])
    return {"recommendations": results, "top_crop": top_crop}


@app.post("/evaluate")
def evaluate(payload: EvaluateRequest, current_user=Depends(get_current_user)) -> Dict[str, Any]:
    result = evaluate_crop(payload.model_dump(exclude={"crop_name"}), payload.crop_name)
    return {"result": result}


@app.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)) -> Dict[str, Any]:
    history = fetch_recommendation_history(current_user["id"])
    return {"user": current_user, "history": history}
