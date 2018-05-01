# fmask-sanity
Python interface to the Python-FMask scripts

## The problem

`python-fmask` only has command-line interfaces to the scripts
that are needed to create and configure the inputs to run FMask.

## The solution

Extract the relevant parts of the `python-fmask` [command-line scripts](https://bitbucket.org/chchrsc/python-fmask/src/95f3bc60d732862ad42c96e09a7dd305f7ca89ee/bin?at=pythonfmask-0.4.5) and replace the `argparse` interface by a Python function.
