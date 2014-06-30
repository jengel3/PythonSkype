from util.plugin import command
from util import http
import json
import config as config


auto_complete = 'http://autocomplete.wunderground.com/aq?query=%s'
forecast_api = "http://api.wunderground.com/api/%s/forecast/q/zmw:%s.json"


@command(name='weather', help='Get the weather of an area.')
def weather_command(chat, message, args, sender):
    if len(args) == 0:
        chat.SendMessage("You must specify a location.")
        return
    json_data = json.loads(http.get_url_data(auto_complete % args[0]))
    results = json_data['RESULTS']
    if results is None or len(results) == 0:
        chat.SendMessage("No match found for %s." % args[0])
        return
    location = results[0]['name']
    zmw = results[0]['zmw']
    response = get_forecast(zmw, location)
    if response is None:
        return
    chat.SendMessage(response)


def get_forecast(zmw, loc):
    conf = config.config()
    key = conf.get("keys", {}).get("wunderground", None)
    if key is None:
        return None
    url = forecast_api.format(key, zmw)
    data = json.loads(http.get_url_data(url))
    forecast = data['forecast']
    simple_forecast = forecast['simpleforecast']
    day_forecast = simple_forecast['forecastday'][0]
    low = day_forecast['low']
    low_far = low['fahrenheit']
    low_cel = low['celsius']
    high = day_forecast['high']
    high_far = high['fahrenheit']
    high_cel = high['celsius']
    conditions = day_forecast['conditions']
    humidity = day_forecast['avehumidity']
    return "%s - Sky Conditions: %s | Temps - High: %sF/%sC | Low: %sF/%sC | Humidity: %s" % (loc, conditions,
                                                                                              high_far,
                                                                                              high_cel, low_far,
                                                                                              low_cel,
                                                                                              humidity)

