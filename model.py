import torch, torch.nn as nn

# IMPLEMENTED FROM SCRATCH FOR LEARNING PURPOSES
TIERS = ['DIAMOND','EMERALD','PLATINUM','GOLD','SILVER','BRONZE','IRON']
UNTIERED = ['challenger','grandmaster','master']
DIVISIONS = ['I','II','III','IV']

class Head(nn.Module):
    def __init__(self,headsize):
        super().__init__()
        self.key = nn.Linear()
        self.query = nn.Linear()
        self.value = nn.Linear()
    
    def forward():
        pass


class MultiHeadAttention(nn.Module):
    def __init__(self,heads,headsize) -> None:
        super().__init__()
    
    

