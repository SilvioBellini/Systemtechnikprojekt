from enum import Enum

class Config:
    """
    Class to store globally used values.
    """
    
    def __init__(self):
        # Network
        self.username = "team2"
        self.password = "rHGpIGxo0o1k"
        self.topic = "team2_4/test"

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
        self.pwmChGreen = 5
        self.pwmChBlue = 3

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
        self.tn = 0.011                  # 0.011   # 0.1
        self.ticksPerRotation = 256      # 256     # 100
        self.gearRatio = 152/1            # 152/1   # 16/1
        self.motorVoltage = 5
        self.pwmMotorFreq = 50

        # LED config
        self.pwmLedFreq = 10000

        # Sensor values
        self.amountOfIRSensors = 7 

        self.valueBlack0 = 200
        self.valueBlack1 = 200
        self.valueBlack2 = 200
        self.valueBlack3 = 200
        self.valueBlack4 = 200
        self.valueBlack5 = 200

        self.minValueWhite0 = 1000
        self.minValueWhite1 = 1000
        self.minValueWhite2 = 1000
        self.minValueWhite3 = 1000
        self.minValueWhite4 = 1000
        self.minValueWhite5 = 1000
        self.minValueGrey = 1900
        self.minValueObstacle = 2000

        # Default Values
        self.defaultSpeedSlow = 0.04
        self.defaultSpeed = 0.05
        self.defaultSpeedFast = 0.05
        self.defaultVolume = 25
        
        # Enums
        self.Directions = Enum("Directions", ["Perpendicular", "Parallel"])
        self.BGMs = Enum("BGM", ["RANDOM_BEAT", "DUBSTEP", "GINTRONIC"])
        self.SFXs = Enum("SFX", ["IGNITION", "APPROVAL_KITCHEN", "APPROVAL_COUNTER", "GOODBYE", "VROOM", "CROWD"])

        # Call by: self.bgm[self.BGMs.RANDOM_BEAT]
        self.bgm = {
            self.BGMs.RANDOM_BEAT: 1,
            self.BGMs.DUBSTEP: 2,
            self.BGMs.GINTRONIC : 3
        }

        # Call by: self.sfx[self.SFXs.IGNITION]
        self.sfx = {
            self.SFXs.IGNITION: 1,
            self.SFXs.APPROVAL_KITCHEN: 2,
            self.SFXs.APPROVAL_COUNTER: 3,
            self.SFXs.GOODBYE: 4,
            self.SFXs.VROOM: 5,
            self.SFXs.CROWD: 6
        }

    def setValueWhite0(self, valueBlack, valueWhite):
        self.valueBlack0 = valueBlack
        self.minValueWhite0 = valueWhite

    def setValueWhite1(self, valueBlack, valueWhite):
        self.valueBlack1 = valueBlack
        self.minValueWhite1 = valueWhite
    
    def setValueWhite2(self, valueBlack, valueWhite):
        self.valueBlack2 = valueBlack
        self.minValueWhite2 = valueWhite

    def setValueWhite3(self, valueBlack, valueWhite):
        self.valueBlack3 = valueBlack
        self.minValueWhite3 = valueWhite

    def setValueWhite4(self, valueBlack, valueWhite):
        self.valueBlack4 = valueBlack
        self.minValueWhite4 = valueWhite

    def setValueWhite5(self, valueBlack, valueWhite):
        self.valueBlack5 = valueBlack
        self.minValueWhite5 = valueWhite