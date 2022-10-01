# -*- coding: utf-8 -*-
"""Final ET001.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ScOz_163ZljzqAiEWtlDOdYv4k7Sil-u

## Installs and Imports
"""

!pip install -Uqq fastbook wandb
import fastbook

from fastbook import *
from fastai.vision.widgets import *
from fastai.callback.wandb import WandbCallback
from fastai.callback.tracker import SaveModelCallback

import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from plotnine import *
import shutil
import wandb

"""## Dataset from Repository


"""

from google.colab import drive
drive.mount('/content/drive')

dblock = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=GrandparentSplitter(valid_name="test"),
    get_y=parent_label,
    item_tfms=Resize(128, method=ResizeMethod.Squish), 
    batch_tfms=aug_transforms(size=128, flip_vert=True),
    )
dls = dblock.dataloaders("/content/drive/MyDrive/ET001/data", bs=128)

dls.train.show_batch(max_n=8, nrows=3)

dls.train.show_batch(max_n=4, nrows=1, unique=True)

"""## Train Model"""

learn = cnn_learner(dls, 
                    resnet34, 
                    metrics=[accuracy, 
                             Precision(average='micro'), 
                             Recall(average='micro'), 
                             F1Score(average='micro')
                             ]
                    ).to_fp16()

learn.fine_tune(epochs=10,
          base_lr=1e-3,
          freeze_epochs=1,
          lr_mult=100,
          pct_start=0.2,
          div=5.0)

dls.valid.show_batch()

learn.recorder.plot_loss()

learn.recorder.plot_sched()

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix(figsize=(12, 12))

interp.print_classification_report()

learn.show_results()