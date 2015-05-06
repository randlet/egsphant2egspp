# egsphant2egspp

A simple script for converting EGSnrc egsphant files to the binary density and text ramp files used by the egs++ EGS_XYZGeometry.

Usage:

    egsphant2esgpp.py input_egsphant_file.egsphant

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
