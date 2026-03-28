import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.operations import add, subtract, multiply, divide

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Calculator API")
templates = Jinja2Templates(directory="templates")


class CalculationRequest(BaseModel):
    a: float
    b: float


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    logger.info("GET / — serving calculator frontend")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add")
async def calculate_add(req: CalculationRequest):
    logger.info("POST /add | a=%s b=%s", req.a, req.b)
    result = add(req.a, req.b)
    return {"operation": "add", "a": req.a, "b": req.b, "result": result}


@app.post("/subtract")
async def calculate_subtract(req: CalculationRequest):
    logger.info("POST /subtract | a=%s b=%s", req.a, req.b)
    result = subtract(req.a, req.b)
    return {"operation": "subtract", "a": req.a, "b": req.b, "result": result}


@app.post("/multiply")
async def calculate_multiply(req: CalculationRequest):
    logger.info("POST /multiply | a=%s b=%s", req.a, req.b)
    result = multiply(req.a, req.b)
    return {"operation": "multiply", "a": req.a, "b": req.b, "result": result}


@app.post("/divide")
async def calculate_divide(req: CalculationRequest):
    logger.info("POST /divide | a=%s b=%s", req.a, req.b)
    try:
        result = divide(req.a, req.b)
        return {"operation": "divide", "a": req.a, "b": req.b, "result": result}
    except ValueError as e:
        logger.warning("POST /divide error: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
