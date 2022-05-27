"""
Recreating the Economist's plot:

https://nitter.it/TheEconomist/status/1529545402818695169#m

Using US CDC data:

https://wonder.cdc.gov/controller/saved/D76/D292F582
"""

import pandas as pd
import pylab as plt
from utils import make_accessible, read_cdc_txt

plt.style.use('ggplot')
plt.ion()

df = read_cdc_txt("Underlying Cause of Death, 1999-2020.txt")
subdf = df.groupby("Year").apply(lambda g: g.nlargest(8, "Deaths"))
CAUSE = 'Injury Mechanism & All Other Leading Causes'
topcauses = subdf.loc[:, CAUSE].unique()[:7]

pdf = df.pivot(index="Year", columns=CAUSE, values="Crude Rate")
subpdf = pdf.loc[:, topcauses].astype(float)

ax = subpdf.plot(figsize=(12, 8))
plt.ylabel('Deaths per 100,000')
plt.title('Underlying cause of death, ages 1-24 (US CDC)')
plt.tight_layout()
make_accessible(ax)

plt.savefig('injury-mechanism-top-7-1-24.png', dpi=300)
plt.savefig('injury-mechanism-top-7-1-24.svg')
