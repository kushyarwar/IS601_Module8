from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.operations import add, subtract, multiply, divide

app = FastAPI(title="Calculator API")
templates = Jinja2Templates(directory="templates")


class CalculationRequest(BaseModel):
    a: float
    b: float


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add")
async def calculate_add(req: CalculationRequest):
    result = add(req.a, req.b)
    return {"operation": "add", "a": req.a, "b": req.b, "result": result}


@app.post("/subtract")
async def calculate_subtract(req: CalculationRequest):
    result = subtract(req.a, req.b)
    return {"operation": "subtract", "a": req.a, "b": req.b, "result": result}


@app.post("/multiply")
async def calculate_multiply(req: CalculationRequest):
    result = multiply(req.a, req.b)
    return {"operation": "multiply", "a": req.a, "b": req.b, "result": result}


@app.post("/divide")
async def calculate_divide(req: CalculationRequest):
    try:
        result = divide(req.a, req.b)
        return {"operation": "divide", "a": req.a, "b": req.b, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
