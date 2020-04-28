import psycopg2
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

conn = psycopg2.connect(user=" ",
                        password=" ",
                        host=" ",
                        port=" ",
                        database=" ")

mapdf = "SELECT kab_name,kota,geom FROM dki_kota"
        
map_df = gpd.GeoDataFrame.from_postgis(mapdf,conn, geom_col='geom') 
map_jakarta=map_df.rename(index=str, columns={'kab_name': 'area'})

# import dataset jumlah penggemar di jakarta
df=pd.read_csv("real_madrid_fans_jakarta.csv")
data_map=df.rename(index=str, columns={'POPULATION': 'FANS'})

# menggabungkan table map_jakarta dengan data_map
data_fans = map_jakarta.set_index('area').join(data_map.set_index('DISTRICT'))

# set variable yang akan divisualisasi
variable = 'FANS'
# set range minimum dan maksimum untuk choropleth
vmin, vmax = data_fans['FANS'].min(), data_fans['FANS'].max()
# visualisasi
fig, ax = plt.subplots(1, figsize=(10, 6))
data_fans.plot(column=variable, cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

ax.axis('off')
# Menambahkan title
ax.set_title('Real Madrid Fans', fontdict={'fontsize': '25', 'fontweight' : '3'})
# Membuat colorbar yang menunjukkan jumlah fans
sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm)