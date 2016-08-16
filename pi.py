import RPi.GPIO as GPIO
import time
def runsequence(name):
	GPIO.setmode(GPIO.BOARD)
	
	for line in sequences[name]:
		for pin in line[0]:
			GPIO.setup(pin, GPIO.OUT)
		for x in (GPIO.HIGH, GPIO.LOW):
			for pin in line[0]:
				GPIO.output(pin, x)
			if x == GPIO.HIGH:
				time.sleep(line[1] * 100)
	GPIO.cleanup()

with open('config.txt') as f:
    reading = False
    sequences = {}
    l = [x.rstrip().lstrip() for x in f.readlines() if x != ""]
    for line in l:
        if reading:
            if line == "}":
                if not lines:
                    sys.exit("Empty block: " + name)
                reading = False
                sequences[name] = lines
                lines = []
            else:
                if not pattern.match(line):
                    sys.exit("Malformed entry: " + line)
                split = line.split(":")
                lines.append(([int(i) for i in split[0].split(",")], int(split[1])))
            continue
 
        if not reading and line.endswith(" {"):
            reading = True
            name = line[:-2].rstrip()
			if name == "":
				sys.exit("Empty block name")
			if len(name) > 25:
				sys.exit(name + " longer than 25 chars")
        else:
            sys.exit("Cannot locate block for " + line)
	if sequences.isempty():
		sys.exit("Blank configuration file")




