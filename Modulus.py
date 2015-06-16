import numpy as np

import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib

  
def modulus(limit):
    """From the following:
    http://matplotlib.org/examples/pylab_examples/clippedline.html
    http://matplotlib.org/examples/pylab_examples/annotation_demo.html"""
    Y = 36000
    U = 58000
    E = 29000000
    eY = 0.03
    eU = 0.2
    points = {'yield':Y/E,
             'plastic':0.03,
             'ultimate':0.2}
    e = points[limit]
    
    x = np.linspace(0.0, e, 240)
    def svs(ep):
        yield_limit = Y/E
        harding = 0.03
        fracture = 0.2
        if ep <= yield_limit:
            s = E * ep
        elif yield_limit < ep <=harding:
            s = E * yield_limit
        elif harding < ep <= fracture:
            
            s = Y +(U-Y)*(1 - ((ep-eU)**2/(eU-eY)**2))**0.5
        return s
#     print(len(x))
    y = [svs(ep) for ep in x.tolist()]
#     print(y)
    fig = plt.figure(figsize=(6.5875, 6.2125))
    ax = fig.add_subplot(111, autoscale_on=False)
#     ax = plt.subplot(111, autoscale_on=False)
    ax.set_xlim(0,e*1.05)
    ylim = np.ceil(max(y)/10000)*10000
    ax.set_ylim(0,ylim)
    ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_title('A36 Steel %s Range'%(limit.title()))
    ax.set_xlabel('Strain ($\epsilon$) in 'r'$\frac{in}{in}$')
    ax.set_ylabel('Stress ($\sigma$) in $psi$')
    
    if limit =='yield':
        ax.annotate(r'$\sigma = E \times \epsilon$', xy=(.45, .55),  xycoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center')
    elif limit == 'plastic':
        ax.annotate(r'$\sigma = E \times \epsilon_{yield}$', xy=(.5, .8),  xycoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center')
    elif limit == 'ultimate':
        ax.annotate(r'Strain Hardening', xy=(.5, .8),  xycoords='axes fraction',
                    horizontalalignment='center', verticalalignment='center')
    ax.plot(x, y)
    plt.grid(True)
    plt.show()
