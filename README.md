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

An example egsphant file is included for testing (the .density & .ramp
resulting from its conversion are also included).  There is also a
sample egs++ geometry file included that uses the .density and .ramp files
to create a phantom geometry.  The geometry can be viewed with egs_view.
