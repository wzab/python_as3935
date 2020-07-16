import as3935
import machine
import micropython
micropython.alloc_emergency_exception_buf(100)
irq_pin = machine.Pin('B9',machine.Pin.IN, machine.Pin.PULL_UP)
i2 = machine.I2C(1)
address = 0x0  # If using MOD-1016 this is the address
sensor = as3935.AS3935(irq_pin, i2, address)

# We need to calibrate the sensor first. Use the tuning cap provided
# or calculate it using sensor.calculate_tuning_cap(*args)
sensor.full_calibration(0)

sensor.set_indoors(True)


# Every time you sense a pulse on IRQ it means there is an
# interruption request. You can read it like this:
def irq_callback(gpio):
    interruption = sensor.get_interrupt()
    if interruption == as3935.INT_NH:
        print("Noise floor too high")
    elif interruption == as3935.INT_D:
        print("Disturbance detected. Mask it?")
    elif interruption == as3935.INT_L:
        print("Lightning detected!")
        distance = sensor.get_distance()
        print("Distance="+str(distance))        


try:
    irq_pin.irq(irq_callback)
    while True:
        pass
finally:
    irq_pin.irq(None)

