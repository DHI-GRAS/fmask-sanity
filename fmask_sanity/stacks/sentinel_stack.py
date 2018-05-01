import os
import glob

from .buildvrt import buildvrt


def create_sentinel_stack(granuledir, outfile):
    infiles = []
    for fnpattern in ['*_B0[1-8].jp2', '*_B8A.jp2', '*_B09.jp2', '*_B1[0-2].jp2']:
        pattern = os.path.join(granuledir, 'IMG_DATA', fnpattern)
        bandfiles = sorted(glob.glob(pattern))
        if not bandfiles:
            raise RuntimeError('No files found for pattern \'{}\'.'.format(pattern))
        infiles += bandfiles
    buildvrt(infiles, outfile, resolution='user', separate=True, extra=['-tr', '20', '20'])
