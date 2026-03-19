"""Generate a PDF documentation for the CFM / ENS Data Challenge."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Challenge CFM / ENS 2024 - High Frequency Market Data", align="C")
        self.ln(10)
        self.set_draw_color(0, 102, 204)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, title)
        self.ln(8)
        self.set_draw_color(0, 102, 204)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 76, 153)
        self.cell(0, 10, title)
        self.ln(8)

    def subsection_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(51, 51, 51)
        self.cell(0, 8, title)
        self.ln(7)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def formula(self, text):
        self.set_font("Courier", "", 10)
        self.set_text_color(139, 0, 0)
        self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 6, f"  {text}", fill=True)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        self.ln(3)

    def bullet(self, text, indent=15):
        x = self.get_x()
        self.set_x(x + indent)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        self.multi_cell(0, 5.5, f"- {text}")
        self.ln(1)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 76, 153)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, cols, widths, fill=False):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(33, 33, 33)
        if fill:
            self.set_fill_color(240, 245, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6.5, col, border=1, fill=fill, align="C" if i == 0 else "L")
        self.ln()


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# ============================================================
# TITLE PAGE
# ============================================================
pdf.add_page()
pdf.ln(40)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 15, "Challenge Data ENS / CFM 2024", align="C")
pdf.ln(20)
pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(0, 102, 204)
pdf.cell(0, 12, "High-Frequency Market Data:", align="C")
pdf.ln(12)
pdf.cell(0, 12, "Could You Guess the Stock?", align="C")
pdf.ln(25)
pdf.set_draw_color(0, 102, 204)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(15)
pdf.set_font("Helvetica", "", 13)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, "Documentation et Guide du Challenge", align="C")
pdf.ln(30)
pdf.set_font("Helvetica", "I", 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "Hugo Rocha Mondragon & Yassine Mannai", align="C")
pdf.ln(8)
pdf.cell(0, 8, "Mars 2026", align="C")

# ============================================================
# TABLE OF CONTENTS
# ============================================================
pdf.add_page()
pdf.chapter_title("Table des matieres")
toc = [
    "1. Introduction a la microstructure des marches",
    "2. Le carnet d'ordres (Order Book)",
    "3. Donnees tick-by-tick et Level 3",
    "4. Description formelle du challenge",
    "5. Description des features",
    "6. Formalisation mathematique",
    "7. Architecture du benchmark",
    "8. Pistes d'approches",
    "9. Glossaire",
]
for item in toc:
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 76, 153)
    pdf.cell(0, 8, item)
    pdf.ln(7)

# ============================================================
# 1. MICROSTRUCTURE
# ============================================================
pdf.add_page()
pdf.chapter_title("1. Introduction a la microstructure des marches")

pdf.section_title("1.1 Qu'est-ce que la microstructure des marches ?")
pdf.body_text(
    "La microstructure des marches est la branche de la finance qui etudie les mecanismes "
    "par lesquels les actifs financiers sont echanges. Elle s'interesse au processus de "
    "formation des prix, a la liquidite, au cout des transactions et au comportement des "
    "differents participants du marche."
)
pdf.body_text(
    "Contrairement a la finance classique qui considere les prix comme des processus continus "
    "(mouvement brownien, Black-Scholes), la microstructure etudie les prix a l'echelle la "
    "plus fine : chaque ordre individuel, chaque transaction, chaque modification du carnet."
)

pdf.section_title("1.2 Les marches electroniques modernes")
pdf.body_text(
    "Aujourd'hui, la quasi-totalite des echanges sur actions se fait via des plateformes "
    "electroniques (exchanges). Pour un meme titre, il existe souvent plusieurs places de marche :"
)
pdf.bullet("NASDAQ - marche electronique americain")
pdf.bullet("NYSE - New York Stock Exchange")
pdf.bullet("BATS/BATY - plateformes alternatives")
pdf.bullet("ARCA, IEX, etc.")
pdf.body_text(
    "Un meme stock peut etre achete ou vendu sur n'importe laquelle de ces plateformes. "
    "Le Consolidated Order Book (carnet agrege) fusionne l'information de toutes les venues."
)

pdf.section_title("1.3 Les participants du marche")
w = [45, 145]
pdf.table_header(["Participant", "Role"], w)
pdf.table_row(["Market Makers", "Fournissent de la liquidite des deux cotes (bid et ask)"], w)
pdf.table_row(["Institutionnels", "Fonds de pension, assurances, gros ordres"], w, True)
pdf.table_row(["HFT", "Algorithmes rapides exploitant les inefficiences"], w)
pdf.table_row(["Retail", "Particuliers, ordres de petite taille"], w, True)

# ============================================================
# 2. ORDER BOOK
# ============================================================
pdf.add_page()
pdf.chapter_title("2. Le carnet d'ordres (Order Book)")

pdf.section_title("2.1 Structure du carnet d'ordres")
pdf.body_text(
    "Le carnet d'ordres est le registre central de toutes les offres d'achat et de vente "
    "en attente pour un titre donne. Il est organise en deux cotes :"
)
pdf.bullet("Cote ASK (vente) : ordres limites de vente, tries par prix croissant")
pdf.bullet("Cote BID (achat) : ordres limites d'achat, tries par prix decroissant")
pdf.body_text(
    "Le meilleur prix d'achat (Best Bid) et le meilleur prix de vente (Best Ask) "
    "definissent le haut du carnet (Top of Book) et determinent le spread."
)

pdf.section_title("2.2 Definitions cles")

pdf.subsection_title("Best Bid et Best Ask")
pdf.body_text("Best Bid : le prix le plus eleve qu'un acheteur est pret a payer :")
pdf.formula("P_bid = max{ P_i : i dans ordres d'achat }")
pdf.body_text("Best Ask : le prix le plus bas qu'un vendeur accepte :")
pdf.formula("P_ask = min{ P_i : i dans ordres de vente }")

pdf.subsection_title("Spread")
pdf.body_text("Le spread est la difference entre best ask et best bid :")
pdf.formula("S = P_ask - P_bid")
pdf.body_text(
    "Le spread est un indicateur fondamental de la liquidite. Un spread etroit "
    "signifie que le titre est tres liquide."
)

pdf.subsection_title("Mid-price")
pdf.body_text("Le prix milieu (mid-price), estimateur du 'vrai' prix :")
pdf.formula("P_mid = (P_ask + P_bid) / 2")

pdf.subsection_title("Order Book Imbalance (OBI)")
pdf.body_text("Le desequilibre du carnet mesure la pression acheteuse vs vendeuse :")
pdf.formula("OBI = (Q_bid - Q_ask) / (Q_bid + Q_ask)")
pdf.body_text("OBI dans [-1, 1]. Positif = pression acheteuse, negatif = pression vendeuse.")

pdf.section_title("2.3 Dynamique du carnet d'ordres")
pdf.body_text("Le carnet evolue a travers trois types d'evenements :")
w = [25, 35, 130]
pdf.table_header(["Action", "Code", "Description"], w)
pdf.table_row(["Add", "A", "Un nouvel ordre limite est ajoute au carnet"], w)
pdf.table_row(["Delete", "D", "Un ordre est annule ou execute (trade)"], w, True)
pdf.table_row(["Update", "U", "Un ordre existant est modifie"], w)

pdf.ln(3)
pdf.body_text("Chaque evenement est caracterise par le flux - le changement net de volume :")
pdf.formula("flux = Delta_Q = Q_apres - Q_avant")
pdf.bullet("flux > 0 : liquidite ajoutee (nouvel ordre)")
pdf.bullet("flux < 0 : liquidite retiree (annulation ou trade)")

# ============================================================
# 3. TICK-BY-TICK & LEVEL 3
# ============================================================
pdf.add_page()
pdf.chapter_title("3. Donnees tick-by-tick et Level 3")

pdf.section_title("3.1 Les niveaux de donnees de marche")
w = [25, 50, 115]
pdf.table_header(["Niveau", "Nom", "Information"], w)
pdf.table_row(["L1", "Top of Book", "Best bid, best ask, derniere transaction"], w)
pdf.table_row(["L2", "Market Depth", "Carnet agrege par niveau de prix"], w, True)
pdf.table_row(["L3", "Market-by-Order", "Chaque ordre avec identifiant unique"], w)

pdf.ln(3)
pdf.body_text(
    "Le dataset du challenge est de Level 3 (Market-by-Order) : chaque mise a jour "
    "fournit un identifiant unique (order_id) pour l'ordre specifique qui a ete "
    "ajoute, modifie ou supprime."
)

pdf.section_title("3.2 Cycle de vie d'un ordre")
pdf.body_text("Avec le Level 3, on peut reconstituer le cycle de vie complet d'un ordre :")
pdf.formula("Ordre o : A(t0) -> U(t1), U(t2), ... -> D(tn)")
pdf.body_text("On peut mesurer :")
pdf.bullet("La duree de vie des ordres : Delta_t = tn - t0")
pdf.bullet("Le taux d'annulation vs execution")
pdf.bullet("Les patterns de modification (ordres deplaces)")

pdf.section_title("3.3 Multi-venue et carnet agrege")
pdf.body_text("Les donnees proviennent d'un carnet agrege construit a partir de plusieurs venues :")
pdf.formula("Best_Bid_agrege = max_v { Best_Bid_v }")
pdf.formula("Best_Ask_agrege = min_v { Best_Ask_v }")
pdf.body_text(
    "Le NBBO (National Best Bid and Offer) est le meilleur prix disponible "
    "tous marches confondus."
)

# ============================================================
# 4. DESCRIPTION DU CHALLENGE
# ============================================================
pdf.add_page()
pdf.chapter_title("4. Description formelle du challenge")

pdf.section_title("4.1 Probleme")
pdf.body_text(
    "Soit S = {s1, s2, ..., s24} l'ensemble des 24 stocks. Pour chaque observation i, "
    "on dispose d'une sequence de 100 evenements du carnet d'ordres :"
)
pdf.formula("X_i = (x_i^(1), x_i^(2), ..., x_i^(100))  dans  R^{100 x d}")
pdf.body_text("Le but est de trouver une fonction :")
pdf.formula("f : R^{100 x d} -> {0, 1, ..., 23}")
pdf.body_text("telle que f(X_i) = y_i (le stock correspondant).")

pdf.section_title("4.2 Dimensions du dataset")
w = [95, 95]
pdf.table_header(["Parametre", "Valeur"], w)
pdf.table_row(["Nombre de stocks", "24"], w)
pdf.table_row(["Sequences / stock / jour", "20"], w, True)
pdf.table_row(["Nombre de jours", "504 (~2 ans)"], w)
pdf.table_row(["Evenements / sequence", "100"], w, True)
pdf.table_row(["Total de lignes", "24 240 000"], w)

pdf.section_title("4.3 Normalisation des prix")
pdf.body_text(
    "Pour eviter que le prix absolu ne donne directement l'identite du stock, "
    "les prix sont centres par rapport au premier best bid de la sequence :"
)
pdf.formula("P_price(k) = P_price(k) - P_bid(1)")
pdf.formula("P_bid(k)   = P_bid(k)   - P_bid(1)")
pdf.formula("P_ask(k)   = P_ask(k)   - P_bid(1)")
pdf.body_text("ou k dans {1, ..., 100} est l'indice de l'evenement dans la sequence.")

pdf.section_title("4.4 Metrique d'evaluation")
pdf.body_text("L'evaluation se fait par accuracy (precision de classification) :")
pdf.formula("Accuracy = (1/N) * sum_{i=1}^{N} 1(y_hat_i = y_i)")
pdf.body_text("ou N est le nombre d'observations de test, y_hat la prediction, y le vrai label.")

pdf.section_title("4.5 Split temporel")
pdf.body_text(
    "Le training set est tire d'une premiere periode temporelle. Le test set utilise les "
    "memes 24 stocks mais sur une periode future differente. Cela teste la capacite du "
    "modele a generaliser dans le temps."
)

# ============================================================
# 5. DESCRIPTION DES FEATURES
# ============================================================
pdf.add_page()
pdf.chapter_title("5. Description des features")

pdf.section_title("5.1 Features categorielles")
w = [30, 55, 105]
pdf.table_header(["Feature", "Valeurs", "Description"], w)
pdf.table_row(["venue", "Entiers (0,1,2,...)", "Place de marche encodee"], w)
pdf.table_row(["action", "A, D, U", "Type d'evenement"], w, True)
pdf.table_row(["side", "A (ask), B (bid)", "Cote du carnet"], w)
pdf.table_row(["trade", "True / False", "Evenement = trade ?"], w, True)

pdf.section_title("5.2 Features numeriques")
w = [30, 30, 130]
pdf.table_header(["Feature", "Type", "Description"], w)
pdf.table_row(["price", "Float", "Prix de l'ordre (centre)"], w)
pdf.table_row(["bid", "Float", "Best bid (centre)"], w, True)
pdf.table_row(["ask", "Float", "Best ask (centre)"], w)
pdf.table_row(["bid_size", "Int", "Volume au best bid agrege"], w, True)
pdf.table_row(["ask_size", "Int", "Volume au best ask agrege"], w)
pdf.table_row(["flux", "Float", "Changement de volume sur le carnet"], w, True)
pdf.table_row(["order_id", "Int", "ID de l'ordre (0 = premier de la sequence)"], w)

pdf.section_title("5.3 Features derivees possibles")
pdf.body_text("On peut construire de nombreuses features qui caracterisent un stock :")

pdf.subsection_title("Spread moyen")
pdf.formula("S_bar = (1/100) * sum_{k=1}^{100} (P_ask(k) - P_bid(k))")

pdf.subsection_title("Order Book Imbalance moyen")
pdf.formula("OBI(k) = (Q_bid(k) - Q_ask(k)) / (Q_bid(k) + Q_ask(k))")

pdf.subsection_title("Frequence des trades")
pdf.formula("f_trade = (1/100) * sum_{k=1}^{100} 1(trade(k) = True)")

pdf.subsection_title("Distribution des venues")
pdf.formula("p_v = |{k : venue(k) = v}| / 100")

pdf.subsection_title("Volatilite du mid-price")
pdf.formula("sigma_mid = std(P_mid(k) - P_mid(k-1))")

pdf.subsection_title("Taille moyenne des ordres")
pdf.formula("q_bar = mean{ |flux(k)| : action(k) = A }")

# ============================================================
# 6. MATH FORMALIZATION
# ============================================================
pdf.add_page()
pdf.chapter_title("6. Formalisation mathematique")

pdf.section_title("6.1 Classification multi-classes")
pdf.body_text("On cherche a minimiser le risque empirique :")
pdf.formula("f_hat = argmin_{f in F} (1/N) sum_{i=1}^{N} L(f(X_i), y_i)")
pdf.body_text("ou L est la cross-entropy :")
pdf.formula("L(f(X_i), y_i) = -sum_{c=0}^{23} 1(y_i = c) * log(p_c(X_i))")
pdf.body_text("avec p_c(X_i) = softmax(z(X_i))_c et z(X_i) dans R^24 les logits.")

pdf.section_title("6.2 Softmax")
pdf.body_text("La fonction softmax convertit les logits en probabilites :")
pdf.formula("p_c = exp(z_c) / sum_{j=0}^{23} exp(z_j),  c dans {0, ..., 23}")

pdf.section_title("6.3 GRU (Gated Recurrent Unit)")
pdf.body_text("Le benchmark utilise un Bi-GRU. Equations du GRU pour un pas t :")

pdf.subsection_title("Porte de mise a jour (update gate)")
pdf.formula("z_t = sigma(W_z * [h_{t-1}, x_t] + b_z)")

pdf.subsection_title("Porte de reinitialisation (reset gate)")
pdf.formula("r_t = sigma(W_r * [h_{t-1}, x_t] + b_r)")

pdf.subsection_title("Etat candidat")
pdf.formula("h_tilde_t = tanh(W_h * [r_t (o) h_{t-1}, x_t] + b_h)")

pdf.subsection_title("Etat cache final")
pdf.formula("h_t = (1 - z_t) (o) h_{t-1} + z_t (o) h_tilde_t")

pdf.body_text(
    "ou sigma est la sigmoide, (o) le produit de Hadamard, [a,b] la concatenation, "
    "W les matrices de poids, b les biais."
)

pdf.section_title("6.4 Bidirectional GRU")
pdf.body_text("Le Bi-GRU traite la sequence dans les deux sens :")
pdf.formula("h_forward  = GRU_forward(x_1, ..., x_100)    dans R^64")
pdf.formula("h_backward = GRU_backward(x_100, ..., x_1)   dans R^64")
pdf.formula("h = [h_forward ; h_backward]                  dans R^128")

pdf.section_title("6.5 SeLU (Scaled Exponential Linear Unit)")
pdf.formula("SeLU(x) = lambda * x                  si x > 0")
pdf.formula("SeLU(x) = lambda * alpha * (exp(x)-1)  si x <= 0")
pdf.body_text("avec lambda = 1.0507 et alpha = 1.6733. SeLU auto-normalise les activations.")

# ============================================================
# 7. BENCHMARK ARCHITECTURE
# ============================================================
pdf.add_page()
pdf.chapter_title("7. Architecture du benchmark")

pdf.section_title("7.1 Preprocessing")
pdf.body_text("Chaque observation est transformee en un tenseur de forme (100, 30) :")
w = [95, 95]
pdf.table_header(["Feature", "Dimension"], w)
pdf.table_row(["Embedding de venue", "8"], w)
pdf.table_row(["Embedding de action", "8"], w, True)
pdf.table_row(["Embedding de trade", "8"], w)
pdf.table_row(["bid", "1"], w, True)
pdf.table_row(["ask", "1"], w)
pdf.table_row(["price", "1"], w, True)
pdf.table_row(["log(bid_size + 1)", "1"], w)
pdf.table_row(["log(ask_size + 1)", "1"], w, True)
pdf.table_row(["log(flux)", "1"], w)
pdf.table_row(["TOTAL", "30"], w, True)

pdf.section_title("7.2 Architecture du modele")
pdf.body_text("Pipeline complet :")
pdf.formula("X dans R^{100xd} -> Embedding -> T dans R^{100x30}")
pdf.formula("T -> Bi-GRU -> h dans R^128")
pdf.formula("h -> Dense + SeLU -> R^64")
pdf.formula("R^64 -> Dense -> z dans R^24 -> Softmax -> probabilites")

pdf.section_title("7.3 Parametres d'entrainement")
w = [95, 95]
pdf.table_header(["Parametre", "Valeur"], w)
pdf.table_row(["Loss", "Cross-Entropy"], w)
pdf.table_row(["Optimiseur", "Adam (Optax)"], w, True)
pdf.table_row(["Learning rate", "3e-3"], w)
pdf.table_row(["Batch size", "1 000"], w, True)
pdf.table_row(["Nombre de batches", "10 000"], w)
pdf.table_row(["Framework", "JAX / Optax / Flax"], w, True)

# ============================================================
# 8. APPROACHES
# ============================================================
pdf.add_page()
pdf.chapter_title("8. Pistes d'approches")

pdf.section_title("8.1 Feature Engineering")
pdf.body_text("Construire des statistiques agregees sur chaque sequence de 100 evenements :")
pdf.bullet("Statistiques de spread : moyenne, ecart-type, min, max")
pdf.bullet("Order Book Imbalance : moyenne, tendance")
pdf.bullet("Profil de venue : distribution de frequence des venues")
pdf.bullet("Profil d'action : ratio A/D/U")
pdf.bullet("Taux de trade : proportion d'evenements qui sont des trades")
pdf.bullet("Statistiques de taille : distribution de bid_size, ask_size, flux")
pdf.bullet("Dynamique temporelle : autocorrelation du mid-price")

pdf.section_title("8.2 Approches classiques ML")
pdf.bullet("Random Forest / XGBoost sur les features agregees")
pdf.bullet("LightGBM avec features statistiques")
pdf.body_text("Avantage : rapide, interpretable, bon baseline.")

pdf.section_title("8.3 Approches Deep Learning")
pdf.bullet("LSTM / GRU (comme le benchmark)")
pdf.bullet("Transformer avec self-attention sur la sequence")
pdf.bullet("1D-CNN pour capturer des patterns locaux")
pdf.bullet("Temporal Convolutional Network (TCN)")

pdf.section_title("8.4 Approches hybrides")
pdf.body_text(
    "Combiner features agregees et features apprises. Attention aux embeddings de venue "
    "qui sont tres informatifs."
)

pdf.section_title("8.5 Indices pour la classification")
pdf.body_text(
    "Pourquoi peut-on identifier un stock a partir de donnees apparemment anonymes ?"
)
pdf.bullet("Le spread moyen est caracteristique de chaque stock")
pdf.bullet("La repartition entre venues depend des accords de market making")
pdf.bullet("La taille typique des ordres varie selon la liquidite")
pdf.bullet("La frequence des trades est fonction de la popularite du stock")
pdf.bullet("La volatilite intra-jour est propre a chaque titre")
pdf.bullet("Le tick-size relatif (taille min de variation / prix) est un signal fort")

# ============================================================
# 9. GLOSSARY
# ============================================================
pdf.add_page()
pdf.chapter_title("9. Glossaire")

glossary = [
    ("Ask", "Prix le plus bas auquel un vendeur est pret a vendre"),
    ("Bid", "Prix le plus eleve qu'un acheteur est pret a payer"),
    ("Book", "Registre de tous les ordres limites en attente"),
    ("Cross-Entropy", "Fonction de perte pour la classification"),
    ("Dark Pool", "Plateforme de trading ou les ordres ne sont pas visibles"),
    ("Flux", "Changement net de volume sur un niveau de prix"),
    ("GRU", "Gated Recurrent Unit, reseau recurrent"),
    ("HFT", "High-Frequency Trading, trading haute frequence"),
    ("Level 3", "Donnees Market-by-Order, ordre individuel identifiable"),
    ("Liquidite", "Facilite d'acheter/vendre sans impacter le prix"),
    ("Market Maker", "Participant fournissant de la liquidite des deux cotes"),
    ("Mid-price", "Moyenne du best bid et best ask"),
    ("NBBO", "National Best Bid and Offer (meilleur prix agrege)"),
    ("OBI", "Order Book Imbalance, desequilibre bid/ask"),
    ("Softmax", "Fonction transformant des logits en probabilites"),
    ("Spread", "Difference entre best ask et best bid"),
    ("Tick", "Plus petite variation de prix possible"),
    ("Tick-by-tick", "Donnees enregistrant chaque evenement individuel"),
    ("Venue", "Plateforme/place de marche d'execution"),
    ("Volatilite", "Mesure de la dispersion des rendements"),
]

w = [40, 150]
pdf.table_header(["Terme", "Definition"], w)
for i, (term, defn) in enumerate(glossary):
    pdf.table_row([term, defn], w, fill=(i % 2 == 1))

# ============================================================
# SAVE
# ============================================================
output_path = r"c:\Users\Yassine Mannai\Bureau\Data Challenge CFM\High_Freq_Data\docs\Challenge_CFM_ENS_2024_Documentation.pdf"
pdf.output(output_path)
print(f"PDF generated: {output_path}")
