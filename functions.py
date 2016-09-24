import numpy as np
import librosa
import pygame
import time

NOTES = ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'a6', 'b6', 'c6', 'd6',
         'e6', 'f6', 'g6', 're']
PITCHES = [-15, -13, -12, -10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19]
LENGTH_STRINGS = ['1', '2', '4', '8', '16', '32']
LENGTHS = [4.0, 2.0, 1.0, 0.5, 0.25, 0.125]
for i in range(len(PITCHES)):
    PITCHES[i] += 0
print(LENGTHS)


def create_sounds(audio_path, semitone_arr, length_arr):
    y, sr = librosa.load(audio_path)
    buffer_arr = [[[] for l in length_arr] for s in semitone_arr]
    for i in range(len(semitone_arr)):
        buffer_arr[i][0] = librosa.effects.pitch_shift(y, sr, semitone_arr[i])
        for j in range(len(length_arr)):
            length = length_arr[j]
            buffer_arr[i][j] = librosa.effects.time_stretch(buffer_arr[i][0], 1/length)
    sound_arr = [[[] for l in length_arr] for s in semitone_arr]
    for i in range(len(semitone_arr)):
        for j in range(len(length_arr)):
            temp_arr = librosa.util.buf_to_int(buffer_arr[i][j], 1)
            sound_arr[i][j] = pygame.sndarray.make_sound(temp_arr)
    return sound_arr


def play_note(sound_arr, pitch_index, length_index):
    sound_arr[pitch_index][length_index].play()


def interpret_note(sound_arr, note_string):
    pitch_index = NOTES.index(note_string[0:2])
    length_index = LENGTH_STRINGS.index(note_string[3:])
    if pitch_index == len(NOTES)-1:
        time.sleep(sound_arr[0][length_index].get_length())
    else:
        play_note(sound_arr, pitch_index, length_index)


def correct_length(audio_path):
    y, sr = librosa.load(audio_path)
    length = librosa.audio.get_duration(y, sr)
    change = 1.5
    for i in range(len(LENGTHS)):
        LENGTHS[i] /= change


def startup(audio_path, song_path):
    correct_length(audio_path)
    pygame.mixer.init(22050, -16, 1, 4096)
    screen = pygame.display.set_mode((640, 480))
    sound_arr = create_sounds(audio_path, PITCHES, LENGTHS)
    song_file = open(song_path, 'r')
    song_notes = song_file.read().splitlines()
    return song_notes, sound_arr


def play_song(audio_path, song_path):
    notes, sounds = startup(audio_path, song_path)
    for note in notes:
        if len(note) > 0:
            interpret_note(sounds, note)
        while pygame.mixer.get_busy():
            time.sleep(0.05)