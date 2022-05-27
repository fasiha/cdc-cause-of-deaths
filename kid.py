"""
Recreating the Economist's plot:

https://nitter.it/TheEconomist/status/1529545402818695169#m

Using US CDC data:

https://wonder.cdc.gov/controller/saved/D76/D292F582
"""

import pandas as pd
from io import StringIO
import pylab as plt

plt.style.use('ggplot')
plt.ion()

with open("Underlying Cause of Death, 1999-2020.txt", 'r') as fid:
    alllines = fid.readlines()
    lines = alllines[:1] + list(filter(lambda s: s.startswith("\t"), alllines))
    io = StringIO("\n".join(lines))
    df = pd.read_csv(io, delimiter='\t')

subdf = df.groupby("Year").apply(lambda g: g.nlargest(8, "Deaths"))
subdf.to_csv("foo.csv")

CAUSE = 'Injury Mechanism & All Other Leading Causes'
subdf.plot.bar(x=CAUSE, y='Deaths')

topcauses = subdf.loc[:, CAUSE].unique()[:7]

# subdf2 = df.groupby(["Year", CAUSE],as_index=False).apply(lambda g: g.nlargest(5, "Deaths"))
pdf = df.pivot(index="Year", columns=CAUSE, values="Crude Rate")
pdf.loc[:, topcauses]

subpdf = pdf.loc[:, topcauses].astype(float)

ax = subpdf.plot(figsize=(12, 8))
plt.ylabel('Deaths per 100,000')
plt.title('Underlying cause of death, ages 1-24 (US CDC)')
plt.tight_layout()
lw = [3, 2, 1]
markers = ['.', 'o', 'x', '+']
ls = ['-', '--']
for i, l in enumerate(ax.lines):
    l.set_marker(markers[i % len(markers)])
    l.set_ls(ls[i % len(ls)])
    l.set_lw(lw[i % len(lw)])
plt.legend()

plt.savefig('injury-mechanism-top-7-1-24.png', dpi=300)
plt.savefig('injury-mechanism-top-7-1-24.svg')
