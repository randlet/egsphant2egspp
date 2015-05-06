#!/usr/bin/env python
"""
This is a simple script for converting EGSnrc egsphant files
to the binary density and text ramp files used by the egs++
XYZGeometry.

Usage: egsphant2esgpp.py input_egsphant_file.egsphant

This will produce two files:

    input_egsphant_file.density
    input_egsphant_file.ramp

which can then be used to create an XYZGeometry like so:


    :start geometry:

        name = phantom
        library = egs_ndgeometry
        type    = EGS_XYZGeometry

        density matrix = input_egsphant_file.density
        ct ramp = input_egsphant_file.ramp

    :stop geometry:

You can also use a custom ramp file if desired.

"""

import array
import os
import sys

from struct import pack

IS_LITTLE_ENDIAN = sys.byteorder == "little"
MED_IDXS = list("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def write_density(data, path):

    path = path + ".density"
    f = open(path, "wb")

    f.write(pack('?', IS_LITTLE_ENDIAN))

    f.write(pack('iii', *data['dims']))

    xbounds, ybounds, zbounds = data['bounds']
    f.write(pack('f'*len(xbounds), *xbounds))
    f.write(pack('f'*len(ybounds), *ybounds))
    f.write(pack('f'*len(zbounds), *zbounds))

    rhos = data['reg_rhos']
    f.write(pack('f'*len(rhos), *rhos))

    f.close()

    return path

def write_ramp(data, path):

    path = path + ".ramp"
    f = open(path, "w")

    media = data['media']

    reg_meds = data['reg_meds']
    reg_rhos = data['reg_rhos']
    med_map =  data['med_map']

    med_rhos = {}
    for m in media:
        med_rhos[m] = []

    for m, r in zip(reg_meds, reg_rhos):
        med = med_map[m]
        med_rhos[med].append(r)

    for k, v in med_rhos.items():
        if v:
            min_ = min(v)
            max_ = max(v)

            # egspp doesn't handle min rho == max rho so
            # add a negligble offset from actual densities
            if abs(min_-max_) < 1E-8:
                min_ *= (1 - 1E-7)
                max_ *= (1 + 1E-7)

            def_ = (min_+max_)/2.
            f.write("%s\t%.7E\t%.7E\t%.7E\n"%(k, min_, max_, def_))

    f.close()

    return path



def parse_egsphant(path):

    f = open(path,"r")

    nmed = int(f.readline().strip())

    med_map = {}
    meds = []
    for i in range(nmed):
        meds.append(f.readline().strip())
        med_map[MED_IDXS[i]] = meds[-1]


    data = [x.strip() for x in f.read().strip().split() if x.strip()]

    f.close()

    estep_slice = slice(nmed)
    estepes = map(float, data[estep_slice])
    del data[estep_slice]

    dim_slice = slice(3)
    nx, ny, nz = map(int, data[dim_slice])
    del data[dim_slice]

    nvox =  nx*ny*nz

    xs_slice = slice(nx+1)
    xbounds = map(float, data[xs_slice])
    del data[xs_slice]

    ys_slice = slice(ny+1)
    ybounds = map(float, data[ys_slice])
    del data[ys_slice]

    zs_slice = slice(nz+1)
    zbounds = map(float, data[zs_slice])
    del data[zs_slice]


    reg_meds = []
    for kk in range(nz):
        for jj in range(ny):
            reg_meds.extend(list(data.pop(0)))


    reg_rhos = map(float, data)
    del data

    try:
        assert len(reg_meds) == len(reg_rhos)
        assert len(reg_meds) == nvox
    except:
        print "failed to read media and rho properly"



    return {
        'dims': (nx, ny, nz),
        'bounds': (xbounds, ybounds, zbounds),
        'estepes': estepes,
        'media': meds,
        'med_map': med_map,
        'reg_meds': reg_meds,
        'reg_rhos': reg_rhos
    }






if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: %s file_to_convert.egsphant" % __file__
        exit()

    path = os.path.normpath(sys.argv[1])

    if not os.path.exists(path):
        print "Unable to find '%s' egsphant file" % path
        exit()


    try:
        data = parse_egsphant(path)
    except Exception, e:
        print "Invalid egsphant file. Error:\n\t%s\n" % e
        exit()

    idx =  path.find(".egsphant")

    outpath = path
    if idx >= 0 :
        outpath = outpath[:idx]

    try:
        density_name = write_density(data, outpath)
    except Exception, e:
        print "Failed to write density data. Error:\n\t%s\n" % e
        exit()

    try:
        ramp_name = write_ramp(data, outpath)
    except Exception, e:
        print "Failed to write ramp data. Error:\n\t%s\n" % e
        exit()



    print "Wrote density to : %s" % density_name
    print "Wrote ramp to    : %s" % ramp_name



