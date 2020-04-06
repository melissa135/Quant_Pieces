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
        self.X = data_source

    def __iter__(self):
        mylist = []
        for i in range(0, self.__len__()):
            if random.random() >= 0.5 :
                mylist.append(i)
        random.shuffle(mylist)
        return iter(mylist)

    def __len__(self):
        return len(self.X)

if __name__ == '__main__':

    x = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
    
    ss = Sample_Set(x)
    ms = My_Sampler(ss)
    dataloader = data.DataLoader(ss, batch_size=2, sampler=ms)

    for batch in range(0, 5):
        print('--------New Batch--------')
        for data in dataloader:
            print(data)
