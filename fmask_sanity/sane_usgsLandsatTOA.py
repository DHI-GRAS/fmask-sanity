import os
import tempfile
import logging
from argparse import Namespace

import numpy as np

from fmask_sanity.stacks import landsat_stack
from fmask_sanity.interfaces import fmask_usgsLandsatTOA
from fmask_sanity.interfaces import fmask_usgsLandsatMakeAnglesImage
from fmask_sanity.metadata import landsat as lmeta

logger = logging.getLogger(__name__)

LANDSATKEYS = ['4&5', '7', '8']


def run_fmask(productdir, outfile, landsatkey='8'):

    if landsatkey not in LANDSATKEYS:
        raise ValueError(f'landsatkey must be in {LANDSATKEYS}. Got {landsatkey}')

    with tempfile.TemporaryDirectory() as tempdir:
        mtl = lmeta.find_mtl_in_product_dir(productdir)

        # create band stack
        logger.info('Creating band stack ...')
        refimg = os.path.join(tempdir, 'ref.vrt')
        landsat_stack.create_landsat_stack(
            productdir, outfile=refimg, imagename='ref', landsatkey=landsatkey)
        logger.info('Done.')

        # create angles file
        anglesfile = os.path.join(tempdir, 'angles.img')
        if not os.path.isfile(anglesfile):
            logger.info('Creating angles file ...')
            with np.errstate(invalid='ignore'):
                fmask_usgsLandsatMakeAnglesImage.mainRoutine(
                        Namespace(
                            mtl=mtl,
                            templateimg=refimg,
                            outfile=anglesfile))
            logger.info('Done.')

        logger.info('Creating TOA image ...')
        cmdargs = Namespace(
                infile=refimg,
                mtl=mtl,
                anglesfile=anglesfile,
                output=outfile)
        with np.errstate(invalid='ignore'):
            fmask_usgsLandsatTOA.mainRoutine(cmdargs)
        logger.info('Done.')
