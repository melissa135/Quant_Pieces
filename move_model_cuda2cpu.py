import os
import torch
from network_structure import *

path = '/home/zhu/workspace/Stock_Offline/predictor/mlp_encoder_fixed_contract_20200912224927/full'

for i in range(0, 8):  # notice the count
    name = 'aelt_%d.pt'%i
    f_dir = os.path.join(path, name)
    model = torch.load(f_dir).to('cpu')
    torch.save(model, f_dir)
