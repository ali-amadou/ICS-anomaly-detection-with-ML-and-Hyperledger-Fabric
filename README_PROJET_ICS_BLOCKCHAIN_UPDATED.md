# AI-Based ICS Network Anomaly Detection with Machine Learning and Hyperledger Fabric

## 1. Présentation du projet

Ce projet met en œuvre un système de détection d'anomalies et d'attaques
dans des flux réseau associés à un environnement **Industrial Control
Systems (ICS)**.

L'architecture combine :

-   un modèle de Machine Learning pour la détection binaire ;
-   un second modèle pour l'identification du type d'attaque ;
-   un mécanisme de génération d'alertes ;
-   **Hyperledger Fabric** pour l'enregistrement des alertes ;
-   un récepteur réseau temps réel ;
-   une supervision via Streamlit ;
-   une simulation de trafic réalisée depuis un second PC à partir des
    données du dataset.

L'objectif est de disposer d'une chaîne complète :

``` text
PC2 / Dataset replay
        │
        │  flux réseau envoyés un par un
        ▼
PC1 - Récepteur temps réel
        │
        ▼
Prétraitement / Encodage
        │
        ▼
Random Forest binaire
        │
   ┌────┴─────┐
   ▼          ▼
Normal      Attack
              │
              ▼
       AttackClassifier
              │
              ▼
       Type d'attaque
              │
              ▼
       Génération alerte
              │
              ▼
      Hyperledger Fabric
              │
              ▼
      Supervision Streamlit
```

> **Important :** dans la démonstration actuelle, le PC2 joue le rôle de
> générateur/replay de flux à partir du dataset. Il ne s'agit pas d'une
> simulation complète d'un PLC réel ni d'une interception MITM réelle.

------------------------------------------------------------------------

## 2. Architecture actuelle

### PC1 --- Machine principale

Le PC1 assure les fonctions principales du système :

-   réception des flux ;
-   prétraitement ;
-   détection binaire ;
-   classification multiclasses des attaques ;
-   calcul de la sévérité ;
-   génération des alertes ;
-   enregistrement des alertes dans Hyperledger Fabric ;
-   supervision du système.

Le récepteur écoute actuellement sur :

``` text
0.0.0.0:5000
```

### PC2 --- Générateur de trafic

Le PC2 envoie les lignes du dataset progressivement afin de reproduire
un scénario de trafic réseau temps réel.

Le principe est :

``` text
Ligne du dataset
      ↓
Conversion en flux
      ↓
Envoi réseau vers PC1
      ↓
Analyse par le système IDS
```

Cette approche permet de tester le comportement temps réel sans avoir
besoin de déployer immédiatement de vrais équipements industriels.

------------------------------------------------------------------------

# 3. Composant Machine Learning

## 3.1 Détection binaire

Le premier niveau utilise un modèle :

``` text
RandomForest_Selected_v1
```

Il distingue deux catégories :

-   `Normal`
-   `Attack`

Le modèle utilise les caractéristiques préparées dans :

``` text
models/selected_features.pkl
```

Le modèle entraîné est stocké dans :

``` text
models/random_forest_selected.pkl
```

Le prétraitement utilise notamment les encodeurs sauvegardés dans :

``` text
preprocessing/encoders.pkl
```

Le flux reçu est transformé avant d'être présenté au modèle afin de
conserver le même format que celui utilisé pendant l'entraînement.

------------------------------------------------------------------------

## 3.2 Classification du type d'attaque

Lorsqu'un flux est identifié comme `Attack`, un deuxième modèle est
appelé.

Composant :

``` text
classifier/attack_classifier.py
```

Modèles associés :

``` text
models/attack_classifier.pkl
models/attack_label_encoder.pkl
models/attack_features.pkl
```

Le classificateur actuel reconnaît cinq catégories :

``` text
BAD-MISCONF
BAD-MISCONF-DUPLICATION
BAD-MITM
BAD-PORTSCAN
BAD-SSH
```

