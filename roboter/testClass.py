import flink
import driver

class TestClass:
    
    def testAudio(self):
        audio.selectDevice()
        audio.setVolume(10)
        audio.playAudioClip(1, 3)            
        time.sleep(15)
        audio.pause()