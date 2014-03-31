"""Test PsychoPy sound.py using pyo backend
"""

from psychopy import prefs, core
prefs.general['audioLib'] = ['pyo']

import pytest
from scipy.io import wavfile
import shutil, os
from tempfile import mkdtemp
from psychopy import sound, microphone

import numpy

# py.test --cov-report term-missing --cov sound.py tests/test_sound/test_sound_pyo.py

from psychopy.tests.utils import TESTS_PATH, TESTS_DATA_PATH

@pytest.mark.needs_sound
class TestPyo(object):
    @classmethod
    def setup_class(self):
        self.contextName='pyo'
        try:
            assert sound.Sound == sound.SoundPyo
        except:
            pytest.xfail('need to be using pyo')
        self.tmp = mkdtemp(prefix='psychopy-tests-sound')

        # ensure some good test data:
        testFile = 'green_48000.flac.dist'
        new_wav = os.path.join(self.tmp, testFile.replace('.dist', ''))
        shutil.copyfile(os.path.join(TESTS_DATA_PATH, testFile), new_wav)
        w = microphone.flac2wav(new_wav)
        r, d = wavfile.read(w)
        assert r == 48000
        assert len(d) == 92160

    @classmethod
    def teardown_class(self):
        if hasattr(self, 'tmp'):
            shutil.rmtree(self.tmp, ignore_errors=True)

    def test_init(self):
        for note in ['A', 440, '440', [1,2,3,4], numpy.array([1,2,3,4])]:
            sound.Sound(note, secs=.1)
        with pytest.raises(ValueError):
            sound.Sound('this is not a file name')
        with pytest.raises(ValueError):
            sound.Sound(-1)
        with pytest.raises(ValueError):
            sound.Sound(440, secs=-1)
        with pytest.raises(ValueError):
            sound.Sound(440, secs=0)
        with pytest.raises(DeprecationWarning):
            sound.setaudioLib('foo')

        points = 100
        snd = numpy.ones(points) / 20

        testFile = os.path.join(self.tmp, 'green_48000.wav')
        s = sound.Sound(testFile)

    def test_play(self):
        s = sound.Sound(secs=0.1)
        s.play()
        core.wait(s.getDuration()+.1)  # allows coverage of _onEOS
        s.play(loops=1)
        core.wait(s.getDuration()*2+.1)
        s.play(loops=-1)
        s.stop()

    def test_methods(self):
        s = sound.Sound(secs=0.1)
        v = s.getVolume()
        assert v == 1
        s.setVolume(0.5)
        assert s.getVolume() == 0.5
        s.setLoops(2)
        assert s.getLoops() == 2

    def test_reinit_pyo(self):
        sound.initPyo()

    def test_sound_output(self):
        # play a sound while also recording via microphone
        # get FFT of the recorded sound, analyze it
        pass
