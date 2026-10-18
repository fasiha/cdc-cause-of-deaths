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

CAUSE = 'Injury Mechanism & All Other Leading Causes'
AGEGROUP = "Ten-Year Age Groups"

old = read_cdc_txt("Underlying Cause of Death, 1999-2020.txt")
old = old[old["Year"].astype(int) < 2018]


def combine_ages(fname):
    """The 2018-2024 export is split by age group: sum deaths and population
    over 1-4, 5-14, 15-24 to get the 1-24 crude rate"""
    d = read_cdc_txt(fname)
    d = d[d[AGEGROUP].isin(["1-4 years", "5-14 years", "15-24 years"])].copy()
    d["Population"] = pd.to_numeric(d["Population"])
    d["Deaths"] = pd.to_numeric(d["Deaths"])
    pop = d.drop_duplicates(["Year", AGEGROUP]).groupby("Year")["Population"].sum()
    g = d.groupby(["Year", CAUSE])["Deaths"].sum().reset_index()
    g["Population"] = g["Year"].map(pop)
    g["Crude Rate"] = (g["Deaths"] / g["Population"] * 1e5).round(1)
    return g


new = combine_ages("Underlying Cause of Death, 2018-2024-year-agegroup-injurymechanism.txt")
df = pd.concat([old, new], ignore_index=True)
df["Year"] = df["Year"].astype(int)
df["Crude Rate"] = pd.to_numeric(df["Crude Rate"], errors="coerce")
subdf = df.groupby("Year").apply(lambda g: g.nlargest(8, "Deaths"))
topcauses = subdf.loc[:, CAUSE].unique()[:7]

pdf = df.pivot(index="Year", columns=CAUSE, values="Crude Rate")
subpdf = pdf.loc[:, topcauses].astype(float)

ax = subpdf.plot(figsize=(12, 8))
plt.ylabel('Deaths per 100,000')
plt.ylim(bottom=0)
plt.title('Underlying cause of death, ages 1-24 (US CDC)')
plt.tight_layout()
make_accessible(ax)

plt.savefig('injury-mechanism-top-7-1-24.png', dpi=300)
plt.savefig('injury-mechanism-top-7-1-24.svg')
