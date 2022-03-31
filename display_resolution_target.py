#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import os
import numpy as np
from PIL import Image

def rotate(arr, angle):
    """ Rotate the pattern

    Args:
        arr (numpy.ndarray): Pattern to rotate.
        angle (int): Rotate angle. Only [0, 90, 180, 270] allowed.

    Returns:
        _ (numpy.ndarray): Rotated pattern. 
    """
    def _0(a):
        return a
    def _90(a):
        return a.T
    def _180(a):
        return np.flip(a)
    def _270(a):
        return np.flip(a.T)
    assert angle in [0, 90, 180, 270]
    switch = {0:_0, 90:_90, 180:_180, 270:_270}
    return switch[angle](arr)

def En(linewidth=1, angle=0):
    """ Generate character 'E'

    Notes:
        default pattern = [
                                1 1 1 1 1
                                1 0 0 0 0
                                1 1 1 1 1
                                1 0 0 0 0
                                1 1 1 1 1
                            ]

    Args:
        linewidth (int): Linewidth.
        angle (int): Rotate angle. Only [0, 90, 180, 270] allowed.

    Returns:
        E (numpy.ndarray): Rotated 'E' pattern. 
    """
    l = linewidth
    assert isinstance(l,int)
    assert angle in [0, 90, 180, 270]
    E = np.zeros((l*5,l*5), dtype='uint8')
    E[0:l, :] = 255
    E[2*l:3*l, :] = 255
    E[4*l:5*l, :] = 255
    E[:, 0:l] = 255
    if not angle == 0:
        E = rotate(E, angle)
    return E

def assign(arr, vertical, horizontal, linewidth, angle=0):
    """ Assign 'E' to a desired location

    Args:
        arr (numpy.ndarray): Background array.
        vertical (int): Vertical pixel number of the pattern's upper-left corner on background array.
        horizontal (int): Horizontal pixel number of the pattern's upper-left corner on background array.
        linewidth (int): Linewidth of the pattern.
        angle (int): Rotate angle. Only [0, 90, 180, 270] allowed.

    Returns:
        arr (numpy.ndarray): Background array with pattern on it. 
    """
    v, h, l, a = vertical, horizontal, linewidth, angle
    assert isinstance(arr,np.ndarray)
    assert isinstance(v,int)
    assert isinstance(h,int)
    assert isinstance(l,int)
    assert isinstance(a,int)
    arr[v:v+5*l, h:h+5*l] = En(l,a)
    return arr

def GroupAssign(canvas, params):
    """ Assign multiple 'E'

    Args:
        canvas (numpy.ndarray): Background array.
        params (list): List of parameters. Format: [[vertical, horizontal, linewidth, angle], ...]

    Returns:
        canvas (numpy.ndarray): Background array with multiple patterns on it. 
    """
    for param in params:
        if len(param) == 3:
            d = 0
            a, b, c = param
        else:
            a, b, c, d = param
        canvas = assign(canvas, a, b, c, d)
    return canvas

if __name__ == '__main__':
    resolution = np.array([1024, 1280])

    canvas = np.zeros(resolution, dtype='uint8')

    params = [
        # [vertical, horizontal, linewidth, angle]
        [825, 825, 10],
        [900, 800, 5, 0],
        [900, 850, 5, 90],
        [800, 900, 5, 180],
        [850, 900, 5, 270],
        [900, 900, 3],
        [925, 900, 2],
        [900, 925, 2, 90],
        [925, 925, 1]
        ]
    canvas = GroupAssign(canvas, params)

    img = Image.fromarray(canvas.astype('uint8'))

    img.save('./External Display/target.tif')
