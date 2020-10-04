from sanic import Sanic
from sanic.response import json

# utils
from datetime import datetime
from .weather import Weather
from .meme import Meme

app = Sanic(name="setio")

@app.route("/")
@app.route("/<path:string>")
async def index(request, path=""):
    return json({"hello": path})

@app.route("/weather/<city_id:string>")
async def weather(request, city_id=""):
    weather = Weather.Get(city_id)

    dt = datetime.now().strftime("%B %d, %Y | %I:%M %p")

    if weather[0] != "404":
        __message = {
            "messages": [
                {"text": f"Weather for *{weather[0]}, {weather[1]}* | ({dt}) \n\nIt feels like *{weather[5]}°C* ({weather[4]}°C).\n\nThe weather is *{weather[2]}* ({weather[3]}) with a maximum temperature of *{weather[7]}°C* and a minimum temperature of *{weather[6]}°C*."}
            ]
        }
    else:
        __message = {
            "messages": [
                {"text": "Sorry but that city or municipality cannot be found."}
            ]
        }

    return json(__message)

@app.route("/meme", methods=["POST"])
async def meme(request):
    fb_id = request.args['messenger user id']
    
    meme = Meme.Get(fb_id)

    if meme:
        return json({
            "messages": [
                {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": meme
                        }
                    }
                }
            ]
        })

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)