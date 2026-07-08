import os
import numpy as np
from astropy.io import fits
from PIL import Image

current = "M 51"
folder = "C:/Users/brinl/Desktop/astro/data"

output_folder = "C:/Users/brinl/Desktop/astro/koncne_fotke_test"
output_filename = f"{current}_koncna_fotografija.png"

os.makedirs(output_folder, exist_ok=True)

r_min, r_max = 198, 709
r_gamma = 2.41

g_min, g_max = 66, 502
g_gamma = 0.92

b_min, b_max = 32, 492
b_gamma = 0.74

print("Branje FITS datotek")
R = fits.getdata(os.path.join(folder, "FINAL", current, "R.fits"))
G = fits.getdata(os.path.join(folder, "FINAL", current, "V.fits"))
B = fits.getdata(os.path.join(folder, "FINAL", current, "B.fits"))

def power_scale(x, vmin, vmax, a):
    out = np.zeros(x.shape)
    out[x > vmax] = 255
    mask = (x > vmin) & (x < vmax)
    out[mask] = 255 * ((x[mask] - vmin) / (vmax - vmin))**a
    return np.array(out, dtype=int)

print("Ustvarjanje končne slike")
R_scaled = power_scale(R, r_min, r_max, r_gamma)
G_scaled = power_scale(G, g_min, g_max, g_gamma)
B_scaled = power_scale(B, b_min, b_max, b_gamma)

rgb_data = np.dstack([R_scaled, G_scaled, B_scaled]).astype(np.uint8)
koncna_slika = Image.fromarray(rgb_data)


koncna_slika.save(os.path.join(output_folder, output_filename))