Les catégories `BAD-PORTSCAN1` et `BAD-PORTSCAN2` ont été regroupées
sous :

``` text
BAD-PORTSCAN
```

Le classificateur retourne notamment :

-   le type d'attaque ;
-   la confiance associée à cette classification.

------------------------------------------------------------------------

# 4. Chaîne de détection

Le composant principal de détection binaire se trouve dans :

``` text
classifier/binary_detector.py
```

La logique générale est :

1.  réception d'un flux ;
2.  conservation des informations originales ;
3.  encodage des variables catégorielles ;
4.  sélection des features attendues par le Random Forest ;
5.  calcul des probabilités `Attack` / `Normal` ;
6.  décision binaire ;
7.  calcul de la sévérité ;
8.  si le flux est malveillant, appel du classificateur multiclasses ;
9.  création d'une alerte ;
10. enregistrement de l'alerte dans la blockchain.

Les niveaux de sévérité utilisés sont :

``` text
Critical
High
Medium
Low
None
```

La sévérité est calculée à partir de la probabilité d'attaque.

------------------------------------------------------------------------

# 5. Prétraitement

Le prétraitement est réalisé par :

``` text
preprocessing/flow_preprocessor.py
```

Les principales variables catégorielles traitées sont :

``` text
sAddress
rAddress
sIPs
rIPs
protocol
```

Les mappings d'encodage/décodage sont conservés dans :

``` text
preprocessing/encoders.pkl
```

Le préprocesseur doit recevoir un flux contenant les caractéristiques
nécessaires au modèle.

Une erreur de colonnes manquantes est générée si le flux reçu ne possède
pas les features attendues.

------------------------------------------------------------------------

# 6. Réception temps réel

Le projet dispose maintenant d'un récepteur permettant de recevoir les
flux depuis un autre PC.

Le service écoute sur :

``` text
0.0.0.0:5000
```

Exemple de fonctionnement :

``` text
PC2
 │
 │ TCP / flux JSON
 ▼
PC1:5000
 │
 ▼
FlowPreprocessor
 │
 ▼
BinaryDetector
 │
 ├── Normal
 │
 └── Attack
       │
       ▼
 AttackClassifier
       │
       ▼
 Alert
       │
       ▼
 Hyperledger Fabric
```

Un test de fonctionnement a permis de recevoir plusieurs flux depuis le
PC2. Des flux ont notamment été classifiés comme :

``` text
Prediction: Normal
```

et d'autres comme :

``` text
Prediction: Attack
Attack Type: BAD-MISCONF
Severity: Medium
```

Des alertes ont effectivement été enregistrées dans Fabric pendant ce
scénario de test.

------------------------------------------------------------------------

# 7. Exemple de résultat temps réel

Un exemple observé pendant les essais :

``` text
Flow received

Prediction: Attack
Confidence: 0.6017
Severity: Medium

ATTACK DETECTED

Attack Type: BAD-MISCONF

Blockchain alert ID:
bf360817-b280-4db0-a197-fea4f46a7bc2
```

Un autre flux malveillant a également généré une alerte blockchain avec
un identifiant différent.

> Les valeurs de `Label réel` ne doivent pas être déduites de la sortie
> du récepteur. Elles doivent être récupérées à partir de la ligne
> exacte du dataset envoyée par le PC2.

------------------------------------------------------------------------

# 8. Structure des alertes

Une alerte contient notamment :

-   identifiant de l'alerte ;
-   timestamp ;
-   adresse IP source ;
-   adresse IP destination ;
-   protocole ;
-   prédiction ;
-   confiance ;
-   sévérité ;
-   modèle utilisé ;
-   type d'attaque ;
-   probabilité d'attaque ;
-   probabilité normale.

Exemple conceptuel :

``` json
{
  "alertId": "...",
  "prediction": "Attack",
  "attack_type": "BAD-MISCONF",
  "severity": "Medium",
  "confidence": 0.6017,
  "model": "RandomForest_Selected_v1"
}
```

