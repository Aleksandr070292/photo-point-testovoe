from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from enum import Enum

# Инициализация FastAPI приложения
app = FastAPI(title="Incident Management API", 
              description="API для учета инцидентов")

# Настройка базы данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./incidents.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель статусов инцидентов
class IncidentStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

# Модель источников инцидентов
class IncidentSource(str, Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"

# Модель данных инцидента для базы данных
class IncidentModel(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default=IncidentStatus.NEW, nullable=False)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Pydantic модели для валидации данных
class IncidentCreate(BaseModel):
    description: str
    source: IncidentSource
    
    class Config:
        use_enum_values = True

class IncidentUpdate(BaseModel):
    status: IncidentStatus
    
    class Config:
        use_enum_values = True

class IncidentResponse(BaseModel):
    id: int
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime
    
    class Config:
        use_enum_values = True
        from_attributes = True

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для создания инцидента
@app.post("/incidents/", response_model=IncidentResponse, status_code=201)
def create_incident(incident: IncidentCreate):
    db = next(get_db())
    db_incident = IncidentModel(
        description=incident.description,
        source=incident.source,
        status=IncidentStatus.NEW
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

# Эндпоинт для получения списка инцидентов с фильтром по статусу
@app.get("/incidents/", response_model=List[IncidentResponse])
def get_incidents(status: Optional[IncidentStatus] = Query(None)):
    db = next(get_db())
    query = db.query(IncidentModel)
    if status:
        query = query.filter(IncidentModel.status == status)
    return query.all()

# Эндпоинт для обновления статуса инцидента по id
@app.patch("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident_status(incident_id: int, incident_update: IncidentUpdate):
    db = next(get_db())
    db_incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db_incident.status = incident_update.status
    db.commit()
    db.refresh(db_incident)
    return db_incident

# Корневой эндпоинт для проверки работы API
@app.get("/")
def read_root():
    return {"message": "Incident Management API"}