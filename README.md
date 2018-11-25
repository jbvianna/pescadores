# pescadores
Game simulating the daily life of fishermen

This project was created as an attempt to help students understand concepts of financial planning and risk undertaking.
By playing as fishermen, they have to decide how to allocate their money to buy equipments needed for work 
at the same time they guarantee their daily needs. By balancing the skills they learn with the risks
of the many possible journeys, they can improve their earnings, and save money to pay for lost boats or nets.

On 2018-11-17:
Completar documentação dos métodos em pescadores.py, atualizar mensagens de internacionalização.

Além das mudanças descritas, foram realizadas pequenas alterações no programa.
O script gera_locale.sh foi criado para atualizar os arquivos de i18n, e
gera_release.sh foi simplificado. 

Date:   Mon Nov 19 10:56:34 2018 -0200
Author: Joao Vianna <jvianna@gmail.com>

    Testes das classes Pesca, Perigo, Posicao, Barco e Pescador.
    
    Suíte de testes para o módulo pescadores (incompleta).
    Os testes revelaram que os valores para resistência dos barcos estavam muito elevados.
    Isto foi corrigido no programa e nos manuais.

Date:   Tue Nov 20 11:20:34 2018 -0200
Author: Joao Vianna <jvianna@gmail.com>

Leitura do mapa em arquivo.

O método de criação do mapa na classe Mapa foi alterado, para
ler os cados em um arquivo .csv.
O arquivo com a imagem do mapa foi renomeado, para refletir a
relação com o mapa de parati.
Foram criados arquivos de mapa para Português e Inglês, com
os mesmos dados que se encontravam no programa.
A classe Perigo recebeu um novo método, para retornar a
descrição do perigo deixando o código mais flexível.

new file:   mapa_parati.csv
new file:   mapa_parati_en.csv
new file:   mapa_parati_img.png
modified:   gera_release.sh
modified:   locales/en/LC_MESSAGES/pescadores.mo
modified:   locales/en/LC_MESSAGES/pescadores.po
modified:   locales/pescadores.pot
modified:   locales/pt/LC_MESSAGES/pescadores.mo
modified:   locales/pt/LC_MESSAGES/pescadores.po
deleted:    mapa_pesca.png
modified:   pescadores.py

Date:   Tue Nov 25 11:20:34 2018 -0200
Author: Joao Vianna <jvianna@gmail.com>

Versão 0.95

O diálogo de transferências foi ampliado para permitir operações
de compra e venda de barcos e redes, além de transferências
de dinheiro.

Foi criado um jogador especial: Mestre, que recebe mais dinheiro
no início do jogo, mas não embarca nunca. O Mestre pode realizar
transações com os pescadores, podendo ser utilizado como um
comerciante, ou para aplicar bônus e penalidades.
