---
title:  'Relatório do EP1'
author:
- 'Juliano Garcia de Oliveira Nº USP: 9277086'
- 'João Gabriel Basi Nº USP: 9793801'
- 'Victor Chiaradia Gramuglia Araujo   Nº USP: 9793756'
- 'Guilherme Costa Vieira Nº USP: 9790930'
geometry: margin=3cm
date: "09 de Abril, 2017"
---
[//]: # (Gerando PDF usando pandoc (no terminal): pandoc -s -o teste.pdf relatorio.md)
[//]: # (ESTE É UM COMENTÁRIO : Versão inicial do relatório!)

###1. Introdução

O EP1 consiste em realizar um experimento já feito em sala, do início ao fim. Isto é, observar um fenômeno, medir com um tipo de sensor, obter dados acerca do experimento, utilizar uma modelagem matemática e finalmente analisar os dados e simular o fenômeno, que é a síntese computacional.

O experimento é um estudo do movimento retilíneo uniforme (MRU) e movimento retilínio uniformemente acelerado (MRUV), observando a movimentação dos integrantes do grupo em um espaço controlado, usando sensores do celular em conjunto com a medição do tempo usando cronômetros.

Com esse experimento espera-se observar as semelhanças e diferenças (erros) entre a análise analítica do MRU e MRUV, e comparar com o que foi obtido manualmente na prática do experimento.

###2. Método

####Descrição do algoritmo

O programa EP1 tem como objetivo receber dados do experimento da travessia de forma genérica, ou seja, o programa deve calcular as estatísticas de quaisquer dados entrados, independentemente da quantidade de travessias realizadas. Entretanto, o programa deve admitir como padrão uma travessia de 30 metros.

Como cada pessoa pode realizar dois tipos de travessia distintos (MRU E MRUV), é interessante dar a entrada de dados separando cada pessoa com seus respectivos tempos. Além disso, temos múltiplas travessias e a medição dos tempos pode ser realizada de duas formas: normal e alternada.

Após a leitura dos dados, calcula-se a velocidade média (caso a travessia atual seja do tipo MRU) ou a aceleração média (tipo MRUV) para cada indivíduo durante sua respectiva travessia. Assim sendo, o programa simula o movimento da travessia de cada indivíduo utilizando as equações analíticas do respectivo movimento.

Então, plota-se:

  Se MRU:
  * A velocidade média.
  * Gráfico da função que descreve a simulação do movimento (Espaço x Tempo) e os dados obtidos pelos observadores durante o experimento real.
  * Gráfico dos dados obtidos pelo acelerômetro.
  * Erro entre a simulação e o experimento real.

  Se MRUV:
  * A aceleração média.
  * Gráfico da função que descreve a simulação do movimento (Espaço x Tempo) e os dados obtidos pelos observadores.
  * Gráfico da função que descreve a simulação (Velocidade x Tempo).
  * Gráfico dos dados obtidos pelo acelerômetro.
  * Erro entre a simulação e o experimento real.

####Implementação do algoritmo

###3. Verificação do Programa

###4. Dados

###5. Interpretação

###6. Log

#### Contribuições dos Autores:$\\$
