#!/usr/bin/env python
"""
This script can be used to read the .density file and print out
the information from the file allowing you to make sure the
binary density matrix file was created correctly.

Usage:
    check_conversion.py file_name.density

"""

import struct
import sys

N_BYTE_BYTES = 1
N_INT_BYTES = 4
N_FLOAT_BYTES = 4

if len(sys.argv) < 2:
    print __doc__
    sys.exit()

f = open(sys.argv[1], 'rb')

endian = struct.unpack('b',f.read(N_BYTE_BYTES))[0]
print "Endian      : %s" % ('little' if endian else 'big')

nx = struct.unpack('i',f.read(N_INT_BYTES))[0]
ny = struct.unpack('i',f.read(N_INT_BYTES))[0]
nz = struct.unpack('i',f.read(N_INT_BYTES))[0]
print "Nx, Ny, Nz  : %d, %d, %d" %(nx, ny, nz)

xbounds = struct.unpack('f'*(nx+1), f.read(N_FLOAT_BYTES*(nx+1)))
ybounds = struct.unpack('f'*(ny+1), f.read(N_FLOAT_BYTES*(ny+1)))
zbounds = struct.unpack('f'*(nz+1), f.read(N_FLOAT_BYTES*(nz+1)))
print "Xbounds     : %s" % (["%.2f" % x for x in xbounds],)
print "Ybounds     : %s" % (["%.2f" % x for x in ybounds],)
print "Zbounds     : %s" % (["%.2f" % x for x in zbounds],)

rhos = struct.unpack('f'*(nx*ny*nz), f.read(N_FLOAT_BYTES*(nx*ny*nz)))
print "# rhos read : %d" % len(rhos)
print "Max rho     : %.3f" % max(rhos)
print "Min rho     : %.3f" % min(rhos)

f.close()