Les valeurs de cet exemple servent à illustrer la structure ; les
résultats expérimentaux doivent être repris depuis les sorties
réellement obtenues.

------------------------------------------------------------------------

# 9. Blockchain --- Hyperledger Fabric

La couche blockchain utilise :

-   Hyperledger Fabric ;
-   Node.js ;
-   Fabric Contract API ;
-   un smart contract/chaincode dédié aux alertes.

La blockchain permet de conserver une trace des événements de sécurité.

Les objectifs sont :

-   intégrité des alertes ;
-   traçabilité ;
-   conservation des événements ;
-   vérification de l'historique ;
-   partage contrôlé des informations de sécurité.

Une alerte détectée par le système peut donc suivre le chemin :

``` text
Détection IA
    ↓
Création Alert
    ↓
Client blockchain
    ↓
Smart Contract
    ↓
Hyperledger Fabric Ledger
```

Le réseau Fabric existant est utilisé pour les démonstrations ; la
procédure de démonstration ne nécessite pas de recréer systématiquement
le réseau.

------------------------------------------------------------------------

# 10. Supervision Streamlit

Le projet comprend également une interface de supervision basée sur
**Streamlit**.

Son rôle est de fournir une vue exploitable des événements détectés,
notamment :

-   flux analysés ;
-   prédictions ;
-   attaques détectées ;
-   type d'attaque ;
-   niveau de sévérité ;
-   informations d'alerte ;
-   informations issues de la blockchain.

La supervision constitue la couche de visualisation du système.

> L'interface de supervision est à considérer comme une couche distincte
> du moteur de détection : le pipeline IA et blockchain doit rester
> fonctionnel indépendamment de l'affichage.

------------------------------------------------------------------------

# 11. Données et modèles

## Données brutes

Le dataset réseau principal se trouve dans :

``` text
data/output_bottom.csv
```

Il contient les informations de flux ainsi que plusieurs labels utilisés
pour l'analyse et l'entraînement.

Les labels bruts comprennent notamment :

``` text
IT_B_Label
IT_M_Label
NST_B_Label
NST_M_Label
```

## Dataset prétraité

Les données sélectionnées sont conservées dans :

``` text
processed/dataset_selected.csv
```

Le dataset utilisé pour le classificateur multiclasses est :

``` text
processed/attack_dataset.csv
```

Il est construit à partir des flux d'attaque et utilise `NST_M_Label`
comme information de type d'attaque.

------------------------------------------------------------------------

# 12. Entraînement multiclasses

La préparation du dataset multiclasses est réalisée avec :

``` text
training_multiclass/prepare_multiclass.py
```

Le principe est :

``` text
dataset_selected.csv
       │
       ▼
Conserver Label == 0
       │
       ▼
Flux d'attaque
       │
       ▼
Récupération de NST_M_Label
       │
       ▼
Regroupement des PORTSCAN
       │
       ▼
Suppression de GOOD-SSH
       │
       ▼
attack_dataset.csv
```

L'entraînement du classificateur est réalisé par :

``` text
training_multiclass/train_attack_classifier.py
```

Le modèle utilise un Random Forest avec :

``` text
n_estimators = 300
class_weight = balanced
random_state = 42
```

------------------------------------------------------------------------

# 13. Évaluation du classificateur multiclasses

L'évaluation correcte utilise une séparation entraînement/test de 80/20
avec :

``` text
random_state = 42
stratify = y
```

Résultat obtenu sur le jeu de test :

``` text
Accuracy : 66.35 %
```

  Type d'attaque              Precision   Recall   F1-score
  ------------------------- ----------- -------- ----------
  BAD-MISCONF                    0.5103   0.5273     0.5187
  BAD-MISCONF-DUPLICATION        0.5789   0.5601     0.5694
  BAD-MITM                       0.9612   0.9802     0.9706
  BAD-PORTSCAN                   0.9659   1.0000     0.9827
  BAD-SSH                        1.0000   0.9800     0.9899

