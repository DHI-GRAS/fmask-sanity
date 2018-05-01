import os
import glob


def find_xml_in_granule_dir(granuledir):
    pattern = os.path.join(granuledir, '*.xml')
    xmlfiles = glob.glob(pattern)
    if len(xmlfiles) != 1:
        raise RuntimeError('Expecting exactly one XML file in granules dir. Found {} with pattern \'{}\'.',format(len(xmlfiles), pattern))
    return xmlfiles[0]
