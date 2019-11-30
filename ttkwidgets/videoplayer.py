import tkinter as tk
import tkinter.ttk as ttk
import ffmpeg
from PIL import Image, ImageTk


class VideoPlayer(tk.Canvas):
    def __init__(self, master=None, filename=None, framerate=25, **kwargs):
        super().__init__(master, **kwargs)
        if filename is None:
            raise TypeError()
        self._video = ffmpeg.input(filename)
        probe = ffmpeg.probe(filename)
        self.info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        self.v_width, self.v_height = self.info['width'], self.info['height']
        if isinstance(framerate, int):
            self._video = self._video.filter_('fps', fps=framerate)
            self.framerate = framerate
            self.n_frames = int(float(self.info['duration']) * framerate)
        elif framerate == 'original':
            self.framerate = int(self.info['r_frame_rate'].split('/')[0])
            self.n_frames = int(self.info['nb_frames'])
        
        print(self.framerate, self.n_frames)
        self.config(width=self.v_width, height=self.v_height)
        
        def get_byte(i):
            out, _ = (
                self._video
                .filter_('select', 'gte(n,{})'.format(i))
                .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=1)
                .run(capture_stdout=True, capture_stderr=True)
            )
            return out
        
        self.frames = [get_byte(i) for i in range(1, self.n_frames)]
        self.current_frame = 0
        
    @property
    def video_frame_delay(self):
        """ Returns the delay between two frames in milliseconds """
        return int(1.0 / self.framerate * 1000)
    
    def get_frame(self):
        if self.current_frame < len(self.frames):
            frame = self.frames[self.current_frame]
            return ImageTk.PhotoImage(image=Image.frombytes(mode='RGB', size=(self.v_width, self.v_height), data=frame))
        else:
            frame = self.frames[-1]
            return ImageTk.PhotoImage(image=Image.frombytes(mode='RGB', size=(self.v_width, self.v_height), data=frame))
    
    def start_video_playback(self):
        self.current_frame += 1
        self.frame = self.get_frame()
        self.delete('video_frames')
        self.create_image((0, 0), anchor=tk.NW, image=self.frame, tags='video_frames')
        self.after(self.video_frame_delay, self.start_video_playback)


if __name__ == '__main__':
    root = tk.Tk()
    vp = VideoPlayer(root, filename='dist/test.mp4', framerate=5)
    vp.pack()
    vp.start_video_playback()
    root.mainloop()
