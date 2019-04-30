#!/bin/env/python

# Import modules
import carla

try:
    import pygame
except ImportError:
    raise RuntimeError(
        'Cannot import pygame. Please make sure the pygame package is installed.'
    )

import argparse

# Modules
def event_4(seed):
    print('Using seed', seed)


# Define the main module
def main():
    event_4(4000)


# Main execution
if __name__ == '__main__':
    main()