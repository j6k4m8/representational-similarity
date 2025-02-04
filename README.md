(Metric) Representational Similarity Analysis in PyTorch
========================================================

This repository provides the `repsim` package for comparing representational similarity in PyTorch.

See [rsatoolbox](https://github.com/rsagroup/rsatoolbox) for a more mature and fully-featured toolbox. In contrast, this
repository
- does everything in PyTorch, so the outputs are in principle differentiable.
- provides kernel-based methods such as CKA.
- provides metric RSA methods of [Williams et al. (2021)](http://arxiv.org/abs/2110.14739) and [Shahbazi et al. (2021)](https://doi.org/10.1016/j.neuroimage.2021.118271).

## Terminology

- Here, a **neural representation** refers to a `n` by `d` matrix containing the activity of `d` neurons in
response to `n` inputs.
- **Similarity** and **distance** are essentially inverses. Similarity is high when distance is low, and vice versa.
Both are (with few exceptions) non-negative quantities.
- **Pairwise similarity** refers to a `n` by `n` matrix of similarity scores among all pairs of input-items for a given 
neural representation. Likewise, **pairwise distance** is `n` by `n` but contains distances rather than similarities.
- **Representational similarity** is a scalar score that is large when two neural representations are similar to each
other. **Representational distance** is likewise a scalar that is large when two representations are dissimilar.

## Design

There are two core operations of any measure of representational similarity:

1. Computing **pairwise similarity** (or **pairwise distance**). The result is a `n` by `n` Representational Similarity
Matrix (RSM) (or Representational Distance Matrix (RDM)). 
2. Comparing two RSMs (or RDMs) to each other to get a scalar **representational similarity** (or distance) score. 

Step 1 is handled by functions in the `repsim.pairwise` module. See the `repsim.pairwise.compare()` function to get started.

Step 2 is handled by the top-level `repsim.compare()` function.

In some special circumstances, we can take computational shortcuts bypassing Step 1, so most users will not explicitly
call anything inside `repsim.pairwise`.

Applying the kernel trick is central to some of the representational similarity measures we use. The `repsim.kernels`
module contains the kernel logic. By default, `repsim` makes all pairwise comparisons using a Squared Exponential kernel
whose length scale adapts to the median Euclidean distance of the given data. This can be overridden in most places by
specifying a `kernel` keyword argument to `repsim.pairwise.compare`, or a `kernel_x` and `kernel_y` argument to
`repsim.compare`. For example:
```python
import repsim
import repsim.kernels
import repsim.pairwise
import torch

n, d = 10, 3
x = torch.randn(n, d)

# Get pairwise distances using squared exponential kernel with an automatic length-scale (the default)
rdm_default = repsim.pairwise.compare(x)

# Get pairwise distances using laplace kernel with an automatic length-scale
k = repsim.kernels.Laplace()
rdm_laplace = repsim.pairwise.compare(x, kernel=k)

# Get pairwise distances using squared exponential kernel with a custom length-scale
k = repsim.kernels.SquaredExponential(length_scale=0.2)
rdm_sqexp_short = repsim.pairwise.compare(x, kernel=k)
```