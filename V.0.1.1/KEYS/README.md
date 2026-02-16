# KEYS — Clés publiques Coherenta

Ce dossier contient les **clés publiques** permettant de vérifier les signatures des releases.

- `public/` : clés publiques valides
- `revoked.json` : clés révoquées (ne plus faire confiance)

Règle : une release est officielle si la signature est valide avec une clé **non révoquée**.
