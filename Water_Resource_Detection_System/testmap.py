from staticmap import StaticMap, CircleMarker
import numpy as np
a=open('loc_data.csv','r')
data=np.loadtxt(a,delimiter=',')
c=1
for i in data:
    m =StaticMap(300,300,10)
    wc=(i[1],i[0])
    marker_outline = CircleMarker(wc, 'white',9)
    marker = CircleMarker(wc, '#0036FF',6)
    m.add_marker(marker_outline)
    m.add_marker(marker)
    image = m.render(zoom=12)
    s='map'+str(c)+'.png'
    image.save(s)
    c=c+1
