"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to _init_  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def _init_(self, p_simbol_0=0.5, a0=-1, a1=1, Nsamples=20, Nsymbols=100 ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block._init_(
            self,
            name='Generador de Simbolos',   # will show up in GRC
            in_sig= None, #[np.float32],
            out_sig=[np.float32]
        )
        
        self.p_0 = p_simbol_0 #probabilidad de generación símbolo 1
        self.p_1 = 1-self.p_0 #probabilidad de generación símbolo 2
        self.a0 = a0
        self.a1 = a1

        self.Nsymbols = Nsymbols
        self.Nsamples = Nsamples

        self.N = Nsymbols * Nsamples 
        
        
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def work(self, input_items, output_items):
        # Genera una secuencia de símbolos basados en las probabilidades dadas
        data = np.random.choice([self.a0, self.a1], size=self.Nsymbols, p=[self.p_0, self.p_1])
        # Repite cada símbolo según el número de muestras por símbolo
        data = np.concatenate([[v]*self.Nsamples for v in data])
        message = data  # Almacena la secuencia completa en la variable 'message'
        """example: multiply with constant"""
        
        for i in range(len(message)):
        	output_items[0][i] =  message[i]
        
        return len(output_items[0])
    
        