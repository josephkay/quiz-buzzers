from pynput import keyboard
from playsound import playsound
import sounddevice as sd
from time import sleep, time

class QuizHandler:
    def __init__(self):
        self.key = None
        self.current_round = None
        self.key_dict = {'shift': 'blue1', 'ctrl_l': 'blue2', 'shift_r': 'red1', 'ctrl_r': 'red2'}
        self.round_dict = {'1': 'record',
                           '2': 'play'}
        self.buzzer_dict = {'red1': None, 'red2': None, 'blue1': None, 'blue2': None}
        self.fs = 44100
        sd.default.samplerate = self.fs
        sd.default.channels = 2
    
    def start(self):
        while True:
            round_options = '''
            1: Record
            2: Play
            0: Exit
            Go: '''
            go = input(round_options)
            if go == '0':
                break
            elif go in self.round_dict:
                self.current_round = self.round_dict[go]
                self.play_buzzer()
    
    def play_buzzer(self):
        if self.current_round == 'play':
            while True:
                self.listen()
                if self.key == 'esc':
                    break
                elif self.key in self.buzzer_dict:
                    print(self.key)
                    clip_length = len(self.buzzer_dict[self.key])/self.fs
                    sd.play(self.buzzer_dict[self.key], self.fs)
                    sleep(clip_length + 1)
                
        elif self.current_round == 'record':
            while True:
                self.listen()
                if self.key == 'esc':
                    break
                print(f'Recording: {self.key}')
                player_recording = self.key
                rec = sd.rec(10 * self.fs)
                while True:
                    self.listen()
                    start_time = time()
                    if self.key == player_recording or self.key == 'esc':
                        sd.stop()
                        clip_length = time() - start_time
                        frame_length = int(self.fs * clip_length) * 10
                        self.buzzer_dict[player_recording] = rec[5000:frame_length-2000]
                        print('Recording stopped')
                        break
    
    def listen(self):
        lis = keyboard.Listener(on_press=self.get_one_key)
        lis.start()
        lis.join()
    
    def get_one_key(self, key):
        try: k = key.char
        except: k = key.name
        if key == keyboard.Key.esc:
            self.key = 'esc'
            return False
        elif k in self.key_dict:
            self.key = self.key_dict[k]
            return False
    
    def play(self, filename):
        playsound(f'wavs/{filename}')

quiz = QuizHandler()

quiz.start()
