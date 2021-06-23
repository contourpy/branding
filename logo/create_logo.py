from contourpy import contour_generator
from contourpy.util.mpl_util import filled_to_mpl_paths, lines_to_mpl_paths
import matplotlib.pyplot as plt
import matplotlib.collections as mcollections
import numpy as np
import os
from pathlib import Path


# Configuration.
input_filename = 'coefficients.txt'
border = 0.05
nmodes = 8
z_mean = -0.03429101451261287

ngrid = 40
xborder = [0.03, 0.05]
yborder = [0.06, 0.02]
font_path = Path('../fonts/Catamaran-Bold.ttf')
svg_linewidth = 0.5
png_linewidth = 1.0

# Colors are colorbrewer RdYlGn palette.
colors = ["#1a9641", "#a6d96a", "#ffffbf", "#fdae61", "#d7191c"]


def full_output_filename(filename):
    return os.path.join('output', filename)

def plot_logo(ax, linewidth):
    cont_gen = contour_generator(x2, y2, z)
    for i in range(len(colors)):
        filled = cont_gen.filled(levels[i], levels[i+1])
        paths = filled_to_mpl_paths(filled, cont_gen.fill_type)
        collection = mcollections.PathCollection(
            paths, facecolors=colors[i], edgecolors='none', lw=0)
        ax.add_collection(collection)

    for level in levels:
        lines = cont_gen.lines(level)
        paths = lines_to_mpl_paths(lines, cont_gen.line_type)
        collection = mcollections.PathCollection(
            paths, facecolors='none', edgecolors='k', lw=linewidth)
        ax.add_collection(collection)

    ax.set_xlim(xborder[0], 1.0-xborder[1])
    ax.set_ylim(yborder[0], 1.0-yborder[1])
    ax.axis('off')


# Load Fourier coefficients from file.
coefficients = np.loadtxt(input_filename)

# Create z-field on quad grid from Fourier components.
x = np.linspace(xborder[0], 1.0-xborder[1], ngrid)
y = np.linspace(yborder[0], 1.0-yborder[1], ngrid)
x2, y2 = np.meshgrid(x, y)
xflat = x2.ravel()
yflat = y2.ravel()
A = np.empty((ngrid*ngrid, nmodes*nmodes))
for i in range(nmodes):
    for j in range(nmodes):
        A[:, i+j*nmodes] = np.sin((i+1)*np.pi*xflat) * np.sin((j+1)*np.pi*yflat)

z = (A*coefficients).sum(axis=1) + z_mean
z.shape = (ngrid, ngrid)
levels = np.linspace(0.0, z.max(), 6)

# Logo only, SVG.
fig = plt.figure(figsize=(1, 1), dpi=100)
ax = fig.add_axes([0, 0, 1, 1], aspect='equal')
plot_logo(ax, svg_linewidth)
filename = full_output_filename('contourpy_logo.svg')
print(f'Writing file {filename}')
fig.savefig(filename, transparent=True)

# Logo only, PNG files.
fig = plt.figure(figsize=(1, 1), dpi=100)
ax = fig.add_axes([0, 0, 1, 1], aspect='equal')
plot_logo(ax, png_linewidth)
for pixels in (200, 300):
    size = pixels / 100.0
    fig.set_size_inches(size, size)
    filename = full_output_filename(f'contourpy_logo_{pixels}.png')
    print(f'Writing file {filename}')
    fig.savefig(filename, transparent=True)

# PNG file with white border to fit in github circle.
fig = plt.figure(figsize=(3, 3), dpi=100)  # So 300 pixels.
ax = fig.add_axes([0, 0, 1, 1], aspect='equal')
plot_logo(ax, png_linewidth)
border = 0.1
ax.set_xlim(xborder[0]-border, 1.0-xborder[1]+border)
ax.set_ylim(yborder[0]-border, 1.0-yborder[1]+border)
filename = full_output_filename(f'contourpy_logo_{pixels}_border.png')
print(f'Writing file {filename}')
fig.savefig(filename, transparent=True)

# Logo and name, horizontal.
fig = plt.figure(figsize=(2.55, 0.75))
ax = fig.add_axes([0, 0, 1, 1], aspect='equal')
plot_logo(ax, svg_linewidth)
ax.text(0.95, 0.5, 'ContourPy', font=font_path, fontsize=28, ha='left', va='center_baseline', c="#000000")
ax.set_xlim(0.0, 3.4)
filename = full_output_filename('contourpy_logo_horiz.svg')
print(f'Writing file {filename}')
fig.savefig(filename, transparent=True)

# Logo and name, vertical.
fig = plt.figure(figsize=(2.0, 1.1))
ax = fig.add_axes([0, 0, 1, 1], aspect='equal')
plot_logo(ax, svg_linewidth)
ax.text(0.5, 0.05, 'ContourPy', font=font_path, fontsize=28, ha='center', va='top', c="#000000")
ax.set_ylim(-0.5, 1.0)
filename = full_output_filename('contourpy_logo_vert.svg')
print(f'Writing file {filename}')
fig.savefig(filename, transparent=True)
