import pyb, sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)     # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False) # must turn this off to prevent image washout...
clock = time.clock()

uart = pyb.UART(3, 9600, timeout_char=1000)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)

while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        uart.write(("Tag ID %d; " % tag.id()).encode())
    uart.write(("FPS %f\r\n" % clock.fps()).encode())
