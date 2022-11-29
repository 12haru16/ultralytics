import logging
from pathlib import Path

import torch
from omegaconf import OmegaConf
from tqdm import tqdm

from ultralytics.yolo.engine.trainer import DEFAULT_CONFIG
from ultralytics.yolo.utils import TQDM_BAR_FORMAT
from ultralytics.yolo.utils.files import increment_path
from ultralytics.yolo.utils.ops import Profile
from ultralytics.yolo.utils.torch_utils import de_parallel, select_device


class BaseValidator:
    """
    Base validator class.
    """

    def __init__(self, dataloader, save_dir=None, pbar=None, logger=None, args=None):
        self.dataloader = dataloader
        self.pbar = pbar
        self.logger = logger or logging.getLogger()
        self.args = args or OmegaConf.load(DEFAULT_CONFIG)
        self.device = select_device(self.args.device, dataloader.batch_size)
        self.save_dir = save_dir if save_dir is not None else \
                increment_path(Path(self.args.project) / self.args.name, exist_ok=self.args.exist_ok)
        self.cuda = self.device.type != 'cpu'
        self.batch_i = None
        self.training = True

    def __call__(self, trainer=None, model=None):
        """
        Supports validation of a pre-trained model if passed or a model being trained
        if trainer is passed (trainer gets priority).
        """
        self.training = trainer is not None
        if self.training:
            model = trainer.ema.ema or trainer.model
            self.args.half &= self.device.type != 'cpu'
            model = model.half() if self.args.half else model.float()
            loss = torch.zeros_like(trainer.loss_items, device=trainer.device)
        else:  # TODO: handle this when detectMultiBackend is supported
            assert model is not None, "Either trainer or model is needed for validation"
            # model = DetectMultiBacked(model)
            # TODO: implement init_model_attributes()

        model.eval()

        dt = Profile(), Profile(), Profile(), Profile()
        n_batches = len(self.dataloader)
        desc = self.get_desc()
        # NOTE: keeping this `not self.training` in tqdm will eliminate pbar after finishing segmantation evaluation during training,
        # so I removed it, not sure if this will affect classification task cause I saw we use this arg in yolov5/classify/val.py.
        # bar = tqdm(self.dataloader, desc, n_batches, not self.training, bar_format=TQDM_BAR_FORMAT)
        bar = tqdm(self.dataloader, desc, n_batches, bar_format=TQDM_BAR_FORMAT)
        self.init_metrics(de_parallel(model))
        with torch.no_grad():
            for batch_i, batch in enumerate(bar):
                self.batch_i = batch_i
                # pre-process
                with dt[0]:
                    batch = self.preprocess(batch)

                # inference
                with dt[1]:
                    preds = model(batch["img"])
                    # TODO: remember to add native augmentation support when implementing model, like:
                    #  preds, train_out = model(im, augment=augment)

                # loss
                with dt[2]:
                    if self.training:
                        loss += trainer.criterion(preds, batch)[1]

                # pre-process predictions
                with dt[3]:
                    preds = self.postprocess(preds)

                self.update_metrics(preds, batch)
                if self.args.plots and batch_i < 3:
                    self.plot_val_samples(batch, batch_i)
                    self.plot_predictions(batch, preds, batch_i)

        stats = self.get_stats()
        self.check_stats(stats)

        self.print_results()

        # print speeds
        if not self.training:
            t = tuple(x.t / len(self.dataloader.dataset) * 1E3 for x in dt)  # speeds per image
            # shape = (self.dataloader.batch_size, 3, imgsz, imgsz)
            self.logger.info(
                'Speed: %.1fms pre-process, %.1fms inference, %.1fms loss, %.1fms post-process per image at shape ' % t)

        if self.training:
            model.float()
        # TODO: implement save json

        return stats | trainer.label_loss_items(loss.cpu() / len(self.dataloader), prefix="val") \
                if self.training else stats

    def preprocess(self, batch):
        return batch

    def postprocess(self, preds):
        return preds

    def init_metrics(self):
        pass

    def update_metrics(self, preds, batch):
        pass

    def get_stats(self):
        return {}

    def check_stats(self, stats):
        pass

    def print_results(self):
        pass

    def get_desc(self):
        pass

    @property
    def metric_keys(self):
        return []

    # TODO: may need to put these following functions into callback
    def plot_val_samples(self, batch, ni):
        pass

    def plot_predictions(self, batch, preds, ni):
        pass