# SCuMpy

![Pond SCM](pond-scum.jpg)

Welcome to SCuMpy! The name is intended
to (1) evoke the name of the amazing 
Python library NumPy, and (2) be a 
portmanteau of SCM (Structural Causal Model) 
and python.

A linear SCM is a DAG 
whose arrows are labelled by path coefficients
(a.k.a. gains). If you want to learn 
more about linear SCM, explained 
using my notational conventions 
which are also be SCuMpy’s notational conventions, 
check out my free, open 
source book Bayesuvius. 
Look under the chapter entitled 
“Linear Deterministic Bnets with External Noise”.

In SCuMpy, we use the following simple notation. 
Let $\underline{a}, \underline{b}$ be any 2 
random variables. (I underline random variables instead
of the usual convention of capitalizing them.) Then

$$\text{Covariance}(\underline{a}, \underline{b})=
\langle\underline{a}, 
\underline{b}\rangle$$


$$\text{Standard Deviation of }\underline{a} =
\sigma_{\underline{a}} = \sqrt{
\langle\underline{a}, 
\underline{a}\rangle}$$

$$\text{Correlation}(\underline{a}, \underline{b}) =
\frac{\langle\underline{a}, 
\underline{b}\rangle}
{\sigma_{\underline{a}}\sigma_{\underline{b}}}$$

$$\frac{\partial\underline{a}}{
\partial\underline{b}}=
\frac{\langle\underline{a}, 
\underline{b}\rangle}
{\langle\underline{a}, 
\underline{a}\rangle}
$$

 

