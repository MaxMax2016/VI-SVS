import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import torch
import argparse

from pitch.models import PitchDiffusion


def load_model(checkpoint_path, model):
    assert os.path.isfile(checkpoint_path)
    checkpoint_dict = torch.load(checkpoint_path, map_location="cpu")
    saved_state_dict = checkpoint_dict["model_g"]
    if hasattr(model, "module"):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    new_state_dict = {}
    for k, v in state_dict.items():
        try:
            new_state_dict[k] = saved_state_dict[k]
        except:
            new_state_dict[k] = v
    if hasattr(model, "module"):
        model.module.load_state_dict(new_state_dict)
    else:
        model.load_state_dict(new_state_dict)
    return model


def save_model(model, checkpoint_path):
    if hasattr(model, 'module'):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    torch.save({'model_g': state_dict}, checkpoint_path)


def main(args):
    model = PitchDiffusion()
    load_model(args.model, model)
    save_model(model, "pit_opencpop.pt")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=True,
                        help="yaml file for config. will use hp_str from checkpoint if not given.")
    parser.add_argument('-m', '--model', type=str, required=True,
                        help="path of checkpoint pt file for evaluation")
    args = parser.parse_args()

    main(args)
