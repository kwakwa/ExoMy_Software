#!/usr/bin/env python
import rospy
from std_msgs.msg import String

import RPi.GPIO as GPIO
import time
import numpy as np

class Motors():
    '''
    Motors class contains all functions to control the steering and driving motors.
    ''' 

    # Define wheel names
    # rr- -rl
    # cr- -cl
    #    |
    # fr- -fl
    FL, FR, CL, CR, RL, RR = range(0, 6)

    def __init__(self):
        # Set the GPIO modes
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Set variables for the GPIO motor pins
        pin_drive_fr = 8 
        pin_steer_fr = 7

        pin_drive_fl = 12
        pin_steer_fl = 10

        pin_drive_cl = 11 
        pin_steer_cl = 16

        pin_drive_cr = 13 
        pin_steer_cr = 18

        pin_drive_rl = 36
        pin_steer_rl = 37

        pin_drive_rr = 33
        pin_steer_rr = 31


        # Set the GPIO Pin mode to be Output
        GPIO.setup(pin_drive_fl, GPIO.OUT)
        GPIO.setup(pin_steer_fl, GPIO.OUT)

        GPIO.setup(pin_drive_fr, GPIO.OUT)
        GPIO.setup(pin_steer_fr, GPIO.OUT)
                
        GPIO.setup(pin_drive_cl, GPIO.OUT)
        GPIO.setup(pin_steer_cl, GPIO.OUT)

        GPIO.setup(pin_drive_cr, GPIO.OUT)
        GPIO.setup(pin_steer_cr, GPIO.OUT)

        GPIO.setup(pin_drive_rl, GPIO.OUT)
        GPIO.setup(pin_steer_rl, GPIO.OUT)

        GPIO.setup(pin_drive_rr, GPIO.OUT)
        GPIO.setup(pin_steer_rr, GPIO.OUT)

        # PWM characteristics 
        pwm_frequency = 50 		# Hz
	self.steering_pwm_neutral =  [None] * 6

        self.steering_pwm_low_limit = 2.5#5 	# %
        self.steering_pwm_neutral[self.FL] = 7.0 # %
        self.steering_pwm_neutral[self.FR] = 6.2# %
        self.steering_pwm_neutral[self.CL] = 8.0 # %
        self.steering_pwm_neutral[self.CR] = 8.0 # %
        self.steering_pwm_neutral[self.RL] = 5.0 # %
        self.steering_pwm_neutral[self.RR] = 10.0 # %
        self.steering_pwm_upper_limit = 11.5#10	# %
        self.steering_pwm_range = 2.5

        self.driving_pwm_low_limit = 5.0#5 	# %
        self.driving_pwm_neutral = 7.0 			# %
        self.driving_pwm_upper_limit = 9.0#10	# %
        self.driving_pwm_range = 2.0

        # Set the GPIO to software PWM at 'Frequency' Hertz
        self.driving_motors = [None] * 6
        self.steering_motors = [None] * 6

        self.driving_motors[self.FL] = GPIO.PWM(pin_drive_fl, pwm_frequency)
        self.steering_motors[self.FL] = GPIO.PWM(pin_steer_fl, pwm_frequency)

        self.driving_motors[self.FR] = GPIO.PWM(pin_drive_fr, pwm_frequency)
        self.steering_motors[self.FR] = GPIO.PWM(pin_steer_fr, pwm_frequency)

        self.driving_motors[self.CL] = GPIO.PWM(pin_drive_cl, pwm_frequency)
        self.steering_motors[self.CL] = GPIO.PWM(pin_steer_cl, pwm_frequency)

        self.driving_motors[self.CR] = GPIO.PWM(pin_drive_cr, pwm_frequency)
        self.steering_motors[self.CR] = GPIO.PWM(pin_steer_cr, pwm_frequency)

        self.driving_motors[self.RL] = GPIO.PWM(pin_drive_rl, pwm_frequency)
        self.steering_motors[self.RL] = GPIO.PWM(pin_steer_rl, pwm_frequency)

        self.driving_motors[self.RR] = GPIO.PWM(pin_drive_rr, pwm_frequency)
        self.steering_motors[self.RR] = GPIO.PWM(pin_steer_rr, pwm_frequency)

	self.steering_motors[self.FL].start(self.steering_pwm_neutral[self.FL])
	time.sleep(0.5)
	self.steering_motors[self.FR].start(self.steering_pwm_neutral[self.FR])
	time.sleep(0.5)
	self.steering_motors[self.CL].start(self.steering_pwm_neutral[self.CL])
	time.sleep(0.5)
	self.steering_motors[self.CR].start(self.steering_pwm_neutral[self.CR])
	time.sleep(0.5)
	self.steering_motors[self.RL].start(self.steering_pwm_neutral[self.RL])
	time.sleep(0.5)
	self.steering_motors[self.RR].start(self.steering_pwm_neutral[self.RR])
	time.sleep(0.5)

        for motor in self.driving_motors:
            if motor is not None:
                motor.start(0.0)
                #motor.start(self.driving_pwm_neutral)
                time.sleep(0.5)

    def setSteering(self, steering_command):
        duty_cycle = self.steering_pwm_neutral[self.FL] + steering_command[self.FL]/90.0 * self.steering_pwm_range 
        self.steering_motors[self.FL].ChangeDutyCycle(duty_cycle)

        duty_cycle = self.steering_pwm_neutral[self.FR] + steering_command[self.FR]/90.0 * self.steering_pwm_range 
        self.steering_motors[self.FR].ChangeDutyCycle(duty_cycle)

        duty_cycle = self.steering_pwm_neutral[self.CL] + steering_command[self.CL]/90.0 * self.steering_pwm_range 
        self.steering_motors[self.CL].ChangeDutyCycle(duty_cycle)
        
        duty_cycle = self.steering_pwm_neutral[self.CR] + steering_command[self.CR]/90.0 * self.steering_pwm_range 
        self.steering_motors[self.CR].ChangeDutyCycle(duty_cycle)

        duty_cycle = self.steering_pwm_neutral[self.RL] + steering_command[self.RL]/90.0 * self.steering_pwm_range 
        self.steering_motors[self.RL].ChangeDutyCycle(duty_cycle)
        
        duty_cycle = self.steering_pwm_neutral[self.RR] + steering_command[self.RR]/90.0 * self.steering_pwm_range 
        self.steering_motors[self.RR].ChangeDutyCycle(duty_cycle)
            
    def setDriving(self, driving_command):
	if(driving_command[self.FL]==0.0):
		duty_cycle=0.0
	else:
	        duty_cycle = self.driving_pwm_neutral - driving_command[self.FL]/100.0 * self.driving_pwm_range 
	 
        self.driving_motors[self.FL].ChangeDutyCycle(duty_cycle)

	if(driving_command[self.FR]==0.0):
		duty_cycle=0.0
	else:
        	duty_cycle = self.driving_pwm_neutral + driving_command[self.FR]/100.0 * self.driving_pwm_range 
	
        self.driving_motors[self.FR].ChangeDutyCycle(duty_cycle)

	if(driving_command[self.CL]==0.0):
		duty_cycle=0.0
	else:
        	duty_cycle = self.driving_pwm_neutral - driving_command[self.CL]/100.0 * self.driving_pwm_range 
	
        self.driving_motors[self.CL].ChangeDutyCycle(duty_cycle)

	if(driving_command[self.CR]==0.0):
		duty_cycle=0.0
	else:
        	duty_cycle = self.driving_pwm_neutral + driving_command[self.CR]/100.0 * self.driving_pwm_range 
	 
        self.driving_motors[self.CR].ChangeDutyCycle(duty_cycle)

	if(driving_command[self.RL]==0.0):
		duty_cycle=0.0
	else:
        	duty_cycle = self.driving_pwm_neutral - driving_command[self.RL]/100.0 * self.driving_pwm_range 
	
        self.driving_motors[self.RL].ChangeDutyCycle(duty_cycle)

	if(driving_command[self.RR]==0.0):
		duty_cycle=0.0
	else:
	       	duty_cycle = self.driving_pwm_neutral + driving_command[self.RR]/100.0 * self.driving_pwm_range 
	
        self.driving_motors[self.RR].ChangeDutyCycle(duty_cycle)

    def stopMotors(self):
        for motor in self.driving_motors:
            if motor is not None:
                motor.ChangeDutyCycle(0.0)

    def cleanup(self):
        GPIO.cleanup()
