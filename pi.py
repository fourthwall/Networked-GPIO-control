import RPi.GPIO as GPIO
import time
import socket
import sys
import re
pattern = re.compile('([0-9,])+(:[0-9]+)')
def runsequence(name):
    if not name in sequences:
        print("Sequence not found")
        return
    GPIO.setmode(GPIO.BOARD)
    for line in sequences[name]:
        for pin in line[0]:
            print("Setting up pin: " + str(pin))
            GPIO.setup(pin, GPIO.OUT)
        for x in (GPIO.HIGH, GPIO.LOW):
            for pin in line[0]:
                GPIO.output(pin, x)
            if x == GPIO.HIGH:
                time.sleep(line[1] /1000)
    GPIO.cleanup()


with open('config.txt') as f:
    sequences = {}
    lines = []
    name = None
    l = [x.rstrip().lstrip() for x in f.readlines() if x != ""]
    for line in l:
        if line.endswith(" {") and not name:
            name = line[:-2].rstrip()
            if name == "":
                sys.exit("Empty block name")
            if len(name) > 25:
                sys.exit(name + " longer than 25 chars")
        elif name and pattern.match(line):
            split = line.split(":")
            lines.append(([int(i) for i in split[0].split(",")], int(split[1])))
        elif line == "}" and lines:
            sequences[name] = lines
            name = None
            lines = []
        else:
            sys.exit("Parse error: " + l)
    if not sequences:
        sys.exit("Blank configuration file")

ip = "0.0.0.0"
port = 1692
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))
while True:
    data, addr = sock.recvfrom(30)
    print("got request for " + data)
    if len(data) < 30:
        runsequence(str(data))
