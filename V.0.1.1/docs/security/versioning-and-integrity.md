# Protocole v0.1 — Intégrité, authenticité et archivage des versions

Ce protocole définit **le minimum robuste** pour garantir qu’une version publiée du Devblog/registre **n’a pas été modifiée** (intégrité) et qu’elle **provient bien** du processus officiel Coherenta/CBA (authenticité), tout en restant simple à appliquer.

---

## 0) Définitions

- **Bundle de release** : une archive unique (ex. `coherenta-devlog_vX.Y.Z_bundle.zip`) contenant les documents à publier.
- **Hash** : empreinte cryptographique (SHA-256) qui change dès qu’un octet change.
- **Signature** : preuve cryptographique qu’un bundle a été approuvé par une clé officielle.
- **Miroirs** : plusieurs emplacements publics où la release est publiée (anti-remplacement discret).

---

## 1) Artifacts obligatoires (minimum robuste)

Pour chaque release `vX.Y.Z`, publier **les 3 fichiers** :

1. `*_bundle.zip`  
2. `*_bundle.sha256`  (hash SHA-256 du bundle)  
3. `*_bundle.sig`  (signature du bundle)

Et maintenir **les clés publiques** dans :

- `KEYS/public/` (clés publiques de validation)
- `KEYS/revoked.json` (liste des clés révoquées + raison + date)
- `KEYS/README.md` (comment vérifier)

> Règle : **un bundle est “officiel” si et seulement si** (a) le hash correspond **et** (b) la signature est valide avec une clé publique non révoquée.

---

## 2) Publication sur plusieurs miroirs (append-only)

Publier chaque release sur **au moins 3 miroirs** indépendants :

- **Miroir A (Git)** : un dépôt “release-only” (tags immuables)
- **Miroir B (Site)** : un site statique (liste des versions + checks)
- **Miroir C (Archive)** : une archive distribuée (ex. stockage froid / IPFS / autre)

> Objectif : empêcher qu’une version “officielle” soit remplacée discrètement partout à la fois.

---

## 3) Processus de release (résumé opérationnel)

### Étape 1 — Construire le bundle
- Geler les fichiers de la version `vX.Y.Z`
- Générer `*_bundle.zip`

### Étape 2 — Calculer le hash (SHA-256)
- Calculer SHA-256 du bundle
- Écrire le résultat dans `*_bundle.sha256`

### Étape 3 — Signer le bundle
- Signer le **bundle** (pas le hash) avec la/les clés officielles
- Produire `*_bundle.sig`

### Étape 4 — Publier sur les miroirs
- Publier les 3 artifacts (zip + sha256 + sig) sur les 3 miroirs
- Ajouter une entrée dans `releases/index.json` (voir §4)

### Étape 5 — Archivage immuable
- Une fois publiée : **ne jamais modifier** la release.
- En cas d’erreur : publier une **nouvelle** version `vX.Y.(Z+1)`.

---

## 4) Registre des releases (machine-readable)

Créer/maintenir :

- `releases/index.json`

Format recommandé :

```json
{
  "project": "Coherenta Devlog",
  "releases": [
    {
      "version": "v0.3.0",
      "date_utc": "2026-02-15T00:00:00Z",
      "bundle": "coherenta-devlog_v0.3.0_bundle.zip",
      "sha256": "…",
      "signatures": [
        { "key_id": "coherenta-root-2026-01", "sig_file": "coherenta-devlog_v0.3.0_bundle.sig" }
      ],
      "mirrors": ["git", "site", "archive"]
    }
  ]
}
```

---

## 5) Vérification (côté citoyen / lecteur)

Un lecteur doit pouvoir :

1) **Vérifier le hash** : le SHA-256 du bundle téléchargé = contenu du `.sha256`  
2) **Vérifier la signature** : `.sig` valide avec une clé publique dans `KEYS/public/`  
3) **Vérifier la non-révocation** : la clé n’apparaît pas dans `KEYS/revoked.json`  
4) **Comparer miroirs** : au moins 2 miroirs concordent (idéalement 3)

> L’app citoyenne peut automatiser ces étapes et afficher :  
> ✅ “Officiel & intact” / ⚠️ “Non signé / clé révoquée / hash différent”.

---

## 6) Sécurité minimale des clés (à respecter)

- **Clé “root”** : utilisée rarement (signer/valider des clés, pas les bundles)
- **Clé “release”** : signe les bundles (rotation possible)
- Stockage recommandé : hors-ligne (ou au minimum chiffré + sauvegarde)
- En cas de suspicion : **révoquer** immédiatement + publier une note dans le devlog

---

## 7) Option fortement recommandée : Multi-signature (anti-vol de clé)

Au lieu d’1 signature, exiger **N signatures** (ex : 2 sur 3) :

- 1 signature “Comité”
- 1 signature “Archive”
- 1 signature “Gardien”

> Sans voler plusieurs clés, un attaquant ne peut pas produire une release officielle.

---

## 8) Principe Coherenta (résumé en une phrase)

**Hash = détecte la modification. Signature = prouve l’origine. Miroirs = empêchent le remplacement discret.**
