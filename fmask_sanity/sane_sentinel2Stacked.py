import os
import tempfile
import logging
from argparse import Namespace

import numpy as np

from sane_fmask.stacks import sentinel_stack
from sane_fmask.interfaces import fmask_sentinel2Stacked
from sane_fmask.interfaces import fmask_sentinel2makeAnglesImage
from sane_fmask.metadata import sentinel2 as s2meta
from sane_fmask.sensible_defaults import FMASK_PARAMS

logger = logging.getLogger(__name__)


def run_fmask(granuledir, output, verbose=False, **kwargs):

    kwargs = dict(FMASK_PARAMS, **kwargs)

    with tempfile.TemporaryDirectory() as tempdir:
        logger.info('Creating band stacks ...')
        tempvrt = os.path.join(tempdir, 'temp.vrt')
        sentinel_stack.create_sentinel_stack(granuledir, outfile=tempvrt)
        logger.info('Done.')

        logger.info('Creating angles file ...')
        anglesfile = os.path.join(tempdir, 'angles.img')
        cmdargs_angles = Namespace(
                infile=s2meta.find_xml_in_granule_dir(granuledir),
                outfile=anglesfile)
        with np.errstate(invalid='ignore'):
            fmask_sentinel2makeAnglesImage.mainRoutine(cmdargs_angles)
        logger.info('Done.')

        cmdargs = Namespace(
            toa=tempvrt,
            anglesfile=anglesfile,
            output=output,
            verbose=verbose,
            tempdir=tempdir,
            keepintermediates=False,
            **kwargs)

        logger.info('Running FMask ...')
        fmask_sentinel2Stacked.mainRoutine(cmdargs)
        logger.info('Done.')
