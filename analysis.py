import pandas as pd
import matplotlib.pyplot as plt

URL = "https://ourworldindata.org/grapher/avocado-production.csv?v=1&csvType=full&useColumnShortNames=false"

def calc_share(countries, year, country):
    r = range(1961, year + 1)
    mexico_dict = {}
    
    for i in r:
        if i not in countries['Year']:
            continue
        year_table = countries[countries['Year'] == i]
        world_total = year_table['production'].sum()
        country_table = year_table[year_table['Entity'] == country]
        country_production = country_table['production'].iloc[0]
        share = country_production / world_total * 100
        mexico_dict[i] = share

    return mexico_dict

if __name__ == "__main__":
    df = pd.read_csv(URL, storage_options={"User-Agent": "data fetch/1.0"})
    df = df.rename(columns={"Avocados - Production (tonnes)": "production"})
    countries = df[df['Code'].str.len() == 3]

    mexico_share = calc_share(countries, 2024, "Mexico")
    series = pd.Series(mexico_share)
    series.plot(marker="o", title="Mexico's Share of Global Avocado Production (1961-2024)")
    plt.ylabel("Share (%)")
    plt.savefig("figures/mexico_share.png")

    year_countries = countries[countries['Year'] == 2024]
    top10 = year_countries.nlargest(10, "production")
    top10 = top10.set_index("Entity")
    top10["production"].plot(kind="bar", title="Top 10 Producing Countries")
    plt.ylabel("Production (tonnes)")
    plt.xlabel("Countries")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("figures/top10_2024.png")



