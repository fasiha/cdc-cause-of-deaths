import pandas as pd
from io import StringIO
from itertools import product
from pylab import plt


def make_accessible(ax):
    lws = [3, 1]
    markers = ['o', 'x', 'v', 'd']
    for l, (marker, lw) in zip(ax.lines, product(markers, lws)):
        l.set_marker(marker)
        l.set_lw(lw)
    plt.legend()


def read_cdc_txt(fname):
    with open(fname, 'r') as fid:
        alllines = fid.readlines()
    lines = alllines[:1] + list(filter(lambda s: s.startswith("\t"), alllines))
    io = StringIO("\n".join(lines))
    return pd.read_csv(io, delimiter='\t')
