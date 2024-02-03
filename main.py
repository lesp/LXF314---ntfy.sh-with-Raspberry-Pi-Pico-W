import machine, onewire, ds18x20, time
import network
import urequests as requests

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("WIFI SSD HERE","YOUR PASSWORD")
time.sleep(5)
print(wlan.isconnected())

ds_pin = machine.Pin(0)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()

while True:
    ds_sensor.convert_temp()
    time.sleep(1)
    for rom in roms:
        temp_c = ds_sensor.read_temp(rom)
        print(temp_c)
        temperature = str(temp_c)+" C"
        requests.post("https://ntfy.sh/lxf-temp",
                      data=temperature,
                      headers={
                          "Title": "Hourly Temperature Check",
                          "Priority": "5",
                          "Tags": "thermometer",
                          })
    time.sleep(3600)