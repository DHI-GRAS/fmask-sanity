from setuptools import setup, find_packages
import versioneer

setup(
    name='fmask_sanity',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Somewhat sane interface to Python-FMask',
    author='Jonas Sølvsteen',
    author_email='josl@dhigroup.com',
    packages=find_packages(),
    )