Moyennes :

``` text
Macro precision : 80.33 %
Macro recall    : 80.95 %
Macro F1        : 80.62 %
```

### Interprétation

Le modèle reconnaît très bien :

-   `BAD-MITM` ;
-   `BAD-PORTSCAN` ;
-   `BAD-SSH`.

La principale difficulté concerne :

``` text
BAD-MISCONF
BAD-MISCONF-DUPLICATION
```

Ces deux classes sont fréquemment confondues entre elles.

------------------------------------------------------------------------

# 14. Évaluation du modèle binaire

Le modèle binaire doit être évalué sur un véritable jeu de test séparé
de l'entraînement.

Le script d'entraînement utilise une séparation :

``` text
80 % entraînement
20 % test
```

avec :

``` text
random_state = 42
stratify = y
```

Le jeu de test est sauvegardé dans :

``` text
models/selected_test_set.pkl
```

> Il faut distinguer les résultats obtenus sur le jeu de test des
> résultats obtenus en réévaluant le modèle sur l'ensemble du dataset.
> Ces derniers ne doivent pas être présentés comme une performance de
> généralisation.

La matrice de confusion finale à mettre dans le rapport doit donc être
celle produite sur le jeu de test retenu pour l'évaluation.

------------------------------------------------------------------------

# 15. Tests de robustesse et de sécurité

Plusieurs scénarios de test sont prévus :

  -----------------------------------------------------------------------
  Test                    Objectif                Résultat
  ----------------------- ----------------------- -----------------------
  JSON incomplet          Vérifier la robustesse  À documenter selon le
                          du receiver             test exécuté

  Type de donnée          Tester la validation    À documenter selon le
  incorrect               des données             test exécuté

  Flux invalide           Vérifier la gestion des À documenter selon le
                          erreurs                 test exécuté

  Connexion inconnue      Tester l'accessibilité  TCP 5000 inaccessible
                          réseau du receiver      lors du test
  -----------------------------------------------------------------------

Lors d'un test depuis le PC2 vers le PC1 :

``` text
Test-NetConnection 192.168.11.107 -Port 5000
```

le ping a réussi mais :

``` text
TcpTestSucceeded: False
```

Cela signifie que l'hôte était joignable mais que la connexion TCP vers
le port 5000 n'était pas accessible dans les conditions de ce test.

> Ce résultat ne permet pas, à lui seul, de conclure que le receiver a
> explicitement rejeté la connexion : le pare-feu, l'écoute du service
> ou la configuration réseau peuvent également être en cause.

------------------------------------------------------------------------

# 16. Organisation du projet

La structure générale du projet comprend notamment :

``` text
.
├── alerts/
│   └── Structure et gestion des alertes
│
├── analysis/
│   └── Analyse des données
│
├── blockchain/
│   ├── api/
│   │   └── API blockchain
│   ├── chaincode/
│   │   └── Smart contract Hyperledger Fabric
│   └── client/
│       └── Client blockchain
│
├── classifier/
│   ├── binary_detector.py
│   └── attack_classifier.py
│
├── data/
│   └── Dataset réseau
│
├── models/
│   ├── random_forest_selected.pkl
│   ├── selected_features.pkl
│   ├── selected_test_set.pkl
│   ├── attack_classifier.pkl
│   ├── attack_features.pkl
│   └── attack_label_encoder.pkl
│
├── preprocessing/
│   ├── flow_preprocessor.py
│   └── encoders.pkl
│
├── processed/
│   ├── dataset_selected.csv
│   └── attack_dataset.csv
│
├── training/
│   └── Scripts d'entraînement du modèle binaire
│
├── training_multiclass/
│   ├── prepare_multiclass.py
│   ├── train_attack_classifier.py
│   └── evaluate_attack_classifier.py
│
├── realtime/
│   └── Réception des flux réseau temps réel
│
├── tests/
│   └── Tests du système
│
├── demo/
│   └── Scripts/outils liés à la démonstration
│
└── main.py
```

