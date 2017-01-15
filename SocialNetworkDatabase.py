# coding=utf-8
import glob


class SNDB(object):
    """docstring for SNDB."""

    def __init__(self, debug=False):
        super(SNDB, self).__init__()
        self.debug = debug
        if not os.path.exists('DB'):
            os.path.mkdir('DB')

if __name__ == '__main__':
    SNDB(True)
