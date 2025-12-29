import requests
import time
import datetime
import signal
import sys

colors = [(255,0,0), (0,0,255),(0,255,0)]
transition_steps = 20
sleep = 1
bulb_address = "192.168.0.107"
brightness = 50

def graceful_off():
    # reset
    r = requests.get(f"http://{bulb_address}/color/0?turn=on&mode=white&temp=4750&brightness=50")
    r = requests.get(f"http://{bulb_address}/color/0?turn=off&mode=white&temp=4750&brightness=50")

def signal_handler(sig, frame):
    graceful_off()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



def interpolate(x1: float, x2: float, y1: float, y2: float, x: float):
    """Perform linear interpolation for x between (x1,y1) and (x2,y2) """

    return y1 + (y2 - y1) * ((x - x1) / (x2 - x1))

def interpolate_color(color1, color2, nsteps,step):
    x = step / float(nsteps)
    r = round(interpolate(0, 1, color1[0], color2[0], x))
    g = round(interpolate(0, 1, color1[1], color2[1], x))
    b = round(interpolate(0, 1, color1[2], color2[2], x))
    return (r, g, b)



current_color = 0
while 1:
    next_color = (current_color+1) % len(colors)
    dt = datetime.datetime.now()
    if dt.hour >= 21:
        graceful_off()
        print("BYE")
        exit(0)
    for i in range(transition_steps):
        color = interpolate_color(colors[current_color], colors[next_color], transition_steps, i)
        r = requests.get(f"http://{bulb_address}/color/0?turn=on&mode=color&red={color[0]}&green={color[1]}&blue={color[2]}&gain={brightness}")
        print(f"{color[0]} {color[1]} {color[2]} {r.status_code}")
        
        time.sleep(sleep)
    current_color = (current_color+1) % len(colors)


