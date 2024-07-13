from dataclasses import dataclass


@dataclass
class AuthModel:
    id: int
    username: str
    email: str
    password: str
    name: str
    age: int
    gender: str
    height: int
    weight: int
    fitness_objective: str
    activity_level: str
    fitness_goal: str
    how_many_months_process: int
    created_at: str
    updated_at: str