#!/bin/bash

# Gera Release do Sistema em um sub-diretório
# Uso: ./gera_release.sh <nome_dir>
mkdir $1
cp leiame.txt $1
cp COPIANDO $1
cp pescadores.py $1
cp pescadores_tests.py $1
cp pescadores_manual.html $1
cp pescadores_jogo.pdf $1
cp pescadores.png $1
cp pescadores.ico $1
cp mapa_parati.csv $1
cp mapa_parati_en.csv $1
cp mapa_parati_img.png $1
cp mapa_teste.csv $1
cp executar.bat $1
cp executar.sh $1
cp gera_release.sh $1
cp gera_locale.sh $1
# cp roda_testes.sh $1
# cp roda_testes.bat $1
cp program_index.html $1
cp -r locales $1/
cd $1
# Gerando documentação para desenvolvedores
pydoc -w ./
# Testes de regressão
python -m unittest -v pescadores_tests
# Limpando arquivos temporários
rm *.pyc


