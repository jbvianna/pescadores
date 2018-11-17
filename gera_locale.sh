#!/bin/bash

# Arquivos para internacionalização
# Uso: ./gera_locale.sh
mkdir -p locales
rm locales/pescadores.pot
pygettext -d pescadores -o locales/pescadores.pot pescadores.py
mkdir -p locales/en/LC_MESSAGES
mkdir -p locales/pt/LC_MESSAGES
# Da primeira vez, copiar
# cp locales/pescadores.pot locales/en/LC_MESSAGES/pescadores.po
# cp locales/pescadores.pot locales/pt/LC_MESSAGES/pescadores.po
# Editar os arquivos *.po para incluir traduções
# Nas vezes seguintes, usar msgmerge
msgmerge -U locales/en/LC_MESSAGES/pescadores.po locales/pescadores.pot
rm locales/en/LC_MESSAGES/pescadores.po~
msgfmt locales/en/LC_MESSAGES/pescadores.po -o locales/en/LC_MESSAGES/pescadores.mo
msgmerge -U locales/pt/LC_MESSAGES/pescadores.po locales/pescadores.pot
rm locales/pt/LC_MESSAGES/pescadores.po~
msgfmt locales/pt/LC_MESSAGES/pescadores.po -o locales/pt/LC_MESSAGES/pescadores.mo
