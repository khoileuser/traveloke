import json
from os import getenv
from dotenv import load_dotenv
from random import randint

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import google.generativeai as genai


load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

countries = json.loads(open('countries.json').read())

genai.configure(api_key=getenv("GEMINI_API"))
model = genai.GenerativeModel('gemini-pro')

chats = {}


def parse_prompt(budget, length_of_stay, country, travel_styles, locales, activities, accommodation_standard):
    prompt = f"Build for me a {length_of_stay} days trip in {country} with a budget of {budget} $USD. "

    _travel_styles = travel_styles.split(", ")
    if len(_travel_styles) > 1:
        prompt += f"My travel style are {travel_styles}. "
    else:
        prompt += f"My travel style is {travel_styles}. "

    prompt += f"I would like my destination to have {locales}. I love {activities}. "

    _accommodation_standard = accommodation_standard.split(", ")
    if len(_accommodation_standard) > 1:
        prompt += f"My ideal accommodations are {accommodation_standard}, you pick the highest of them available."
    else:
        prompt += f"My ideal accommodation is {accommodation_standard}."

    print(prompt)
    return prompt


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/get_countries")
def read_get_countries():
    return countries


@app.get("/form", response_class=HTMLResponse)
def read_form_get(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")


@app.post("/conversation", response_class=HTMLResponse)
def read_form_post(request: Request, budget: float = Form(...), length_of_stay: int = Form(...), country: str = Form(...),
                   travel_styles: str = Form(...), locales: str = Form(...), activities: str = Form(...), accommodation_standard: str = Form(...)):
    chat = model.start_chat(history=[])
    while True:
        chat_id = randint(0, 999999)
        if chat_id not in chats:
            chats[chat_id] = chat
            break
    response = chat.send_message(parse_prompt(
        budget, length_of_stay, country, travel_styles, locales, activities, accommodation_standard))
    return templates.TemplateResponse(request=request, name="response.html", context={"chat_id": chat_id, "response": response.text})


class Item(BaseModel):
    chat_id: int
    prompt: str


@ app.post("/chat")
def read_chat(request: Request, item: Item):
    chat = chats[item.chat_id]
    response = chat.send_message(item.prompt)
    return {"response": response.text}
