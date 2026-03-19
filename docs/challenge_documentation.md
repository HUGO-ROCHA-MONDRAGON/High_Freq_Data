# Documentation Complète — Challenge CFM / ENS 2024

## High-Frequency Market Data: Could You Guess the Stock?

---

## Table des matières

1. [Introduction à la microstructure des marchés](#1-introduction-à-la-microstructure-des-marchés)
2. [Le carnet d'ordres (Order Book)](#2-le-carnet-dordres-order-book)
3. [Données tick-by-tick et Level 3](#3-données-tick-by-tick-et-level-3)
4. [Description formelle du challenge](#4-description-formelle-du-challenge)
5. [Description des features](#5-description-des-features)
6. [Formalisation mathématique](#6-formalisation-mathématique)
7. [Architecture du benchmark](#7-architecture-du-benchmark)
8. [Pistes d'approches](#8-pistes-dapproches)
9. [Glossaire](#9-glossaire)

---

## 1. Introduction à la microstructure des marchés

### 1.1 Qu'est-ce que la microstructure des marchés ?

La **microstructure des marchés** est la branche de la finance qui étudie les mécanismes par lesquels les actifs financiers sont échangés. Elle s'intéresse au **processus de formation des prix**, à la **liquidité**, au **coût des transactions** et au comportement des différents participants du marché.

Contrairement à la finance classique qui considère les prix comme des processus continus (mouvement brownien, Black-Scholes), la microstructure étudie les prix **à l'échelle la plus fine** : chaque ordre individuel, chaque transaction, chaque modification du carnet d'ordres.

### 1.2 Les marchés électroniques modernes

Aujourd'hui, la quasi-totalité des échanges sur actions se fait via des **plateformes électroniques** (exchanges). Pour un même titre, il existe souvent **plusieurs places de marché** :

- **NASDAQ** — marché électronique américain
- **NYSE** — New York Stock Exchange
- **BATS/BATY** — plateformes alternatives (dark pools ou lit markets)
- **ARCA**, **IEX**, etc.

Un même stock peut être acheté ou vendu sur n'importe laquelle de ces plateformes. Le **Consolidated Order Book** (carnet agrégé) fusionne l'information de toutes les venues pour avoir une vue globale.

### 1.3 Les participants du marché

| Participant | Rôle |
|-------------|------|
| **Market Makers** | Fournissent de la liquidité en plaçant des ordres des deux côtés (bid et ask) |
| **Investisseurs institutionnels** | Fonds de pension, assurances, passent de gros ordres |
| **Traders haute fréquence (HFT)** | Algorithmes rapides exploitant les inefficiences de micro-secondes |
| **Investisseurs retail** | Particuliers, ordres de petite taille |

---

## 2. Le carnet d'ordres (Order Book)

### 2.1 Structure du carnet d'ordres

Le carnet d'ordres est le registre central de toutes les offres d'achat et de vente en attente pour un titre donné.

```
         CARNET D'ORDRES
    ┌──────────────────────────┐
    │     ASK (vente)          │
    │  Prix    │  Volume       │
    │──────────│───────────────│
    │  101.05  │  200          │  ← Best Ask (meilleure offre de vente)
    │  101.10  │  500          │
    │  101.15  │  150          │
    │          │               │
    │  ════════════════════    │  ← Spread
    │          │               │
    │  101.00  │  300          │  ← Best Bid (meilleure offre d'achat)
    │  100.95  │  450          │
    │  100.90  │  100          │
    │──────────│───────────────│
    │     BID (achat)          │
    └──────────────────────────┘
```

### 2.2 Définitions clés

**Best Bid** : le prix le plus élevé qu'un acheteur est prêt à payer.

$$P_{\text{bid}} = \max_{i \in \text{ordres d'achat}} P_i$$

**Best Ask** : le prix le plus bas qu'un vendeur est prêt à accepter.

$$P_{\text{ask}} = \min_{i \in \text{ordres de vente}} P_i$$

**Spread** : la différence entre le meilleur ask et le meilleur bid.

$$S = P_{\text{ask}} - P_{\text{bid}}$$

Le spread est un indicateur **fondamental** de la liquidité d'un titre. Un spread étroit signifie que le titre est très liquide (facile à acheter/vendre sans impact de prix).

**Mid-price** : le prix milieu, estimateur du « vrai » prix.

$$P_{\text{mid}} = \frac{P_{\text{ask}} + P_{\text{bid}}}{2}$$

**Bid-Ask Size** : le volume total disponible au meilleur bid/ask.

$$Q_{\text{bid}} = \sum_{i : P_i = P_{\text{bid}}} q_i, \quad Q_{\text{ask}} = \sum_{i : P_i = P_{\text{ask}}} q_i$$

### 2.3 Dynamique du carnet d'ordres

Le carnet évolue à travers trois types d'événements :

| Action | Code | Description |
|--------|------|-------------|
| **Add** | `A` | Un nouveau ordre limite est ajouté au carnet |
| **Delete** | `D` | Un ordre existant est annulé ou exécuté (trade) |
| **Update** | `U` | Un ordre existant est modifié (prix ou quantité) |

Chaque événement est caractérisé par le **flux** — le changement net de volume sur le carnet :

$$\text{flux} = \Delta Q = Q_{\text{après}} - Q_{\text{avant}}$$

- Si flux > 0 : de la liquidité a été **ajoutée** (nouvel ordre)
- Si flux < 0 : de la liquidité a été **retirée** (annulation ou trade)

---

## 3. Données tick-by-tick et Level 3

### 3.1 Les niveaux de données de marché

| Niveau | Nom | Information |
|--------|-----|-------------|
| **Level 1** | Top of Book | Seulement best bid, best ask, dernière transaction |
| **Level 2** | Market Depth | Tout le carnet d'ordres agrégé par niveau de prix |
| **Level 3** | Market-by-Order (MBO) | Chaque ordre individuel avec son identifiant unique |

Le dataset du challenge est de **Level 3 (Market-by-Order)** : chaque mise à jour fournit un identifiant unique (`order_id`) pour l'ordre spécifique qui a été ajouté, modifié ou supprimé.

### 3.2 Pourquoi le Level 3 est précieux

Avec le Level 3, on peut reconstituer le **cycle de vie complet** d'un ordre :

$$\text{Ordre } o : \quad \underbrace{A(t_0)}_{\text{placement}} \rightarrow \underbrace{U(t_1), U(t_2), \ldots}_{\text{modifications}} \rightarrow \underbrace{D(t_n)}_{\text{annulation ou exécution}}$$

On peut mesurer :
- La **durée de vie** des ordres : $\Delta t = t_n - t_0$
- Le **taux d'annulation** vs exécution
- Les **patterns de modification** (ordres déplacés)

### 3.3 Multi-venue et carnet agrégé

Les données proviennent d'un carnet **agrégé** construit à partir de plusieurs venues. Pour un même titre :

$$\text{Best Bid}_{\text{agrégé}} = \max_{\text{venue } v} \text{Best Bid}_v$$

$$\text{Best Ask}_{\text{agrégé}} = \min_{\text{venue } v} \text{Best Ask}_v$$

Le **NBBO** (National Best Bid and Offer) est le meilleur prix disponible tous marchés confondus.

---

## 4. Description formelle du challenge

### 4.1 Problème

Soit $\mathcal{S} = \{s_1, s_2, \ldots, s_{24}\}$ l'ensemble des 24 stocks. Pour chaque observation $i$, on dispose d'une séquence de 100 événements du carnet d'ordres :

$$X_i = (x_i^{(1)}, x_i^{(2)}, \ldots, x_i^{(100)}) \in \mathbb{R}^{100 \times d}$$

où $d$ est la dimension du vecteur de features par événement.

Le but est de trouver une fonction :

$$f : \mathbb{R}^{100 \times d} \rightarrow \{0, 1, \ldots, 23\}$$

telle que $f(X_i) = y_i$ (le stock correspondant).

### 4.2 Dimensions du dataset

| | Valeur |
|---|--------|
| Nombre de stocks | 24 |
| Séquences par stock par jour | 20 |
| Nombre de jours | 504 (~2 ans) |
| Événements par séquence | 100 |
| **Total de lignes** | **24 240 000** |

### 4.3 Normalisation des prix

Pour éviter que le prix absolu ne donne directement l'identité du stock, les prix sont centrés :

$$\tilde{P}_{\text{price}}^{(k)} = P_{\text{price}}^{(k)} - P_{\text{bid}}^{(1)}$$

$$\tilde{P}_{\text{bid}}^{(k)} = P_{\text{bid}}^{(k)} - P_{\text{bid}}^{(1)}$$

$$\tilde{P}_{\text{ask}}^{(k)} = P_{\text{ask}}^{(k)} - P_{\text{bid}}^{(1)}$$

où $k \in \{1, \ldots, 100\}$ est l'indice de l'événement dans la séquence.

### 4.4 Métrique

L'évaluation se fait par **accuracy** (précision de classification) :

$$\text{Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}(\hat{y}_i = y_i)$$

où :
- $N$ est le nombre d'observations de test
- $\hat{y}_i$ est la prédiction du modèle
- $y_i$ est le vrai label (stock)
- $\mathbb{1}(\cdot)$ est la fonction indicatrice

---

## 5. Description des features

### 5.1 Features catégorielles

| Feature | Valeurs | Description |
|---------|---------|-------------|
| `venue` | Entiers (ex: 0, 1, 2, ...) | Place de marché encodée |
| `action` | `A`, `D`, `U` | Type d'événement |
| `side` | `A` (ask), `B` (bid) | Côté du carnet |
| `trade` | True / False | L'événement est-il un trade ? |

### 5.2 Features numériques

| Feature | Type | Description |
|---------|------|-------------|
| `price` | Float | Prix de l'ordre (centré) |
| `bid` | Float | Best bid (centré) |
| `ask` | Float | Best ask (centré) |
| `bid_size` | Int | Volume au best bid agrégé |
| `ask_size` | Int | Volume au best ask agrégé |
| `flux` | Float | Changement de volume sur le carnet |
| `order_id` | Int | ID de l'ordre (0 = premier ordre de la séquence) |

### 5.3 Features dérivées possibles

On peut construire de nombreuses features qui caractérisent un stock :

**Spread moyen** :

$$\bar{S}_i = \frac{1}{100} \sum_{k=1}^{100} (P_{\text{ask}}^{(k)} - P_{\text{bid}}^{(k)})$$

**Déséquilibre du carnet (Order Book Imbalance)** :

$$\text{OBI}^{(k)} = \frac{Q_{\text{bid}}^{(k)} - Q_{\text{ask}}^{(k)}}{Q_{\text{bid}}^{(k)} + Q_{\text{ask}}^{(k)}}$$

OBI ∈ [-1, 1]. Valeur positive = pression acheteuse, négative = pression vendeuse.

**Fréquence des trades** :

$$f_{\text{trade}} = \frac{1}{100} \sum_{k=1}^{100} \mathbb{1}(\text{trade}^{(k)} = \text{True})$$

**Distribution des venues** :

$$p_v = \frac{|\{k : \text{venue}^{(k)} = v\}|}{100}$$

pour chaque venue $v$. La répartition du flux entre venues est caractéristique de chaque stock.

**Volatilité du mid-price** :

$$\sigma_{\text{mid}} = \text{std}\left(\Delta P_{\text{mid}}^{(k)}\right) = \text{std}\left(P_{\text{mid}}^{(k)} - P_{\text{mid}}^{(k-1)}\right)$$

**Taille moyenne des ordres** :

$$\bar{q} = \frac{1}{|\{k : \text{action}^{(k)} = A\}|} \sum_{k : \text{action}^{(k)} = A} |\text{flux}^{(k)}|$$

---

## 6. Formalisation mathématique

### 6.1 Le problème de classification multi-classes

On cherche à minimiser le risque empirique :

$$\hat{f} = \arg\min_{f \in \mathcal{F}} \frac{1}{N} \sum_{i=1}^{N} \mathcal{L}(f(X_i), y_i)$$

où $\mathcal{L}$ est la **cross-entropy** :

$$\mathcal{L}(f(X_i), y_i) = -\sum_{c=0}^{23} \mathbb{1}(y_i = c) \log p_c(X_i)$$

avec $p_c(X_i) = \text{softmax}(z(X_i))_c$ et $z(X_i) \in \mathbb{R}^{24}$ les logits du modèle.

### 6.2 Softmax

La fonction softmax convertit les logits en probabilités :

$$p_c = \frac{e^{z_c}}{\sum_{j=0}^{23} e^{z_j}}, \quad c \in \{0, 1, \ldots, 23\}$$

### 6.3 GRU (Gated Recurrent Unit)

Le benchmark utilise un **Bi-GRU**. Les équations du GRU pour un pas de temps $t$ :

**Porte de mise à jour (update gate)** :

$$z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)$$

**Porte de réinitialisation (reset gate)** :

$$r_t = \sigma(W_r \cdot [h_{t-1}, x_t] + b_r)$$

**État candidat** :

$$\tilde{h}_t = \tanh(W_h \cdot [r_t \odot h_{t-1}, x_t] + b_h)$$

**État caché final** :

$$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$$

où :
- $\sigma$ est la fonction sigmoïde
- $\odot$ est le produit élément par élément (Hadamard)
- $[a, b]$ est la concaténation de vecteurs
- $W_z, W_r, W_h$ sont les matrices de poids
- $b_z, b_r, b_h$ sont les biais

### 6.4 Bidirectional GRU

Le Bi-GRU traite la séquence dans les deux sens :

$$\overrightarrow{h_T} = \text{GRU}_{\text{forward}}(x_1, x_2, \ldots, x_{100}) \in \mathbb{R}^{64}$$

$$\overleftarrow{h_1} = \text{GRU}_{\text{backward}}(x_{100}, x_{99}, \ldots, x_1) \in \mathbb{R}^{64}$$

$$h = [\overrightarrow{h_T} ; \overleftarrow{h_1}] \in \mathbb{R}^{128}$$

### 6.5 Architecture complète du benchmark

$$X_i \in \mathbb{R}^{100 \times d} \xrightarrow{\text{embedding}} T_i \in \mathbb{R}^{100 \times 30} \xrightarrow{\text{Bi-GRU}} h_i \in \mathbb{R}^{128} \xrightarrow{\text{Dense + SeLU}} \mathbb{R}^{64} \xrightarrow{\text{Dense}} z_i \in \mathbb{R}^{24} \xrightarrow{\text{Softmax}} p_i \in \Delta^{23}$$

où $\Delta^{23}$ est le simplexe de probabilité à 24 dimensions.

### 6.6 SeLU (Scaled Exponential Linear Unit)

$$\text{SeLU}(x) = \lambda \begin{cases} x & \text{si } x > 0 \\ \alpha(e^x - 1) & \text{si } x \leq 0 \end{cases}$$

avec $\lambda \approx 1.0507$ et $\alpha \approx 1.6733$.

SeLU a la propriété d'**auto-normaliser** les activations, ce qui stabilise l'entraînement sans nécessiter de batch normalization.

---

## 7. Architecture du benchmark

### 7.1 Preprocessing

```
                    Données brutes par événement
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                     │
    venue (int)          action (cat)          trade (bool)
         │                    │                     │
    Embedding(8)         Embedding(8)          Embedding(8)
         │                    │                     │
         └────────────────────┼────────────────────┘
                              │
                    Concaténation avec
               bid, ask, price, log(bid_size+1),
               log(ask_size+1), log(flux)
                              │
                     Vecteur ∈ ℝ³⁰
```

### 7.2 Modèle

```
        Séquence (100, 30)
               │
     ┌─────────┴─────────┐
     │                    │
  GRU Forward          GRU Backward
  (dim=64)             (dim=64)
     │                    │
  h_T ∈ ℝ⁶⁴           h_1 ∈ ℝ⁶⁴
     │                    │
     └────────┬───────────┘
              │
       Concat → ℝ¹²⁸
              │
       Dense → ℝ⁶⁴
              │
           SeLU
              │
       Dense → ℝ²⁴
              │
          Softmax
              │
       Probabilités (24 classes)
```

### 7.3 Entraînement

| Paramètre | Valeur |
|-----------|--------|
| Loss | Cross-Entropy |
| Optimiseur | Adam (Optax) |
| Learning rate | $3 \times 10^{-3}$ |
| Batch size | 1 000 |
| Nombre de batches | 10 000 |
| Framework | JAX / Optax / Flax |

---

## 8. Pistes d'approches

### 8.1 Feature Engineering

Construire des **statistiques agrégées** sur chaque séquence de 100 événements :

- **Statistiques de spread** : moyenne, écart-type, min, max
- **Order Book Imbalance** : moyenne, tendance
- **Profil de venue** : distribution de fréquence des venues
- **Profil d'action** : ratio A/D/U
- **Taux de trade** : proportion d'événements qui sont des trades
- **Statistiques de taille** : distribution de bid_size, ask_size, flux
- **Dynamique temporelle** : autocorrélation du mid-price, vitesse de changement

### 8.2 Approches classiques ML

- **Random Forest / XGBoost** sur les features agrégées
- **LightGBM** avec features statistiques
- Avantage : rapide, interprétable, bon baseline

### 8.3 Approches Deep Learning

- **LSTM / GRU** (comme le benchmark)
- **Transformer** avec self-attention sur la séquence
- **1D-CNN** pour capturer des patterns locaux
- **Temporal Convolutional Network (TCN)**

### 8.4 Approches hybrides

Combiner features agrégées et features apprises (attention aux embeddings de venue qui sont très informatifs).

### 8.5 Indices importants pour la classification

Pourquoi peut-on identifier un stock à partir de données apparemment anonymes ?

1. **Le spread moyen** est caractéristique de chaque stock (dépend de la liquidité, du prix, de la capitalisation)
2. **La répartition entre venues** dépend des accords de market making et de la taille du stock
3. **La taille typique des ordres** varie selon la liquidité
4. **La fréquence des trades** est fonction de la popularité du stock
5. **La volatilité intra-jour** est propre à chaque titre
6. **Le tick-size relatif** (taille minimale de variation / prix) est un signal fort

---

## 9. Glossaire

| Terme | Définition |
|-------|------------|
| **Ask** | Prix le plus bas auquel un vendeur est prêt à vendre |
| **Bid** | Prix le plus élevé qu'un acheteur est prêt à payer |
| **Book / Order Book** | Registre de tous les ordres limites en attente |
| **Cross-Entropy** | Fonction de perte pour la classification |
| **Dark Pool** | Plateforme de trading où les ordres ne sont pas visibles |
| **Flux** | Changement net de volume sur un niveau de prix |
| **GRU** | Gated Recurrent Unit, réseau récurrent |
| **HFT** | High-Frequency Trading, trading haute fréquence |
| **Level 3 / MBO** | Données Market-by-Order, avec ordre individuel identifiable |
| **Liquidité** | Facilité d'acheter/vendre sans impacter le prix |
| **Market Maker** | Participant fournissant de la liquidité des deux côtés |
| **Mid-price** | Moyenne du best bid et best ask |
| **NBBO** | National Best Bid and Offer (meilleur prix agrégé) |
| **Order Book Imbalance** | Déséquilibre entre volume bid et ask |
| **Softmax** | Fonction transformant des logits en probabilités |
| **Spread** | Différence entre best ask et best bid |
| **Tick** | Plus petite variation de prix possible |
| **Tick-by-tick** | Données enregistrant chaque événement individuel |
| **Venue** | Plateforme/place de marché d'exécution |
| **Volatilité** | Mesure de la dispersion des rendements |

---

*Document préparé dans le cadre du Data Challenge ENS/CFM 2024*
