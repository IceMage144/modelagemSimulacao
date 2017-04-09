---
title:  'Relatório do EP1'
author:
- 'Juliano Garcia de Oliveira Nº USP: 9277086'
- 'João Gabriel Basi Nº USP: 9793801'
- 'Victor Chiaradia Gramuglia Araujo   Nº USP: 9793756'
- 'Guilherme Costa Vieira Nº USP: 9790930'
- 'Raphael dos Reis Gusmão Nº 9778561'
geometry: margin=3cm
date: "09 de Abril, 2017"
---
[//]: # (Gerando PDF usando pandoc (no terminal): pandoc -s -o teste.pdf relatorio.md)
[//]: # (ESTE É UM COMENTÁRIO : Versão inicial do relatório!)

### 1. Introdução

O EP1 consiste em realizar um experimento já feito em sala, do início ao fim. Isto é, observar um fenômeno, medir com um tipo de sensor, obter dados acerca do experimento, utilizar uma modelagem matemática e finalmente analisar os dados e simular o fenômeno, que é a síntese computacional.

O experimento é um estudo do movimento retilíneo uniforme (MRU) e movimento retilínio uniformemente acelerado (MRUV), observando a movimentação dos integrantes do grupo em um espaço controlado, usando sensores do celular em conjunto com a medição do tempo usando cronômetros.

Com esse experimento espera-se observar as semelhanças e diferenças (erros) entre a análise analítica do MRU e MRUV, e comparar com o que foi obtido manualmente na prática do experimento.

### 2. Método

#### Descrição do algoritmo

O programa EP1 tem como objetivo receber dados do experimento da travessia de forma genérica, ou seja, o programa deve calcular as estatísticas de quaisquer dados entrados, independentemente da quantidade de travessias realizadas. Entretanto, o programa deve admitir como padrão uma travessia de 30 metros.

Como cada pessoa pode realizar dois tipos de travessia distintos (MRU E MRUV), é interessante dar a entrada de dados separando cada pessoa com seus respectivos tempos. Além disso, temos múltiplas travessias e a medição dos tempos pode ser realizada de duas formas: normal e alternada.

Após a leitura dos dados, calcula-se a velocidade média (caso a travessia atual seja do tipo MRU) ou a aceleração média (tipo MRUV) para cada indivíduo durante sua respectiva travessia. Assim sendo, o programa simula o movimento da travessia de cada indivíduo utilizando as equações analíticas do respectivo movimento.

---usando os dados do acelerometro

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

#### Implementação do algoritmo

A notação JSON (JavaScript Object Notation), por ser fácil de ler e escrever para seres humanos, apresenta-se como um bom formato para a leitura dos dados. Além disso é uma formatação leve para as máquinas interpretarem e isso justifica sua escolha como formato de entrada para esse programa.

O programa recebe um arquivo .json com os dados do experimento realizado. O arquivo contém um vetor na qual os elementos são vetores e cada um deçes possui as seguintes informações:

* "walker": Contém o nome da pessoa que realizou o experimento.
* "movType": Contém o tipo de movimento realizado (MRU ou MRUV).
* "Times": Matriz que contém vetores com as informações de cada travessia. Esses vetores tem três variáveis: "mtype" que contém o tipo de travessia (normal ou alternada), "csv" que contém o nome do arquivo CSV, "measures" que contém os tempos observados na travessia e "tcsv" que contém o tempo inicial e final de acordo com as medições feitas na aplicativo Physics Tools Box.

O programa utiliza o paradigma de orientação à objetos pois é vantajoso tratar cada indivíduo que realizou o experimento como um objeto, visto que aplicam-se operações similares a todos eles. Dessa forma, a reusabilidade de código é favorecida com essa escolha.

A class Walker modela o indiviíduo que realizou o experimento. Recebe como argumento as variáveis "walker", "movType" e "Times" presentes no arquivo de entrada JSON. Suas funções públicas são:

 * getVelocity(): ------------------------------------------

 * plot.graph(): Plota um gráfico relevante para cada travessia:
    * No caso do movimento ser do tipo MRU, usando a equação s = v * t, v sendo a velocidade média da travessia e t o tempo total que ela levou. Uma simulação do movimento é feita e seu gráfico Espaço x Tempo é plotado e, junto com ele, os pontos coletados no experimento, o erro (a média da diferença entre os tempos simulados e obeservados) e o gráfico dos dados obtidos pelo acelerômetro.
    * No caso do movimento ser do tipo MRUV, utiliza-se as equações s = (a * t**2)/2, e v = a * t para simular o movimento e plotar o gráfico Espaço x Tempo e Velocidade x Tempo. Além disso, plota-se a aceleração média, os dados obtidos no experimento, o erro (a média da diferença entre os tempos simulados e observados) e em baixo, os dados obtidos pelo acelerômetro.

### 3. Verificação do Programa

### 4. Dados

### 5. Interpretação

### 6. Log

#### Contribuições dos Autores:$\\$
