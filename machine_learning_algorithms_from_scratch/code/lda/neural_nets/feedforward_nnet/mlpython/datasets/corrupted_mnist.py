# Copyright 2011 Hugo Larochelle. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
#    1. Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
# 
#    2. Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY Hugo Larochelle ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Hugo Larochelle OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those of the
# authors and should not be interpreted as representing official policies, either expressed
# or implied, of Hugo Larochelle.

"""
Module ``datasets.corrupted_mnist`` gives access to the corrupted MNIST dataset.

This is a multi-label classification dataset, where the task is to
reconstruct the original binary image of an MNIST digit from a corrupted
version of it. The corruption was generated by randomly flipping a subset
of the pixels in the original image.

The original dataset from http://yann.lecun.com/exdb/mnist/ has been
preprocessed so that the inputs are binary. Corrupted MNIST was
generated by Volodymyr Mnih.


| **References:**
| The MNIST database of handwritten digits
| LeCun and Cortes
| http://yann.lecun.com/exdb/mnist/

"""

import mlpython.misc.io as mlio
import numpy as np
import os
from gzip import GzipFile as gfile

def load(dir_path,load_to_memory=False):
    """
    Loads the corrupted MNIST dataset.

    The data is given by a dictionary mapping from strings
    ``'train'``, ``'valid'`` and ``'test'`` to the associated pair of data and metadata.
    
    The inputs and targets have been converted to a binary format.

    **Defined metadata:**

    * ``'input_size'``
    * ``'target_size'``
    * ``'length'``

    """
    
    input_size=784
    target_size=784
    dir_path = os.path.expanduser(dir_path)

    def load_line(line):
        tokens = line.split()
        return (np.array([int(i) for i in tokens[:input_size]]), np.array([int(i) for i in tokens[input_size:]]))

    train_file,valid_file,test_file = [os.path.join(dir_path, 'corrupted_mnist_' + ds + '.txt') for ds in ['train','valid','test']]
    # Get data
    train,valid,test = [mlio.load_from_file(f,load_line) for f in [train_file,valid_file,test_file]]

    lengths = [50000,10000,10000]
    if load_to_memory:
        train,valid,test = [mlio.MemoryDataset(d,[(input_size,),(target_size,)],[np.float64,np.float64],l) for d,l in zip([train,valid,test],lengths)]
        
    # Get metadata
    train_meta,valid_meta,test_meta = [{'input_size':input_size,'target_size':target_size,
                                        'length':l} for l in lengths]
    
    return {'train':(train,train_meta),'valid':(valid,valid_meta),'test':(test,test_meta)}


def obtain(dir_path):
    """
    Downloads the dataset to ``dir_path``.
    """

    dir_path = os.path.expanduser(dir_path)
    print 'Downloading the dataset'
    import urllib
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/corrupted_mnist/mnist_corrupted_u.mat',os.path.join(dir_path,'mnist_corrupted_u.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/corrupted_mnist/mnist_corrupted_v.mat',os.path.join(dir_path,'mnist_corrupted_v.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/corrupted_mnist/mnist_corrupted_valid_u.mat',os.path.join(dir_path,'mnist_corrupted_valid_u.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/corrupted_mnist/mnist_corrupted_valid_v.mat',os.path.join(dir_path,'mnist_corrupted_valid_v.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/corrupted_mnist/mnist_corrupted_test_u.mat',os.path.join(dir_path,'mnist_corrupted_test_u.mat'))
    urllib.urlretrieve('http://www.cs.toronto.edu/~larocheh/public/datasets/corrupted_mnist/mnist_corrupted_test_v.mat',os.path.join(dir_path,'mnist_corrupted_test_v.mat'))

    # Writing everything into text files, to allow for not loading the data into memory
    def write_to_txt_file(u,v,filename):
        f = open(filename,'w')
        for u_t,v_t in zip(u,v):
            for i in range(len(u_t)):
                f.write(str(int(u_t[i]>127))+' ')
            for i in range(len(v_t)-1):
                f.write(str(int(v_t[i]>127))+' ')
            f.write(str(int(v_t[-1]>127))+'\n')
        f.close()

    import scipy.io
    u = scipy.io.loadmat(os.path.join(dir_path,'mnist_corrupted_u.mat'))['dat']
    v = scipy.io.loadmat(os.path.join(dir_path,'mnist_corrupted_v.mat'))['dat']
    write_to_txt_file(u,v,os.path.join(dir_path,'corrupted_mnist_train.txt'))

    u = scipy.io.loadmat(os.path.join(dir_path,'mnist_corrupted_valid_u.mat'))['dat']
    v = scipy.io.loadmat(os.path.join(dir_path,'mnist_corrupted_valid_v.mat'))['dat']
    write_to_txt_file(u,v,os.path.join(dir_path,'corrupted_mnist_valid.txt'))

    u = scipy.io.loadmat(os.path.join(dir_path,'mnist_corrupted_test_u.mat'))['dat']
    v = scipy.io.loadmat(os.path.join(dir_path,'mnist_corrupted_test_v.mat'))['dat']
    write_to_txt_file(u,v,os.path.join(dir_path,'corrupted_mnist_test.txt'))

    print 'Done                     '
