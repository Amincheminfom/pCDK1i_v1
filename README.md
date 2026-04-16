# **What is this pCDK1i_v1.0?**

**pCDK1i** stands for **p**redictor of **CDK1** **i**nhibitor. 

It is an online tool hosted on Google Colab [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qQa0GykEpHXavrGyLAdHvFRQ7JsDrvtI?usp=sharing) that predict the CDK1 inhibitory property (1 = Active, 0 = Inactive) of a small molecule and also visualize the molecule.

---
This tool is a part of the manuscript:
> *Multiscale screening integrating machine learning, molecular dynamics simulations and quantum mechanical calculations to identify novel CDK1 inhibitor targeting cancer*. (under preparation)

---

<img src="https://github.com/Amincheminfom/Amincheminfom/blob/main/Amincheminfom1.gif?raw=1" alt= “Amincheminfom_logo” width="350" align="right">

**How to use this?**

1: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qQa0GykEpHXavrGyLAdHvFRQ7JsDrvtI?usp=sharing)

2: Install and import required packages

3: Provide the Smiles of your query moleucle and run the cell

------
**Example Smiles:**

*1. Known CDK1 inhibitor* 
`CN1CC[C@H](c2c(O)cc(O)c3c(=O)cc(-c4ccccc4Cl)oc23)C(O)C1`

*2. Known CDK2 Inactive molecule*
`Cc1cc(Cl)c2cc(C(=O)N[C@H](C)c3ccc(S(=O)(=O)CC(=O)OC(C)(C)C)cc3)n(C)c2c1`

*3. Imatinib*
`Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1`

---
Bugs: If you encounter any bugs, please report the issue to my mail id pharmacist.amin@gmail.com
