import requests
import time
import json
import logging
from quixstreams import Application


def get_weather():
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 35.44,
            "longitude": 24.19,
            "current": "temperature_2m",
        },
    )

    return response.json()


def main():
    app = Application(
        broker_address="localhost:9092",
        loglevel="DEBUG",
    )

    with app.get_producer() as producer:
        while True:
            weather = get_weather()
            logging.debug("Got weather: %s", weather)
            producer.produce(
                topic="weather_data_demo",
                key="Almyrida",
                value=json.dumps(weather),
            )
            logging.info("Produced. Sleeping...")
            time.sleep(10)

# in a terminal:
# kcat -b localhost:9092 -C -t weather_data_demo -o end
if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()