"""
This module expose endpoints with main app features
"""
from typing import Dict

from fastapi import APIRouter, status

from src.services.calculator import Calculator

router = APIRouter()


@router.get("/addition/", tags=["Calculator"], status_code=status.HTTP_200_OK)
async def addition(a: float, b: float) -> Dict[str, float]:
    """Performs the addition of two float values

    Returns:
        Dict[str, float]: single key dict with result of the operation
    """
    return {"result": Calculator.suma(a, b)}


@router.get("/substract/", tags=["Calculator"], status_code=status.HTTP_200_OK)
async def substraction(a: float, b: float) -> Dict[str, float]:
    """Performs the substraction of two float values

    Returns:
        Dict[str, float]: single key dict with result of the operation
    """
    return {"result": Calculator.resta(a, b)}


@router.get("/multiply/", tags=["Calculator"], status_code=status.HTTP_200_OK)
async def multiply(a: float, b: float) -> Dict[str, float]:
    """Performs the multiplication of two float values

    Returns:
        Dict[str, float]: single key dict with result of the operation
    """
    return {"result": Calculator.multiplicacion(a, b)}


@router.get(
    "/divide/",
    tags=["Calculator"],
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def divide(a: float, b: float) -> Dict[str, float | ZeroDivisionError]:
    """Performs the division of two float values.
    Response model is None due to conditional float | ZeroDivisionError
    is not supported by pydantic.

    Returns:
        Dict[str, float]: single key dict with result of the operation
    """
    return {"result": Calculator.division(a, b)}