> Cette liste est une vue fonctionnelle. Pour une correspondance exacte
> avec la version déposée, il faut vérifier l'arborescence réellement
> présente dans le dépôt.

------------------------------------------------------------------------

# 17. Fichiers particulièrement importants

Pour comprendre rapidement le fonctionnement du projet, les fichiers
suivants sont prioritaires :

  -----------------------------------------------------------------------------------------
  Fichier                                               Rôle
  ----------------------------------------------------- -----------------------------------
  `classifier/binary_detector.py`                       Détection binaire et orchestration
                                                        de la classification

  `classifier/attack_classifier.py`                     Identification du type d'attaque

  `preprocessing/flow_preprocessor.py`                  Encodage des flux

  `training_multiclass/prepare_multiclass.py`           Préparation du dataset multiclasses

  `training_multiclass/train_attack_classifier.py`      Entraînement du classificateur
                                                        d'attaque

  `training_multiclass/evaluate_attack_classifier.py`   Évaluation multiclasses

  `models/random_forest_selected.pkl`                   Modèle binaire entraîné

  `models/selected_features.pkl`                        Features utilisées par le modèle
                                                        binaire

  `models/attack_classifier.pkl`                        Modèle multiclasses

  `models/attack_features.pkl`                          Features du classificateur
                                                        multiclasses

  `models/attack_label_encoder.pkl`                     Encodage des classes d'attaque

  `models/encoders.pkl` / `preprocessing/encoders.pkl`  Encodage des variables
                                                        catégorielles

  `realtime/receiver.py`                                Réception des flux temps réel, si
                                                        présent dans la version déposée

  `blockchain/`                                         Intégration Hyperledger Fabric

  `main.py`                                             Point d'entrée général, selon le
                                                        scénario d'exécution
  -----------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 18. Technologies utilisées

  Domaine                     Technologies
  --------------------------- -------------------------------------
  Machine Learning            Python, Scikit-learn, Random Forest
  Manipulation des données    Pandas
  Sérialisation des modèles   Joblib
  Prétraitement               Encodage de variables catégorielles
  Communication temps réel    TCP / JSON
  Blockchain                  Hyperledger Fabric
  Smart Contract              Node.js / Chaincode
  API blockchain              Fabric Contract API
  Supervision                 Streamlit
  Système                     Windows / Ubuntu / WSL
  Conteneurisation            Docker

------------------------------------------------------------------------

# 19. Scénario de démonstration recommandé

Le scénario de démonstration est volontairement simple et reproductible.

### Étape 1 --- Préparer le PC1

Le PC1 doit disposer de :

-   l'environnement Python ;
-   les modèles ;
-   le préprocesseur ;
-   le réseau Hyperledger Fabric ;
-   le receiver ;
-   les composants de supervision.

### Étape 2 --- Démarrer Hyperledger Fabric

Le réseau Fabric existant est démarré selon la configuration du projet.

Il n'est pas nécessaire de recréer le réseau à chaque démonstration.

### Étape 3 --- Démarrer le receiver

Le PC1 écoute sur :

``` text
0.0.0.0:5000
```

### Étape 4 --- Démarrer la supervision

L'interface Streamlit est lancée pour suivre les événements.

### Étape 5 --- Lancer le replay depuis PC2

Le PC2 lit les flux du dataset et les envoie progressivement au PC1.

### Étape 6 --- Observer la chaîne complète

Pour chaque flux :

``` text
Flux
 ↓
Prétraitement
 ↓
Random Forest
 ↓
Normal / Attack
 ↓
Type d'attaque si nécessaire
 ↓
Alerte
 ↓
Fabric
 ↓
Dashboard
```

------------------------------------------------------------------------

# 20. Vérification d'une alerte blockchain

