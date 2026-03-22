# 📊 High-Frequency Market Data: Could You Guess the Stock?

> **Challenge ENS / CFM 2024** — [challengedata.ens.fr/challenges/146](https://challengedata.ens.fr/participants/challenges/146/)

## 🏢 Contexte

Ce projet s'inscrit dans le cadre du **Data Challenge de l'ENS**, proposé par **Capital Fund Management (CFM)**, un gestionnaire d'actifs alternatifs pionnier dans le domaine du **trading quantitatif** appliqué aux marchés financiers mondiaux.

## 🎯 Objectif du Challenge

L'objectif est d'**identifier à quel titre financier (stock) appartient un extrait de données tick-by-tick** issues du carnet d'ordres (order book). Il s'agit d'un problème de **classification multi-classes** (24 classes = 24 actions différentes).

Les données incluent chaque mise à jour atomique du carnet d'ordres agrégé (construit à partir de plusieurs places de marché), contenant :
- Les meilleurs prix bid/ask
- Les transactions (trades)
- Les ordres placés ou annulés

## 📁 Structure du Projet

```
High_Freq_Data/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── docs/
│   ├── challenge_documentation.md     # Documentation détaillée du challenge
│   └── Projet_ML.pdf                  # Sujet du projet (M2 IEF 2025/2026)
├── src/
│   └── Mannai(RochaMondragon)_HighFreqData.ipynb  # Notebook principal
├── data/                              # Données du challenge (Git LFS)
│   ├── X_train_N1UvY30.csv
│   ├── X_test_m4HAPAP.csv
│   └── y_train_or6m3Ta.csv
├── output/                            # Prédictions et soumissions
│   └── y_pred_submission.csv          # Fichier de soumission généré
└── cours_ml/                          # Cours de Machine Learning (non versionné)
```

## 📊 Description des Données

### Input (X)

Le dataset est composé de séquences de **100 observations consécutives** du carnet d'ordres. Chaque observation contient :

| Colonne | Description |
|---------|-------------|
| `obs_id` | Identifiant unique d'une séquence de 100 événements tirés d'un stock/jour aléatoire |
| `venue` | Place de marché (NASDAQ, BATY, etc.), encodée en entier |
| `action` | Type d'événement : `A` (ajout), `D` (suppression), `U` (mise à jour) |
| `order_id` | Identifiant unique de l'ordre (obfusqué, commence à 0 par séquence) |
| `side` | Côté du carnet : `A` (ask) ou `B` (bid) |
| `price` | Prix de l'ordre affecté (centré par rapport au premier bid) |
| `bid` | Meilleur prix bid du carnet agrégé |
| `ask` | Meilleur prix ask du carnet agrégé |
| `bid_size` | Volume au meilleur bid du carnet agrégé |
| `ask_size` | Volume au meilleur ask du carnet agrégé |
| `flux` | Changement de volume sur le carnet causé par l'événement |
| `trade` | Booléen indiquant si l'événement provient d'un trade ou d'une annulation |

**Dimensions** : 100 événements × 20 tirages/stock/jour × 504 jours × 24 stocks = **24 240 000 lignes**

> Les prix (`price`, `bid`, `ask`) sont **normalisés** en soustrayant le meilleur bid du premier événement de chaque séquence de 100.

### Output (Y)

`eqt_code_cat` : entier entre **0 et 23** identifiant le stock.

### Split temporel

- **Train** : première période temporelle
- **Test** : période future différente (mêmes 24 stocks)

## 🏆 Métrique d'Évaluation

La métrique utilisée est l'**accuracy** (taux de classification correcte) :

$$\text{Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}(\hat{y}_i = y_i)$$

## 🔧 Benchmark (fourni par CFM)

### Prétraitement

Chaque observation est transformée en un tenseur de forme **(100, 30)** :

| Feature | Dimension |
|---------|-----------|
| Embedding de `venue` | 8 |
| Embedding de `action` | 8 |
| Embedding de `trade` | 8 |
| `bid` | 1 |
| `ask` | 1 |
| `price` | 1 |
| `log(bid_size + 1)` | 1 |
| `log(ask_size + 1)` | 1 |
| `log(flux)` | 1 |
| **Total** | **30** |

### Architecture

- **Bi-GRU** (2 cellules GRU de dimension 64 : forward + backward)
- Concaténation → vecteur de 128 dimensions
- Dense 128 → 64 + activation **SeLU**
- Dense 64 → 24 (logits) + **Softmax**

### Entraînement

- **Loss** : Cross-Entropy
- **Batch size** : 1 000 observations aléatoires → tenseur (1000, 100, 30)
- **Optimiseur** : Adam (paramètres par défaut Optax, lr = 3×10⁻³)
- **Itérations** : 10 000 batches

## 🚀 Pour Commencer

```bash
# Cloner le repo
git clone https://github.com/HUGO-ROCHA-MONDRAGON/High_Freq_Data.git
cd High_Freq_Data

# Installer les dépendances
pip install -r requirements.txt

# Télécharger les données depuis le site du challenge
# https://challengedata.ens.fr/participants/challenges/146/
# et les placer dans data/

# Lancer le notebook
jupyter notebook src/Mannai\(RochaMondragon\)_HighFreqData.ipynb
```

## 📓 Notebook

Le notebook `src/Mannai(RochaMondragon)_HighFreqData.ipynb` couvre les étapes suivantes :

1. Présentation de la problématique
2. Chargement et décomposition des données (train/validation/test)
3. Feature engineering & statistiques descriptives
4. Modèle de référence — Arbre de Décision
5. Modèle non supervisé — KMeans (k=24) + méthode du coude + visualisation PCA
6. Modèle supervisé — Random Forest + SVM (RBF) + Grid Search + validation croisée
7. Interprétation — Feature Importance + SHAP
8. Deuxième méthode ensembliste — Gradient Boosting
9. Comparaison des modèles & génération du fichier de soumission

## 📈 Résultats Actuels (validation)

| Modèle | Val Accuracy |
|--------|--------------|
| Decision Tree | 0.3253 |
| Random Forest | 0.4361 |
| Random Forest (Grid Search) | 0.4386 |
| SVM (RBF) | 0.2744 |
| Gradient Boosting | **0.4882** |
| KMeans (alignement optimal) | 0.0485 |

Métriques non supervisées (KMeans) : **ARI = 0.0164**, **NMI = 0.0946**.

Meilleur modèle actuel : **Gradient Boosting**.

## 👥 Équipe

- Hugo Rocha Mondragon
- Yassine Mannai

## 📚 Ressources

- [Page du Challenge ENS](https://challengedata.ens.fr/participants/challenges/146/)
- [Site de CFM](https://www.cfm.fr/)
- [Documentation détaillée](docs/challenge_documentation.md)

## ✅ TODO (prochaines étapes)

- Vérifier la robustesse (stabilité des scores avec plusieurs seeds et folds).
- Finaliser l'analyse SHAP (interprétation globale + quelques cas locaux).
- Générer et valider le fichier de soumission final sur la plateforme ENS.
