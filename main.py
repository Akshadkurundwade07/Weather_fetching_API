from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="Weather App")

API_KEY = "b8f928c896083dac3033c44ad7728a87"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.get("/")
def home():
    return {"message": "Weather App is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/weather/{city}")
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key")

    data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }