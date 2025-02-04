import torch
from repsim.types import CorrType
from repsim.repsim import Stress, GeneralizedShapeMetric, AffineInvariantRiemannian, Corr


def compare(x: torch.Tensor, y: torch.Tensor, method: str = 'stress', **kwargs) -> torch.Tensor:
    meths = {
        'stress': Stress(),
        'generalized_shape_metric': GeneralizedShapeMetric(),
        'riemannian': AffineInvariantRiemannian(),
        'spearman': Corr(corr_type=CorrType.SPEARMAN),
        'pearson': Corr(corr_type=CorrType.PEARSON),
    }

    if method.lower() not in meths:
        raise ValueError(f'Unrecognized Representational Similarity Method "{method}"')

    return meths[method.lower()].compare(x, y, **kwargs)
