#!/bin/bash

# Nome da branch atual
CURRENT_BRANCH=$(git branch --show-current)

# Mensagem do commit (você pode personalizar ou passar como argumento)
COMMIT_MESSAGE="Automatic commit and merge"

# Verifica se há alterações para commitar
if [[ -n $(git status -s) ]]; then
    echo "Fazendo commit das alterações..."
    git add .
    git commit -m "$COMMIT_MESSAGE"
    git push origin "$CURRENT_BRANCH"
else
    echo "Nenhuma alteração para commitar."
fi

# Faz o merge na branch main
echo "Mudando para a branch main..."
git checkout main

echo "Atualizando a branch main..."
git pull origin main

echo "Fazendo merge da branch $CURRENT_BRANCH na main..."
git merge "$CURRENT_BRANCH"

echo "Enviando alterações para o repositório remoto..."
git push origin main

echo "Voltando para a branch $CURRENT_BRANCH..."
git checkout "$CURRENT_BRANCH"

echo "Processo concluído!"