"""
https://wonder.cdc.gov/controller/saved/D76/D292F612
"""
import pandas as pd
import pylab as plt
from utils import make_accessible, read_cdc_txt

plt.style.use('ggplot')
plt.ion()

INTENT = 'Injury Intent'
df = read_cdc_txt("Underlying Cause of Death, 1999-2020-guns.txt")
pdf = df.pivot(index="Year", columns=INTENT, values="Crude Rate")
pdf['Total'] = pdf.sum(axis=1)
subpdf = pdf.loc[:, pdf.columns[[-1, 0, 2, 4, 1, 3]]].astype(float)

ax = subpdf.plot(figsize=(12, 8))
plt.ylabel('Deaths per 100,000')
plt.title('Death injury intent: firearms, ages 1-24 (US CDC)')
plt.tight_layout()
make_accessible(ax)

plt.savefig('injury-intent-guns.png', dpi=300)
plt.savefig('injury-intent-guns.svg')
