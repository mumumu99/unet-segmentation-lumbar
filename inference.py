import matplotlib.pyplot as plt

import torch
from torch.utils.data import DataLoader

from config import argparser
from utils import dice_coeff

class Inference(object):

    def __init__(self, config, model, dataset):
        self.config = config
        self.model = model
        self.dataset = dataset

        self.dataloader = {
            'test': DataLoader(self.dataset['test'], batch_size=1, shuffle=True)
        }

        self.device = torch.device(self.config.device if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def inference(self):
        self.model.load_state_dict(torch.load(self.config.save_folder + "\model-unet.pth"))
        self.model.eval()

        x_test, y_test = next(iter(self.dataloader['test']))
        x_test, y_test = x_test.float(), y_test.float()
        x_test, y_test = x_test.to(self.device), y_test.to(self.device)

        y_pred = self.model(x_test)
        y_pred = y_pred.data.cpu().numpy()
        
        print(y_pred.shape)

        fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(15,15))
        axs.imshow(x_test.data.cpu().numpy()[0, 0])

        for i in range(0, 4):
            # fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15,15))
            fig, axs = plt.subplots(nrows=1, ncols=2)
            axs[0].imshow(y_test.data.cpu().numpy()[0, i])
            axs[1].imshow(y_pred[0, i])

            score = dice_coeff(y_test.data.cpu().numpy()[0, i], y_pred[0, i])
            fig.suptitle('the dice score is {:6f}'.format(score), va='bottom')


def main():
    config, model, dataset = argparser()

    infer = Inference(config, model, dataset)

    infer.inference()


if __name__ == '__main__':
    main()


