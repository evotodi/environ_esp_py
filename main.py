def connectToWifiAndUpdate():
    import time
    import machine
    import network
    import gc
    import app.secrets as secrets
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from app.ota_updater.ota_updater import OTAUpdater

    # noinspection PyUnresolvedReferences
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/evotodi/environ_esp_py', main_dir='app', secrets_file="secrets.py", unstableVersions=True)
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del otaUpdater
        gc.collect()

def startApp():
    # noinspection PyUnresolvedReferences
    import app.start


connectToWifiAndUpdate()
startApp()
