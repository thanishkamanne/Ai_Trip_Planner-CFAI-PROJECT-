from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class TransportType(Enum):
    FLIGHT = "Flight"
    TRAIN = "Train"
    BUS = "Bus"
    CAR = "Car"

class HotelPreference(Enum):
    BUDGET = "Budget"
    STANDARD = "Standard"
    LUXURY = "Luxury"

class RiskTolerance(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

@dataclass
class TripRequest:
    source: str
    destination: str
    budget: float
    duration: int
    hotel_pref: HotelPreference
    transport_pref: TransportType
    risk_tolerance: RiskTolerance

@dataclass
class RouteInfo:
    path: List[str]
    total_distance: float
    total_cost: float
    total_time: float
    avg_traffic: float
    max_risk: float
    algorithm: str
    explored_nodes: int
    execution_time: float
    explanation: str = ""

@dataclass
class User:
    username: str
    password: str
    email: str
    saved_trips: List[Dict] = field(default_factory=list)
