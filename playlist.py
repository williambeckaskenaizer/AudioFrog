from collections import deque
from song import Song
from random import shuffle

class Playlist:
    
    def __init__(self):
        self.song_queue = deque()
        self.playhistory = deque()
        
    def __len__(self):
        return len(self.song_queue)
    
    def add_song(self, song: Song):
        self.song_queue.append(song)
    
    def skip_song(self):
        self.song_queue.popleft()
        
    def shuffle(self):
        shuffle(self.song_queue)
        
    def next(self):

        if len(self.song_queue) == 0:
            return None

        if len(self.song_queue) == 0:
            return None

        if len(self.playhistory) > 10:
            self.playhistory.popleft()

        return self.song_queue[0]
        
    def get_songs(self):
        return self.song_queue