# Imports
import struct
import math
import numpy as np

# Create, and open a new binary file
file_name = 'stigmatic_gaussian_beam.dat'
file = open(file_name, 'wb')

# Variable header data
number_rays = 16                        # The number of rays in the file.
# A text description of the source
description = ("Stigmatic Gaussian beam using P. Colbourne's"
               " implementation (http://dx.doi.org/10.1117/12.2071105).")
                                        # (maximum 100 characters).
source_flux = 1                         # The total flux in watts of this
                                        # source.
ray_set_flux = 1                        # The flux in watts represented by
                                        # this Ray Set.
wavelength = 0.561                      # The wavelength in micrometers,
                                        # 0 if a composite.
inclination = (0, 0)                    # Angular range for ray set (Degrees).
azimuth = (0, 0)                        # Angular range for ray set (Degrees).
dimension_units = 4                     # METERS=0, IN=1, CM=2, FEET=3, MM=4
loc = (0, 0, 0)                         # Coordinate Translation of the source.
rot = (0, 0, 0)                         # Source rotation (Radians).
ray_format = 0                          # The ray_format_type must be either 0
                                        # for flux only format, or 2 for the
                                        # spectral color format.
flux_type = 0                           # If and only if the ray_format_type is
                                        # 0, then the flux_type is 0 for watts,
                                        # and 1 for lumens. For the spectral
                                        # color format, the flux must be in
                                        # watts, and the wavelength in
                                        # micrometers.

# Fixed header data
format_version = 1010                   # Format version ID, current value is
                                        # 1010.

# Unused header data
scale = (0, 0, 0)                       # Currently unused.

# Write header data
file.write(struct.pack('i', format_version))
file.write(struct.pack('i', number_rays))
if len(description) < 100:
    description.ljust(100, '\0')
else:
    description = description[0:99]
file.write(struct.pack('100s', description.encode('utf-8')))
file.write(struct.pack('f', source_flux))
file.write(struct.pack('f', ray_set_flux))
file.write(struct.pack('f', wavelength))
file.write(struct.pack('2f', inclination[0], inclination[1]))
file.write(struct.pack('2f', azimuth[0], azimuth[1]))
file.write(struct.pack('l', dimension_units))
file.write(struct.pack('3f', loc[0], loc[1], loc[2]))
file.write(struct.pack('3f', rot[0], rot[1], rot[2]))
file.write(struct.pack('3f', scale[0], scale[1], scale[2]))
file.write(struct.pack('4f', 0, 0, 0, 0)) # Unused bytes
file.write(struct.pack('2i', ray_format, flux_type))
file.write(struct.pack('2i', 0, 0)) # Reserved bytes

# Beam parameters
x_waist = 0.001
y_waist = 0.002
x_div = wavelength/1000/math.pi/x_waist
y_div = wavelength/1000/math.pi/y_waist
alpha_space = np.linspace(0, 2*math.pi, num=number_rays, endpoint=False)

# Fixed ray data
z = 0
flux = 1

for alpha in alpha_space: 
    x = x_waist*math.cos(alpha)
    y = y_waist*math.sin(alpha)
    l = -x_div*math.sin(alpha)
    m = y_div*math.cos(alpha)
    l = l / math.sqrt(1 + l**2 + m**2)
    m = m / math.sqrt(1 + l**2 + m**2)
    n = 1 / math.sqrt(1 + l**2 + m**2)

    # Write ray data
    file.write(struct.pack('7f', x, y, z, l, m, n, flux))

# Close the binary file
file.close()