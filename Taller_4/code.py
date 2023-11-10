"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        
    def kde_function(signal_x,eval_points=None,method="Silverman",res=500):
    	
        if method == 'Silverman':
            n = len(signal_x)
            sigma = np.std(signal_x)
            optimal_bandwidth = (4 / (3 * n)) ** (1 / 5) * sigma
            print(f'Method:{method}\nOptimal bandwidth: {optimal_bandwidth:.2f}')

        elif method == 'Cross Validation':
            # Define los posibles valores para el ancho de banda
            bandwidths = np.arange(0.05, 2, 0.05)

            # Crea y configura el objeto para la búsqueda en la cuadrícula
            kde = KernelDensity(kernel='gaussian')
            grid = GridSearchCV(kde, {'bandwidth': bandwidths})
            grid.fit(signal_x.reshape(-1, 1))

            # Obtiene el mejor estimador y su ancho de banda óptimo
            kde_optimal = grid.best_estimator_
            optimal_bandwidth = kde_optimal.bandwidth
            print(f'Optimal bandwidth: {optimal_bandwidth:.2f}')

        else:
            print('Error')
            return
            
        kde = scipy.stats.gaussian_kde(signal_x, bw_method=optimal_bandwidth)

        if eval_points is None:
            eval_points = np.linspace(np.min(signal_x), np.max(signal_x),res)
            
        y_sp = kde.pdf(eval_points)
            
        return (eval_points, y_sp)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])