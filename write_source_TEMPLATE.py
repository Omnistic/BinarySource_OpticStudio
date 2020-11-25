# Imports
import struct

# Create, and open a new binary file
file_name = 'binary_source.dat'
file = open(file_name, 'wb')

# Variable header data
number_rays = 1                         # The number of rays in the file.
description = 'A binary test source'    # A text description of the source
                                        # (maximum 100 characters).
source_flux = 1                         # The total flux in watts of this
                                        # source.
ray_set_flux = 1                        # The flux in watts represented by
                                        # this Ray Set.
wavelength = 0.561                      # The wavelength in micrometers,
                                        # 0 if a composite.
inclination = (0, 0)                    # Angular range for ray set (Degrees).
azimuth = (0, 0)                        # Angular range for ray set (Degrees).
dimension_units = 0                     # METERS=0, IN=1, CM=2, FEET=3, MM=4
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

# Ray data
x = 0
y = 0
z = 0
l = 0
m = 0
n = 1
flux = 1

# Ray spectral data
# ray_wavelength = 0.561

# Write ray data
file.write(struct.pack('7f', x, y, z, l, m, n, flux))

# Write spectral data
# file.write(struct.pack('8f', x, y, z, l, m, n, flux, wavelength))

# Close the binary file
file.close()