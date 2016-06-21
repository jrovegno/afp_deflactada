import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

karg_csv = dict(delimiter=';', decimal=',', index_col=0, parse_dates=True)

url = 'https://raw.githubusercontent.com/collabmarket/data_bcentral/master/data/uf.csv'
uf = pd.read_csv(url, **karg_csv)

afps = ['CUPRUM','HABITAT','PLANVITAL']

for afp_name in afps:
    
    filename = 'https://raw.githubusercontent.com/collabmarket/data_afp/master/data/VC-%s.csv'%afp_name
    afp = pd.read_csv(filename, **karg_csv)
    afp_uf = afp.div(uf.Valor,axis=0)
    
    for fondo in ['A','C','E']:
        for tipo,aux in zip(['nominal','real'],[afp, afp_uf]):
            
            # Grafico rentabilidad, rentabilidad acumulada y valor cuota promedio periodo
            # Periodos : W week, , M month, Q quarter, A year
            # Ultimo valor del periodo
            df = aux.loc['1981':,[fondo]].resample('M').last()
            # Suma rentabilidad mensual rentabilidad promedio anual
            aux = df.pct_change(1).resample('A').sum()
            # Grafo rentabilidad
            fig, ax = plt.subplots(figsize=(8,8))
            # Media movil 5 agnos
            aux.rolling(window=5,center=False).median().plot(ax=ax)
            # Rentabilidad anual
            aux.plot(title='Rentabilidad %s Promedio Anual %s fondo %s'%(tipo,afp_name,fondo), kind='bar', ax=ax)
            # Fix date format on bar plot with pandas
            # Make most of the ticklabels empty so the labels don't get too crowded
            ticklabels = ['']*len(aux.index)
            bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            width, height = bbox.width, bbox.height
            step = int(len(aux.index)/(width*1.3))
            # Every step ticklable shows the month, day and year
            ticklabels[::step] = [item.strftime('%Y') for item in aux.index[::step]]
            ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
            plt.gcf().autofmt_xdate()
            plt.legend(loc=3)
            plt.savefig('rent-%s-%s-%s.png'%(tipo,afp_name,fondo))

