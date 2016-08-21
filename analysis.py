import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

karg_csv = dict(delimiter=';', decimal=',', index_col=0, parse_dates=True)

url = 'https://raw.githubusercontent.com/collabmarket/data_bcentral/master/data/uf.csv'
uf = pd.read_csv(url, **karg_csv)

afps = ['CUPRUM', 'HABITAT', 'PLANVITAL', 'PROVIDA']
fondos = ['A', 'C', 'E']

for afp_name in afps:
    
    filename = 'https://raw.githubusercontent.com/collabmarket/data_afp/master/data/VC-%s.csv'%afp_name
    afp = pd.read_csv(filename, **karg_csv)
    afp_uf = afp.div(uf.Valor,axis=0)
    
    for fondo in fondos:
        for tipo,vcf in zip(['nominal','real'],[afp, afp_uf]):
            
            # Grafico rentabilidad, rentabilidad acumulada y valor cuota promedio periodo
            # Periodos : W week, , M month, Q quarter, A year
            # Ultimo valor del periodo
            df = vcf.loc['1981':,[fondo]].resample('M').last()
            # Rentabilidad promedio anual = suma rentabilidades mensuales
            aux = df.pct_change(1).resample('A').sum()
            
            if fondo == 'C':
                  # Media movil 10 agnos
                  aux['%s-movil_10'%(fondo)] = aux[[fondo]].rolling(window=10).mean()
            else:
                  # Media movil 5 agnos
                  aux['%s-movil_5'%(fondo)] = aux[[fondo]].rolling(window=5).mean() 
            # Grafo rentabilidad
            fig, ax = plt.subplots(figsize=(8,8))
            # Rentabilidad anual
            titulo = 'Rentabilidad %s Promedio Anual %s fondo %s'%(tipo,afp_name,fondo)
            
            aux['year'] = aux.index.strftime('%Y')
            aux.plot(x='year', y=0,title=titulo, kind='bar', ax=ax)
            aux.plot(x='year', y=1, ax=ax)
            # Fix date format on bar plot with pandas
            # Make most of the ticklabels empty so the labels don't get too crowded
            ticklabels = ['']*len(aux.year.values)
            bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            width, height = bbox.width, bbox.height
            step = int(len(aux.year.values)/(width*1.3))
            # Every step ticklable shows the month, day and year
            ticklabels[::step] = aux.year.values[::step]
            ax.xaxis.set_ticklabels(ticklabels)
            plt.legend(loc=3)
            plt.savefig('rent-%s/rent-%s-%s-%s.png'%(tipo,tipo,afp_name,fondo))
            plt.show()

