from torch.utils.data import DataLoader
from pitch.data_utils import DistributedBucketSampler
from pitch.data_utils import TextAudioLoader
from pitch.data_utils import TextAudioCollate


def create_dataloader_train(hps, n_gpus, rank):
    collate_fn = TextAudioCollate()
    train_dataset = TextAudioLoader(hps.data.training_files, hps.data)
    train_sampler = DistributedBucketSampler(
        train_dataset,
        hps.train.batch_size,
        [32, 300, 400, 500, 600, 700, 800, 900, 1000],
        num_replicas=n_gpus,
        rank=rank,
        shuffle=True)
    train_loader = DataLoader(
        train_dataset,
        num_workers=4,
        shuffle=False,
        pin_memory=True,
        collate_fn=collate_fn,
        batch_sampler=train_sampler)
    return train_loader


def create_dataloader_eval(hps):
    collate_fn = TextAudioCollate()
    eval_dataset = TextAudioLoader(hps.data.validation_files, hps.data)
    eval_loader = DataLoader(
        eval_dataset,
        num_workers=2,
        shuffle=False,
        batch_size=hps.train.batch_size,
        pin_memory=True,
        drop_last=False,
        collate_fn=collate_fn)
    return eval_loader
