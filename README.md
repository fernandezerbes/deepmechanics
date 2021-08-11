## deepmechanics

*deepmechanics* is a package for the solution of structural mechanics problems in Python using Artificial Neural Networks (ANN). It is based on the Deep Energy Method [1] and implements a quadtree geometry with Gauss-Legendre quadrature for the computation of the functional (loss function) that is to be minimized.


[1] Vien Minh Nguyen-Thanh, Xiaoying Zhuang, & Timon Rabczuk (2020). A deep energy method for finite deformation hyperelasticity. European Journal of Mechanics - A/Solids, 80, 103874.

---

### Usage

Clone the repository

```shell
git clone https://github.com/FernandezErbes/deepmechanics.git
```

Go to the repository folder and install the package with [pip](https://pypi.org/project/pip/)

```shell
pip install .
```

Create your own drivers by following the [examples](https://github.com/FernandezErbes/deepmechanics/tree/main/examples).

---

### Example results

#### Cantilever beam with uniform load on the top edge
*deepmechanics* results
![cantilever_uy_dm](https://user-images.githubusercontent.com/62465061/128981275-55902480-3881-41f5-9984-3b9f778f39c9.png)

*ANSYS* Finite Element reference solution
![cantilever_uy](https://user-images.githubusercontent.com/62465061/128981225-9f4bd4f7-0f3c-4864-af4f-6db394f923fd.png)

#### Double-clamped beam with uniform load on the top edge
*deepmechanics* results
![double_clamped_uy_dm](https://user-images.githubusercontent.com/62465061/128981681-905a804e-6287-4285-a2ae-407ad94c3ce4.png)

*ANSYS* Finite Element reference solution
![double_clamped_uy](https://user-images.githubusercontent.com/62465061/128981693-ab613942-4ff4-4a0d-9056-da790b8e837a.png)


