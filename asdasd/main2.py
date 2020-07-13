## В разработке) Но ето работает можно потестить
import pyowm
city = input("Какой город вас интересует🏙?: ")
owm = pyowm.OWM('517eb41f1720be4a8afc801586d2b54f')  # You MUST provide a valid API key

# Search for current weather in London (Great Britain)
mgr = owm.weather_manager()
observation = mgr.weather_at_place('{},RU'.format(city))
w = observation.weather
temperature = w.temperature('celsius')['temp']

temperature2 = w.detailed_status
print("В городе " + city + " сейчас температура: " + str(temperature) +"°C, "+(str(temperature2)))

