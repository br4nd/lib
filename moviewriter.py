import pdb

class moviewriter :

    enabled = True

    def __init__(self, fig, name, enabled=True, fps=10, dpi=100) :
        self.enabled = enabled
        if enabled :
            import matplotlib.animation as animation

            writer_list = animation.writers.list()

            if 'ffmpeg' in writer_list :
                writer = animation.writers['ffmpeg']
            elif 'libav' in writer_list :
                writer = animation.writers['libav']
            else :
                # something else may not work ....
                print 'check the writer'
                pdb.set_trace()

            self.movie_writer = writer(fps=fps)
            self.movie_writer.setup(fig, '.'.join((name,'mp4')), dpi=dpi)

    def update(self) :
        if self.enabled :
            self.movie_writer.grab_frame()

    def finish(self) :
        if self.enabled :
            self.movie_writer.finish()
