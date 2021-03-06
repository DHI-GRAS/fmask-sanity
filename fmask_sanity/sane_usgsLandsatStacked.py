import os
import tempfile
import logging
from argparse import Namespace

import numpy as np

from fmask_sanity.stacks import landsat_stack
from fmask_sanity.interfaces import fmask_usgsLandsatStacked
from fmask_sanity.interfaces import fmask_usgsLandsatMakeAnglesImage
from fmask_sanity.interfaces import fmask_usgsLandsatSaturationMask
from fmask_sanity.interfaces import fmask_usgsLandsatTOA
from fmask_sanity.interfaces import landsat as lmeta
from fmask_sanity.sensible_defaults import FMASK_PARAMS

logger = logging.getLogger(__name__)

LANDSATKEYS = ['4&5', '7', '8']


def run_fmask(productdir, output, landsatkey='8', **kwargs):

    kwargs = dict(FMASK_PARAMS, **kwargs)

    if landsatkey not in LANDSATKEYS:
        raise ValueError(f'landsatkey must be in {LANDSATKEYS}. Got {landsatkey}')

    with tempfile.TemporaryDirectory() as tempdir:

        mtl = lmeta.find_mtl_in_product_dir(productdir)

        # create band stacks
        logger.info('Creating band stacks ...')
        outfile_template = os.path.join(tempdir, 'temp_{imagename}.vrt')
        vrtfiles = landsat_stack.create_landsat_stacks(
            productdir, outfile_template=outfile_template, landsatkey=landsatkey)
        logger.info('Done.')

        # create angles file
        anglesfile = os.path.join(tempdir, 'angles.img')
        if not os.path.isfile(anglesfile):
            logger.info('Creating angles file ...')
            with np.errstate(invalid='ignore'):
                fmask_usgsLandsatMakeAnglesImage.mainRoutine(
                    Namespace(
                        mtl=mtl,
                        templateimg=vrtfiles['ref'],
                        outfile=anglesfile))
            logger.info('Done.')

        # create saturation file
        saturationfile = os.path.join(tempdir, 'saturation.img')
        if not os.path.isfile(saturationfile):
            logger.info('Creating saturation mask file ...')
            fmask_usgsLandsatSaturationMask.mainRoutine(
                Namespace(
                    infile=vrtfiles['ref'],
                    mtl=mtl,
                    output=saturationfile))
            logger.info('Done.')

        # create TOA file
        toafile = os.path.join(tempdir, 'toa.img')
        if not os.path.isfile(toafile):
            logger.info('Creating TOA file ...')
            fmask_usgsLandsatTOA.mainRoutine(
                Namespace(
                    infile=vrtfiles['ref'],
                    mtl=mtl,
                    anglesfile=anglesfile,
                    output=toafile))
            logger.info('Done.')

        cmdargs = Namespace(
            toa=toafile,
            thermal=vrtfiles['thermal'],
            anglesfile=anglesfile,
            saturation=saturationfile,
            mtl=mtl,
            verbose=True,
            tempdir=tempdir,
            output=output,
            **kwargs)

        logger.info('Running FMask (this may take a while) ...')
        fmask_usgsLandsatStacked.mainRoutine(cmdargs)
        logger.info('Done.')
