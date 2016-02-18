class moviewriter :

    enabled = True

    def __init__(self, fig, name, enabled=True, fps=15, dpi=100) :
        self.enabled = enabled
        if enabled :
            import matplotlib.animation as animation
            FFMpegWriter = animation.writers['ffmpeg']
            self.movie_writer = FFMpegWriter(fps=fps)
            self.movie_writer.setup(fig, '.'.join((name,'mp4')), dpi=dpi)

    def update(self) :
        if self.enabled :
            self.movie_writer.grab_frame()

    def finish(self) :
        if self.enabled :
            self.movie_writer.finish()
