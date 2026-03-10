#!/usr/bin/python3

import os
import numpy as np

file_wav = os.getenv('file_wav')
file_wav_prm = os.getenv('file_wav_prm')
file_image = os.getenv('file_image')
nx = int(os.getenv('nx'))
ny = int(os.getenv('ny'))
electron_energy = float(os.getenv('electron_energy'))
file_cel = os.getenv('file_cel')

with open(file_cel, 'r') as cel_file:
    lines = cel_file.readlines()
    line = lines[1].split()
    a = float(line[1])
    b = float(line[2])

aberrations = [[0.0, 0.0],    # image shift
               [-4.0, -8.0],  # defocus
               [0.0, 0.0],    # astigmatism
               [0.0, 0.0],    # coma
               [0.0, 0.0],    # three-lobe aberration
               [0.0, 0.0],    # spherical aberration
               [0.0, 0.0]]    # star aberration
aberrations = np.array(aberrations)

with open(file_wav_prm, "w") as f:
    print(f"'{file_wav}'", file=f)      # line 1
    print(f"{nx} {ny}", file=f)
    print(f"{a/nx} {b/ny}", file=f)
    print(f"{electron_energy}", file=f)
    print(f"{0}", file=f)               # line 5
    print(f"'{file_image}'", file=f)
    print(f"{nx} {ny}", file=f)
    print(f"{0} {1.0} {1.0} {0.0}", file=f)
    print(f"{0}", file=f)
    print(f"{0.0}", file=f)            # line 10
    print(f"{0.0} {0.0}", file=f)
    print(f"{0.0}", file=f)
    print(f"{1}", file=f)
    print(f"{1} {3.8}", file=f)
    print(f"{1} {0.4}", file=f)        # line 15
    print(f"{0} {1.0} '{'mtf.dat'}'", file=f)
    print(f"{0} {1.0} {1.0} {0.0}", file=f)
    print(f"{len(aberrations)}", file=f)
    for i, abr in enumerate(aberrations):
        value = np.random.uniform(aberrations[i, 0], aberrations[i, 1])
        valx = value * np.cos(np.random.uniform(0, 2*np.pi))
        valy = value * np.sin(np.random.uniform(0, 2*np.pi))
        print(f"{i} {valx} {valy}", file=f) 
    print(f"{250.0} {0.03}", file=f)   # line 19+Nabr
    print(f"{0.0} {0.0}", file=f)
    print(f"{0}", file=f)
