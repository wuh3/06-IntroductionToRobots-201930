"""
A simple version of part of the RoseBot class that you will implement
in your Capstone project.
"""

import ev3dev.ev3 as ev3
import time
import math


###############################################################################
#    RoseBot class.
#
# NOTE TO STUDENTS:
#   You should construct a RoseBot for the Snatch3r robot.
#   Do ** NOT ** construct any instances of any other classes in this module,
#   since a RoseBot constructs instances of all the sub-systems that provide
#   ALL of the functionality available to a Snatch3r robot.
#
#   Use those sub-systems (and their instance variables)
#   to make the RoseBot (and its associated Snatch3r robot) do things.
###############################################################################
class RoseBot(object):
    def __init__(self):
        # Use these instance variables
        self.drive_system = DriveSystem()
        # self.sound_system = SoundSystem()

###############################################################################
#    DriveSystem
###############################################################################
class DriveSystem(object):
    def __init__(self):
        """ Constructs two Motors (for the left and right wheels). """
        self.left_motor = Motor('B')
        self.right_motor = Motor('C')

###############################################################################
#    SoundSystem
###############################################################################
class SoundSystem(object):
    """
    Has all the kinds of "noise makers" available to the Snatch3r robot.
    Use this object to make   ** any **   sounds.
    """

    def __init__(self, beeper, tone_maker, speech_maker, song_maker):
        self.beeper = beeper
        self.tone_maker = tone_maker
        self.speech_maker = speech_maker
        self.song_maker = song_maker


###############################################################################
###############################################################################
# Classes built directly upon the underlying EV3 robot modules.
# USE them, and AUGMENT them if you wish, but do NOT modify them.
#
# In the DriveSystem:
#   -- Motor
#
# In the SoundSystem:
#   -- Beeper
#   -- ToneMaker
#   -- SpeechMaker
#   -- SongPlayer
#
###############################################################################
###############################################################################
class Motor(object):
    def __init__(self, port, motor_type='large'):
        # port must be 'A', 'B', 'C', or 'D'.  Use 'arm' as motor_type for Arm.
        if motor_type == 'large':
            self._motor = ev3.LargeMotor('out' + port)
        elif motor_type == 'medium':
            self._motor = ev3.MediumMotor('out' + port)

    def turn_on(self, speed):
        """ speed must be -100 to 100 """
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0


class Beeper(object):
    def __init__(self):
        self._beeper = ev3.Sound

    def beep(self):
        """
        Starts playing a BEEP sound.

        Does NOT block, that is, continues immediately to the next statement
        while the sound is being played. Returns a subprocess.Popen,
        so if you want the sound-playing to block until the sound is completed
        (e.g. if the next statement will immediately make another sound),
        then use   beep  like this:
             beeper = Beeper()
             beeper.beep().wait()

        :rtype subprocess.Popen
        """
        return self._beeper.beep()


class ToneMaker(object):
    def __init__(self):
        self._tone_maker = ev3.Sound

    def play_tone(self, frequency, duration):
        """
        Starts playing a tone at the given frequency (in Hz) for the given
        duration (in milliseconds).

        Does NOT block, that is, continues immediately to the next statement
        while the sound is being played. Returns a subprocess.Popen,
        so if you want the sound-playing to block until the sound is completed
        (e.g. if the next statement will immediately make another sound),
        then use   tone  like this:
             tone_player = ToneMaker()
             tone_player.play_tone(400, 500).wait()

        :rtype subprocess.Popen
        """
        return self._tone_maker.tone(frequency, duration)

    def play_tone_sequence(self, tones):
        """
        Starts playing a sequence of tones, where each tone is a 3-tuple:
          (frequency, duration, delay_until_next_tone_in_sequence)
        Does NOT block; see   play_tone  above.

        Here is a cheerful example, from the ev3 documentation::
            tone_player = ToneMaker()
            tone_player.play_tone_sequence([
        (392, 350, 100), (392, 350, 100), (392, 350, 100), (311.1, 250, 100),
        (466.2, 25, 100), (392, 350, 100), (311.1, 250, 100), (466.2, 25, 100),
        (392, 700, 100), (587.32, 350, 100), (587.32, 350, 100),
        (587.32, 350, 100), (622.26, 250, 100), (466.2, 25, 100),
        (369.99, 350, 100), (311.1, 250, 100), (466.2, 25, 100),
        (392, 700, 100),
        (784, 350, 100), (392, 250, 100), (392, 25, 100), (784, 350, 100),
        (739.98, 250, 100), (698.46, 25, 100), (659.26, 25, 100),
        (622.26, 25, 100), (659.26, 50, 400), (415.3, 25, 200),
        (554.36, 350, 100),
        (523.25, 250, 100), (493.88, 25, 100), (466.16, 25, 100),
        (440, 25, 100),
        (466.16, 50, 400), (311.13, 25, 200), (369.99, 350, 100),
        (311.13, 250, 100), (392, 25, 100), (466.16, 350, 100),
        (392, 250, 100),
        (466.16, 25, 100), (587.32, 700, 100), (784, 350, 100),
        (392, 250, 100),
        (392, 25, 100), (784, 350, 100), (739.98, 250, 100),
        (698.46, 25, 100),
        (659.26, 25, 100), (622.26, 25, 100), (659.26, 50, 400),
        (415.3, 25, 200),
        (554.36, 350, 100), (523.25, 250, 100), (493.88, 25, 100),
        (466.16, 25, 100), (440, 25, 100), (466.16, 50, 400),
        (311.13, 25, 200),
        (392, 350, 100), (311.13, 250, 100), (466.16, 25, 100),
        (392.00, 300, 150), (311.13, 250, 100), (466.16, 25, 100), (392, 700)
        ]).wait()

          :rtype subprocess.Popen
        """
        return self._tone_maker.tone(tones)


class SpeechMaker(object):
    def __init__(self):
        self._speech_maker = ev3.Sound

    def speak(self, phrase):
        """
        Speaks the given phrase aloud.
        The phrase must be short.

        Does NOT block, that is, continues immediately to the next statement
        while the sound is being played. Returns a subprocess.Popen,
        so if you want the sound-playing to block until the sound is completed
        (e.g. if the next statement will immediately make another sound),
        then use   speak  like this:
             speech_player = SpeechMaker()
             speech_player.speak().wait()

        :type  phrase:  str
        :rtype subprocess.Popen
        """
        return self._speech_maker.speak(phrase)