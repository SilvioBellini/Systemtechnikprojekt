import flink
import driver

class TestClass:
    """
    Class for testing parts of the robot(speakers, servos, etc.)
    """
    def testAudio(self):
        """
        function to play music on the speaker
        """
        audio.selectDevice()
        audio.setVolume(10)
        audio.playAudioClip(1, 3)            
        time.sleep(15)
        audio.pause()
    