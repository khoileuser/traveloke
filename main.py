import json
from os import getenv
from dotenv import load_dotenv

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import google.generativeai as genai


load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

countries = json.loads(open('countries.json').read())

genai.configure(api_key=getenv("GEMINI_API"))
model = genai.GenerativeModel('gemini-pro')


def get_response(budget, travel_style, accommodation_standard, length_of_stay, country):
    response = model.generate_content(
        f"recommend for me a travel plan. i have a budget of {budget}$, i plan to stay for {length_of_stay} days, {travel_style} travel style in {country} country with {accommodation_standard} accommodation standard")
    return response.text


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/get_countries")
def read_get_countries():
    return countries


@app.get("/form", response_class=HTMLResponse)
def read_form_get(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")


@app.post("/form", response_class=HTMLResponse)
def read_form_post(request: Request, budget: float = Form(...), travel_style: str = Form(...), accommodation_standard: str = Form(...), length_of_stay: int = Form(...), country: str = Form(...)):
    print(budget, travel_style, accommodation_standard, length_of_stay, country)
    response = get_response(budget, travel_style,
                            accommodation_standard, length_of_stay, country)
    return templates.TemplateResponse(request=request, name="response.html", context={"response": response})
