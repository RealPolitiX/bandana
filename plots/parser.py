#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@authors: R. Patrick Xian, Christopher Sutton
"""

import numpy as np


def parse_geometry(path):
    """ Parse the input geometry file.
    """

    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    vectors =[]
    frac_coords = []
    cartesian_coords = []
    types = []

    for i, line in enumerate(lines):

        if "lattice_vector" in line:
            ls = line.split()
            vectors.append([float(ls[1]), float(ls[2]), float(ls[3])])

        if "atom_frac" in line:
            ls = line.split()
            frac_coords.append([float(ls[1]), float(ls[2]), float(ls[3])])
            types.append(str(ls[4]))
            Cartesian=False

        elif 'atom ' in line:
            ls = line.split()
            cartesian_coords.append([float(ls[1]), float(ls[2]), float(ls[3])])
            types.append(str(ls[4]))
            Cartesian=True
        else:
            continue

    if Cartesian == True:
        return vectors, cartesian_coords, types, Cartesian
    else:
        return vectors, frac_coords, types, Cartesian


def parse_homo_lumo(path):
    """ Parse the indices of the HOMO and LUMO.
    """

    for line in open(path):
        # Start from k-position
        if "      0.00000       " in line:
            words = line.split()
            n_energy=int(words[0])
            break

    n_HOMO = 4 + 2*(n_energy-1)-1
    n_LUMO = 4 + 2*n_energy-1

    return n_HOMO, n_LUMO


def parse_bands(files, band_id, nend=None):
    """ Parse the energy bands from the `bandxxxx.out` files.

    :Parameters:
        files : list
            List of band energy files.
        band_id : int
            Band index.
        nend : int | None
            Ending index of the energy band values.
    """

    band = []
    n_bands = len(files)

    for i_band, filename in enumerate(files):
        data = np.loadtxt(filename)
        y = data[0:nend, band_id]
        y = y / 27.2113845  # change energy from eV to a.u.
        band.append(y)

    band = np.asarray(band)

    return band


def sympad(matrix, pads=None, prerow=0, postrow=0, precol=0, postcol=0,
            mode='reflect', reftype='even'):
    """ Symmetrically padding the 2D matrix.

    :Parameters:
        matrix : 2D array
            2D matrix before padding.
        pads : tuple/list | None
            Padding shapes.
        prerow, postrow, precol, postcol : int, int, int, int | 0, 0, 0, 0
            Padding indices along the row and column dimensions.
        mode : str | 'reflect'
            Padding mode.
        reftype : str | 'even'
            Reflection type.
    """

    if pads is None:
        matpad = np.pad(matrix, ((prerow, postrow), (precol, postcol)),
                        mode=mode, reflect_type=reftype)
    else:
        matpad = np.pad(matrix, pads, mode=mode, reflect_type=reftype)

    return matpad
