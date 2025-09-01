import time
import RPi.GPIO as GPIO
import adafruit_dht
import board

# Пины (меняй под своё подключение)
FAN_PIN = 18       # Вентилятор
LED_PIN = 23       # Индикатор
DHT_PIN = board.D4 # DHT22 датчик

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# Настройка датчика
dht = adafruit_dht.DHT22(DHT_PIN)

try:
    while True:
        try:
            temp = dht.temperature
            hum = dht.humidity

            if temp is not None and hum is not None:
                print(f"Температура: {temp:.1f}°C  Влажность: {hum:.1f}%")

                # Условие включения вентиляции
                if temp > 28 or hum > 70:
                    GPIO.output(FAN_PIN, GPIO.HIGH)
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    print("Вентиляция ВКЛ")
                else:
                    GPIO.output(FAN_PIN, GPIO.LOW)
                    GPIO.output(LED_PIN, GPIO.LOW)
                    print("Вентиляция ВЫКЛ")
            else:
                print("Ошибка чтения данных с датчика")

        except RuntimeError as e:
            print("Ошибка DHT22:", e)

        time.sleep(2)

except KeyboardInterrupt:
    print("Завершение программы")

finally:
    GPIO.cleanup()
