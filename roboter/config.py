from enum import Enum

class Config:
    """
    Class to store globally used values.
    """
    def __init__(self):
        # Network
        self.username = "team2"
        self.password = "rHGpIGxo0o1k"
        self.topic = "team1_2/test"

        # GPIO Channels
        self.gpioChStop = 0
        self.gpioChStart = 2

        self.gpioChMode1 = 4
        self.gpioChMode2 = 6
        self.gpioChMode4 = 8
        self.gpioChMode8 = 10

        self.gpioChLimitSwitchGripper = 13
        self.gpioChLimitSwitchHopper = 15

        self.gpioChSleepDrive = 16
        self.gpioChEnableServo = 18

        self.gpioChSensorBottle = 21
        self.gpioChSensorGlass = 23

        # PWM Channels
        self.pwmChLeftA = 2
        self.pwmChLeftB = 0
        self.pwmChRightA = 6
        self.pwmChRightB = 4

        self.pwmChRed = 1
        self.pwmChGreen = 3
        self.pwmChBlue = 5

        self.pwmChFill = 10
        self.pwmChGrip = 12

        # FQD Channels
        self.fqdChLeft = 0
        self.fqdChRight = 1

        # UART Channels
        self.uartChAudio = 0

        # Motor config
        self.ts = 0.01
        self.kp = 0.1
        self.tn = 0.01                  # 0.011   # 0.1
        self.ticksPerRotation = 100      # 256     # 100
        self.gearRatio = 16/1            # 152/1   # 16/1
        self.motorVoltage = 5
        self.pwmMotorFreq = 50

        # LED config
        self.pwmLedFreq = 10000

        # Sensor values
        self.amountOfIRSensors = 7 
        self.minValueWhite = 1000
        self.minValueGrey = 600

        # Default Values
        self.defaultSpeed = 0.03
        self.defaultVolume = 25
        
        # Enums
        self.Directions = Enum("Directions", ["Perpendicular", "Parallel"])
        self.BGMs = Enum("BGM", ["RANDOM_BEAT"])
        self.SFXs = Enum("SFX", ["IGNITION", "APPROVAL_KITCHEN", "APPROVAL_COUNTER", "GOODBYE"])

        # Call by: self.bgm[self.BGMs.RANDOM_BEAT]
        self.bgm = {
            self.BGMs.RANDOM_BEAT: 1
        }

        # Call by: self.sfx[self.SFXs.STARTUP]
        self.sfx = {
            self.SFXs.IGNITION: 1,
            self.SFXs.APPROVAL_KITCHEN: 2,
            self.SFXs.APPROVAL_COUNTER: 3,
            self.SFXs.GOODBYE: 4
        }