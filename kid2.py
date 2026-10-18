"""
Same as before but generates THREE plots:
- 1-4
- 5-14
- 15-24

from:

https://wonder.cdc.gov/controller/saved/D76/D292F592
"""

import pandas as pd
import pylab as plt
from utils import make_accessible, read_cdc_txt

plt.style.use('ggplot')
plt.ion()

CAUSE = 'Injury Mechanism & All Other Leading Causes'
AGEGROUP = "Ten-Year Age Groups"

# 1999-2017 from the old (bridged-race) database, 2018-2024 from the new
# single-race database: https://wonder.cdc.gov/controller/saved/D158/D525F242
old = read_cdc_txt(
    "Underlying Cause of Death, 1999-2020-year-agegroup-injurymechanism.txt")
new = read_cdc_txt(
    "Underlying Cause of Death, 2018-2024-year-agegroup-injurymechanism.txt")
old = old[old["Year"].astype(int) < 2018]
bigdf = pd.concat([old, new], ignore_index=True)
bigdf["Crude Rate"] = pd.to_numeric(bigdf["Crude Rate"], errors="coerce")
bigdf = bigdf[bigdf[AGEGROUP].isin(["1-4 years", "5-14 years", "15-24 years"])]
ages = bigdf[AGEGROUP].unique()

for age in ages:
    df = bigdf[bigdf[AGEGROUP] == age]
    subdf = df.groupby("Year").apply(lambda g: g.nlargest(8, "Deaths"))
    CAUSE = 'Injury Mechanism & All Other Leading Causes'
    topcauses = subdf.loc[:, CAUSE].unique()[:7]
    pdf = df.pivot(index="Year", columns=CAUSE, values="Crude Rate")
    subpdf = pdf.loc[:, topcauses].astype(float)

    ax = subpdf.plot(figsize=(12, 8))
    plt.title(age)
    plt.ylabel('Deaths per 100,000')
    plt.title(f'Underlying cause of death, ages {age} (US CDC)')
    plt.tight_layout()
    make_accessible(ax)

    basefname = f'injury-mechanism-top-7-{age.replace(" ", "")}'
    plt.savefig(f'{basefname}.png', dpi=300)
    plt.savefig(f'{basefname}.svg')
