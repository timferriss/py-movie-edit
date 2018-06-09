'''
Author: Garren Ijames

'''
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os, math, random, datetime, shutil

from snipper import snip_clips, weird_colors

TRY_COUNT = 0

class Edit:

    MOVIE_PATH = '/Users/gmanjames/Desktop/videos'

    STAGING_DIR = '/Users/gmanjames/Desktop/videos/staging'

    BACKUP_DIR = '/Users/gmanjames/Desktop/videos/backup'

    MAX_LEN = 60

    IGNORE = [
        '.',
        '..',
        '.DS_STORE',
        'backup',
        'staging'
    ]




    def __init__( self, first_phrase, secon_phrase ):
        self.first_phrase = first_phrase
        self.secon_phrase = secon_phrase


    def _get_clips( self ):
        vids_for_first = [f for f in os.listdir(Edit.MOVIE_PATH + '/' + self.first_phrase) if 'mp4' in f]
        vids_for_secon = [f for f in os.listdir(Edit.MOVIE_PATH + '/' + self.secon_phrase) if 'mp4' in f]
        first_vid_index = random.randint(0, len(vids_for_first) - 1)
        secon_vid_index = random.randint(0, len(vids_for_secon) - 1)

        while first_vid_index == secon_vid_index:
            secon_vid_index = random.randint(0, len(vids_for_secon) - 1)

        return [ vids_for_first[first_vid_index], vids_for_secon[secon_vid_index] ]

    def _backup( self ):
        backup_file = Edit.BACKUP_DIR + '/' + datetime.datetime.now().strftime('%Y%m%d_%M_%S_%f')

        # make a backup if something is in staging
        upload_exists = len(os.listdir(Edit.STAGING_DIR)) == 1
        if upload_exists:
            shutil.move(Edit.STAGING_DIR + '/upload.mp4', backup_file)


    def create( self ):
        clips = self._get_clips()
        print('first:', clips[0], '-', 'second:', clips[1])
        clip1 = VideoFileClip(Edit.MOVIE_PATH + '/' + self.first_phrase + '/' + clips[0])
        clip2 = VideoFileClip(Edit.MOVIE_PATH + '/' + self.secon_phrase + '/' + clips[1])

        clip1 = clip1.fl_image( weird_colors )
        
        # all of the subclips to stitch together
        snips = snip_clips(clip1, clip2, 2, 15)

        self._backup()

        final_clip = concatenate_videoclips(snips)
        final_clip.write_videofile(Edit.STAGING_DIR + '/upload.mp4', audio_codec="aac")





def run_edit():
    phrases = [f for f in os.listdir(Edit.MOVIE_PATH) if not f in Edit.IGNORE]
    first_index = random.randint(0, len(phrases) - 1)
    secon_index = random.randint(0, len(phrases) - 1)

    while first_index == secon_index:
        secon_index = random.randint(0, len(phrases) - 1)

    first_phrase = phrases[first_index]
    secon_phrase = phrases[secon_index]
    edit = Edit( first_phrase, secon_phrase )

    edit.create()


def main():
    try:
        run_edit()
    except:
        global TRY_COUNT
        if TRY_COUNT < 5:
            TRY_COUNT += 1
            main()
        else:
            print('errorred out')

if __name__ == '__main__':
    main()

