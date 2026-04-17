# High-Frequency Market Data: Could You Guess the Stock?

**Challenge ENS / CFM 2024** — [challengedata.ens.fr/challenges/146](https://challengedata.ens.fr/participants/challenges/146/)

**Etudiants :** Yassine Mannai & Hugo Rocha Mondragon  
**Enseignant :** Arthur Thomas (Groupe 2)

---

## Contexte

Ce projet s'inscrit dans le cadre du **Data Challenge de l'ENS**, propose par **Capital Fund Management (CFM)**. L'objectif est d'identifier a quel titre financier (parmi 24 stocks) appartient une sequence de 100 evenements tick-by-tick extraits du carnet d'ordres agrege. Il s'agit d'un probleme de **classification multi-classes** (24 classes) evalue a l'**accuracy**.

## Structure du Projet

```
High_Freq_Data/
├── README.md
├── requirements.txt
├── docs/
│   ├── challenge_documentation.md
│   └── Projet_ML.pdf
├── src/
│   └── Mannai(RochaMondragon)_HighFreqData.ipynb
├── data/
│   ├── X_train_N1UvY30.csv
│   ├── X_test_m4HAPAP.csv
│   └── y_train_or6m3Ta.csv
├── output/
│   └── y_pred_submission.csv
└── cours_ml/
```

## Donnees

Le dataset contient des sequences de **100 observations consecutives** du carnet d'ordres. Chaque observation inclut : venue, action (ajout/suppression/mise a jour), side (bid/ask), prix, volumes, flux et indicateur de trade. Les prix sont normalises par rapport au premier bid de chaque sequence.

**Dimensions** : 100 evenements x 20 tirages/stock/jour x 504 jours x 24 stocks = **24 240 000 lignes** (train), soit 242 400 sequences.

## Plan du Notebook

1. Presentation de la problematique
2. Chargement et decomposition des donnees
3. Feature engineering (73 features agregees) & statistiques descriptives
4. Modele de reference (Decision Tree)
5. Modele non supervise (KMeans)
6. Modeles supervises (Random Forest, XGBoost)
7. Methode ensembliste (Stacking)
8. Interpretation (Feature Importance, SHAP)
9. Deep Learning (Transformer Encoder)
10. Comparaison des modeles & Conclusion

## Resultats (validation)

| Modele | Type | Val Accuracy |
|--------|------|-------------|
| **Stacking (XGB+ET+HGB)** | **Ensembliste (stacking)** | **55.68%** |
| XGBoost | Supervise (boosting) | 52.50% |
| Random Forest | Supervise (bagging) | 44.09% |
| Random Forest (Grid Search) | Supervise optimise | 43.61% |
| Decision Tree (depth=15) | Reference | 35.58% |
| Transformer Encoder | Deep Learning sequentiel | 30.26% |

Le **StackingClassifier** combinant XGBoost, ExtraTrees et HistGradientBoosting atteint le meilleur score. Le record du challenge est 63%.

## Installation

```bash
git clone https://github.com/HUGO-ROCHA-MONDRAGON/High_Freq_Data.git
cd High_Freq_Data
pip install -r requirements.txt
```

Les donnees doivent etre telechargees depuis la [page du challenge](https://challengedata.ens.fr/participants/challenges/146/) et placees dans `data/`.

## Technologies

- Python 3.13, NumPy, Pandas, Matplotlib, Seaborn
- scikit-learn (Decision Tree, Random Forest, ExtraTrees, HistGBT, Stacking, KMeans, PCA)
- XGBoost
- PyTorch (Transformer Encoder)
- SHAP

## Equipe

- Hugo Rocha Mondragon
- Yassine Mannai

## Ressources

- [Page du Challenge ENS](https://challengedata.ens.fr/participants/challenges/146/)
- [Site de CFM](https://www.cfm.fr/)
- [Documentation detaillee](docs/challenge_documentation.md)