Lorsqu'une attaque est détectée, le système retourne un identifiant
blockchain.

Exemple :

``` text
Blockchain alert ID:
bf360817-b280-4db0-a197-fea4f46a7bc2
```

Cet identifiant permet de retrouver l'événement enregistré dans le
ledger selon les fonctions exposées par le smart contract.

------------------------------------------------------------------------

# 21. Limites actuelles

Le système constitue une démonstration fonctionnelle, mais certaines
limites doivent être clairement mentionnées.

### 21.1 Replay de dataset

Le trafic temps réel est actuellement simulé par l'envoi de lignes du
dataset.

Il ne s'agit donc pas encore d'une capture directe de trafic provenant
de PLC ou d'équipements industriels réels.

### 21.2 Dépendance aux données d'entraînement

Le modèle ML reconnaît principalement les comportements représentés dans
les données utilisées pour son entraînement.

Il ne faut pas présenter le système comme capable de détecter
automatiquement toutes les attaques possibles.

### 21.3 Classification multiclasses

Les performances sont élevées pour MITM, PORTSCAN et SSH, mais plus
faibles pour les deux catégories de mauvaise configuration :

``` text
BAD-MISCONF
BAD-MISCONF-DUPLICATION
```

### 21.4 Communication réseau

La communication PC2 → PC1 dépend de la configuration réseau et du
pare-feu Windows.

### 21.5 Sécurité de production

La configuration actuelle est destinée à une démonstration/prototype. Un
déploiement industriel réel nécessiterait notamment :

-   authentification forte des sources ;
-   chiffrement des communications ;
-   gestion des certificats ;
-   contrôle d'accès ;
-   journalisation renforcée ;
-   haute disponibilité ;
-   durcissement des composants ;
-   supervision et réponse à incident.

------------------------------------------------------------------------

# 22. Résumé pour l'encadrant

Le projet peut être compris comme un pipeline de sécurité en plusieurs
niveaux :

``` text
1. Génération/replay des flux
             ↓
2. Réception réseau
             ↓
3. Prétraitement
             ↓
4. Détection binaire par Random Forest
             ↓
5. Classification du type d'attaque
             ↓
6. Génération d'une alerte structurée
             ↓
7. Enregistrement dans Hyperledger Fabric
             ↓
8. Supervision via Streamlit
```

L'intérêt principal du projet est la combinaison de deux mécanismes
complémentaires :

**Machine Learning** → détecter et caractériser les comportements réseau
suspects.

**Blockchain** → conserver une trace intègre et traçable des alertes de
sécurité.

La démonstration actuelle relie ces composants avec un scénario PC2 →
PC1 reproductible à partir du dataset.

------------------------------------------------------------------------

# 23. Ordre de lecture conseillé

Pour comprendre rapidement le projet, il est recommandé de suivre cet
ordre :

1.  `README.md`
2.  `realtime/receiver.py`
3.  `classifier/binary_detector.py`
4.  `preprocessing/flow_preprocessor.py`
5.  `classifier/attack_classifier.py`
6.  `models/`
7.  `training/`
8.  `training_multiclass/`
9.  `blockchain/`
10. `tests/`
11. `demo/`
12. `main.py`

Cet ordre suit approximativement le chemin d'un flux depuis sa réception
jusqu'à son enregistrement blockchain.

------------------------------------------------------------------------

# 24. Conclusion

Le projet a évolué d'un simple prototype de détection vers une chaîne
intégrée combinant :

-   détection binaire ;
-   classification multiclasses ;
-   réception temps réel ;
-   génération automatique d'alertes ;
-   persistance blockchain ;
-   supervision.

La prochaine étape logique est surtout la consolidation : documenter
précisément les scripts de lancement, stabiliser les tests de
robustesse, associer les flux temps réel à leurs labels réels pour
produire un tableau expérimental fiable, et maintenir une distinction
claire entre les résultats sur jeu de test et les résultats obtenus sur
l'ensemble des données.
