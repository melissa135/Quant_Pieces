import random
import torch.utils.data as data

class Sample_Set(data.Dataset):

    def __init__(self, X):
        super(Sample_Set, self).__init__()
        self.X = X

    def __getitem__(self, index):
        data = self.X[index]
        return data

    def __len__(self):
        return len(self.X)

class My_Sampler(data.Sampler):

    def __init__(self, data_source):
        self.data_source = data_source
        self.mylist = data_source

    def __iter__(self):
        self.mylist = []
        for i in range(0, self.num_samples):
            if random.random() >= 0.5 :
                self.mylist.append(i)
        random.shuffle(self.mylist)
        return iter(self.mylist)

    @property
    def num_samples(self):
        return len(self.data_source)

    def __len__(self):
        return self.num_samples

if __name__ == '__main__':

    x = [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ]
    
    ss = Sample_Set(x)
    ms = My_Sampler(ss)
    dataloader = data.DataLoader(ss, batch_size=2, sampler=ms, drop_last=True)
    
    for epoch in range(0, 10):
        print('--------New epoch--------')
        for i, d in enumerate(dataloader, 0):
            #if random.random() <= 0.5:  #
            #    continue  #
            print(d)

    for epoch in range(0, 10):
        print('--------New New epoch--------')
        for i, d in enumerate(dataloader, 0):
            #if random.random() <= 0.5:  #
            #    continue  #s
            print(d)

    xx = [ 0, 1, 2, 3, 4 ]
    sss = Sample_Set(xx)
    concat_x = data.ConcatDataset([ss, sss])

    for i in range(0, concat_x.__len__()):
        print(concat_x.__getitem__(i))
