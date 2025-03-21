# Detecção de Formas Geométricas em Bases de Pouso de Drones


## Descrição

Este projeto tem como objetivo realizar a detecção de formas geométricas (como círculos, quadrados e cruzes) em imagens, com foco na identificação de formas compostas e a detecção de quadrados pretos em diferentes contextos. O sistema é altamente configurável, permitindo ajustes em tempo real de parâmetros de segmentação de cores e detecção de bordas, além de realizar transformações morfológicas para melhorar a detecção das formas.


## Funcionalidades

O projeto oferece as seguintes funcionalidades:

1. **Detecção de Formas Geométricas**:
   - Detecta e classifica formas geométricas como círculos, quadrados, retângulos e cruzes em imagens.
   - Utiliza contornos e transformações morfológicas para identificar e distinguir as formas presentes.

2. **Segmentação de Cores**:
   - Segmenta imagens com base nas cores definidas (como Amarelo e Azul) usando limites ajustáveis para o canal HSV.
   - Permite a personalização dos limites de cor via interface gráfica para facilitar o ajuste durante o processamento.

3. **Detecção de Bordas com Algoritmo Canny**:
   - Aplica o algoritmo Canny para detecção de bordas em imagens, ajudando a destacar as formas presentes.
   - Os parâmetros de limiar de Canny podem ser ajustados em tempo real, permitindo otimizar a detecção de bordas conforme necessário.

4. **Transformações Morfológicas**:
   - Aplica operações morfológicas (fechamento) para melhorar a qualidade das bordas e facilitar a detecção de formas geométricas.

5. **Detecção de Quadrados Pretos**:
   - Detecta quadrados pretos em imagens, destacando essas áreas específicas, o que pode ser útil para identificar elementos em bases de pouso de drones, por exemplo.

6. **Interface Gráfica de Ajuste de Parâmetros**:
   - Fornece uma interface gráfica para ajustar os parâmetros de segmentação de cores e detecção de bordas em tempo real, utilizando sliders.
   - Exibe várias janelas para visualizar os resultados do processamento, incluindo a imagem original, segmentação, bordas, formas detectadas e quadrados pretos.

7. **Detecção de Formas Compostas**:
   - Detecta e destaca formas compostas, como bases formadas por várias formas geométricas próximas umas das outras.
   - Permite identificar objetos ou estruturas mais complexas dentro da imagem.


## Tecnologias Usadas

- **Python**: Linguagem principal utilizada para o desenvolvimento do sistema.
- **OpenCV**: Biblioteca de visão computacional para processamento de imagens, detecção de formas geométricas, segmentação por cores e detecção de bordas.
- **Numpy**: Utilizada para manipulação de arrays e operações matemáticas em imagens.


## Como Funciona

O projeto realiza a detecção e classificação de formas geométricas em imagens, com ênfase em quadrados pretos, formas geométricas normais (círculos, quadrados, retângulos, triângulos e cruzes) e formas compostas (bases formadas por múltiplas formas). O fluxo do código é organizado da seguinte forma:

1. **Pré-processamento da Imagem**:
   - As imagens são carregadas e redimensionadas proporcionalmente para um tamanho máximo configurável (800x600 por padrão).
   - A imagem é convertida para o espaço de cores HSV (Matiz, Saturação e Valor) para facilitar a segmentação de cores.

2. **Segmentação de Cores**:
   - A segmentação de cores é realizada com base em intervalos de cor definidos para diferentes cores (como amarelo e azul). A segmentação utiliza o método `cv2.inRange` do OpenCV para criar uma máscara que destaca as cores desejadas na imagem.

3. **Detecção de Bordas**:
   - O algoritmo de detecção de bordas Canny é utilizado para identificar as bordas nas imagens. O código aplica a técnica de Canny utilizando dois limiares de controle ajustáveis para refinar a detecção de bordas.

4. **Transformações Morfológicas**:
   - Após a detecção de bordas, o código aplica operações morfológicas (fechamento) para eliminar ruídos e melhorar a definição dos contornos.

5. **Classificação de Formas**:
   - Os contornos encontrados nas imagens são analisados e classificados com base no número de vértices e características geométricas:
     - **Triângulos**: Detectados com 3 vértices.
     - **Quadrados/Retângulos**: Detectados com 4 vértices e uma proporção de aspecto de 1 (quadrado) ou diferente de 1 (retângulo).
     - **Círculos**: Identificados com base na circularidade (perímetro vs área).
     - **Cruz**: Detectada se a forma possui quatro ângulos entre 80° e 100°.

6. **Detecção de Formas Compostas**:
   - O código verifica a proximidade entre formas para identificar estruturas compostas, como bases de formas geométricas, agrupando formas que estão próximas umas das outras.

7. **Detecção de Quadrados Pretos**:
   - Um método específico é utilizado para detectar quadrados pretos em uma imagem. O código converte a imagem para escala de cinza, aplica limiarização e encontra contornos para identificar quadrados.

8. **Interface Gráfica e Ajustes Dinâmicos**:
   - O código possui uma interface gráfica com sliders que permitem ao usuário ajustar parâmetros de segmentação de cores, bordas e transformações morfológicas em tempo real.
   - As janelas de visualização incluem:
     - **Imagem Original**: Exibe a imagem original carregada.
     - **Segmentação**: Mostra a segmentação de cores, destacando as formas.
     - **Bordas**: Exibe as bordas detectadas pela técnica de Canny.
     - **Formas Normais**: Exibe a imagem com as formas detectadas.
     - **Formas Compostas**: Exibe a imagem com formas compostas.
     - **Quadrados Pretos**: Exibe a imagem com os quadrados pretos identificados.

9. **Encerramento do Processo**:
   - O processo continua até que o usuário pressione a tecla 'q' para fechar a aplicação e as janelas de visualização.
   
O código foi projetado para processar imagens em lote, podendo ser facilmente adaptado para trabalhar com diferentes conjuntos de imagens e tipos de formas.


## Como rodar o código

### Requisitos

- Python 3.x
- OpenCV
- Numpy

### Instalação de dependências

1. Criação de Ambiente Virtual (opcional, mas recomendado):

Para garantir que as dependências do projeto não conflitem com outras versões de pacotes no seu sistema, recomendo criar um ambiente virtual. Se você ainda não tem o `virtualenv` instalado, instale com:

**pip install virtualenv**

No Windows:

**python -m venv venv**
**.\venv\Scripts\activate**

2. Após ativar o ambiente virtual, instale as dependências necessárias com o comando:

**pip install opencv-python numpy**

### Passos para Rodar

1. **Baixe ou clone o repositório do projeto para sua máquina.**
Se você não tem o Git instalado, pode baixar o repositório como um arquivo ZIP e extraí-lo.

2. **Prepare as imagens para processamento:**
- Coloque as imagens que deseja processar dentro de uma pasta no seu computador.
- O código irá acessar essa pasta para carregar as imagens.

3. **Configure o caminho da pasta de imagens:**
No código, altere a variável folder_path para o caminho da pasta onde as imagens estão localizadas.

Exemplo:
**process_images_in_folder('C:/caminho/para/sua/pasta/de/imagens')**

4. **Execute o script Python:**
-Abra o terminal ou prompt de comando.
-Navegue até o diretório onde o arquivo drone_landing_detection.py está localizado.
-Execute o script com o comando:
**drone_landing_detecti.py**

5. **Interaja com a interface gráfica:**
A interface gráfica será aberta automaticamente e permitirá que você ajuste os parâmetros de segmentação de cores e detecção de bordas utilizando sliders.

O sistema exibirá várias janelas com os resultados:
    -Imagem Original: A imagem original carregada.
    -Segmentação: A segmentação de cores, com as formas destacadas.
    -Bordas: A detecção de bordas usando o algoritmo Canny.
    -Imagem com Formas Normais: A imagem com as formas detectadas (círculos, quadrados, cruzes).
    -Imagem com Formas Compostas: A imagem mostrando formas compostas, como bases.
    -Quadrados Pretos: A imagem com os quadrados pretos identificados.

6. **Fechar a aplicação:**
Para fechar a aplicação, pressione a tecla 'q' enquanto qualquer uma das janelas estiver em foco.

Isso encerrará o processo e fechará as janelas abertas.


## Por que é util

Este sistema pode ser útil em diversas áreas, como:
    - **Robótica e Drones**: Para detecção e reconhecimento de objetos em ambientes externos.
    - **Visão Computacional**: Pode ser integrado a sistemas de visão computacional para identificar padrões geométricos.
    - **Processamento de Imagens**: Pode ser aplicado em áreas que necessitam de processamento de imagens em tempo real para detectar formas e objetos.


## Justificativas das Escolhas

A seguir, são apresentadas as justificativas das escolhas feitas para o desenvolvimento deste projeto, incluindo as tecnologias utilizadas e as abordagens adotadas para a implementação.

1. **Uso do OpenCV**
   O OpenCV (Open Source Computer Vision Library) foi escolhido devido à sua vasta gama de funcionalidades dedicadas ao processamento de imagens e visão computacional. Algumas de suas funcionalidades principais, como detecção de bordas (Canny), segmentação de cores, operações morfológicas, e contorno de formas, são fundamentais para o sucesso do projeto. Além disso, o OpenCV é amplamente documentado e utilizado, o que facilita a implementação e a resolução de problemas.

2. **Uso do Espaço de Cores HSV**
   O espaço de cores HSV foi escolhido para segmentação de cores, pois é mais robusto a variações de iluminação do que o modelo RGB. O HSV separa a informação de matiz (H), saturação (S) e valor (V), permitindo segmentar objetos baseados em suas cores de forma mais precisa, especialmente em condições de iluminação variável.

3. **Segmentação de Cores com Limiares Personalizáveis**
   A segmentação de cores foi configurada para ser ajustável em tempo real através de sliders, permitindo ao usuário adaptar os parâmetros para diferentes condições de imagem e cores de interesse. Essa flexibilidade facilita a experimentação com diferentes intervalos de cores e melhora a acuracidade da detecção de formas em diferentes 

4. **Detecção de Bordas com Canny**
   O algoritmo Canny foi adotado para a detecção de bordas devido à sua eficácia e precisão na identificação de bordas em imagens. O Canny é amplamente utilizado em sistemas de visão computacional devido à sua capacidade de detectar bordas de alta qualidade com controle de sensibilidade através dos dois limiares ajustáveis.

5. **Operações Morfológicas**
   As operações morfológicas (fechamento) foram aplicadas para melhorar a qualidade dos contornos detectados e reduzir ruídos. Essas operações são essenciais para obter uma detecção mais precisa de formas geométricas, especialmente quando se lida com imagens com ruído ou formas desconectadas.

6. **Classificação de Formas**
   A classificação de formas geométricas foi baseada no número de vértices dos contornos (triângulos, quadrados, retângulos, círculos, etc.). Para círculos, a circularidade foi calculada para garantir uma detecção precisa. As formas compostas foram identificadas pela proximidade de diferentes formas na imagem.

7. **Detecção de Quadrados Pretos**
   A detecção de quadrados pretos foi implementada usando limiarização, um método simples e eficaz para destacar a diferença entre áreas claras e escuras da imagem. Isso facilita a identificação precisa de quadrados pretos, mesmo em imagens com diferentes níveis de iluminação.

8. **Interface Gráfica e Ajustes Dinâmicos**
   A interface gráfica com sliders permite que o usuário ajuste parâmetros como limiares de cor, tamanho do kernel e limiares do Canny em tempo real. Isso torna o sistema flexível, permitindo que o usuário adapte as configurações para diferentes tipos de imagens.

9. **Processamento em Lote de Imagens**
   O código foi projetado para processar imagens em lote, permitindo ao usuário aplicar a detecção em um diretório inteiro de imagens de forma eficiente. Isso é útil em situações onde se tem várias imagens a serem processadas sem a necessidade de intervenção manual para cada uma.

Essas escolhas foram feitas com base nas melhores práticas do campo de visão computacional, levando em consideração a precisão, flexibilidade e eficiência do sistema. As fontes de informações incluem documentação oficial, artigos acadêmicos e exemplos práticos encontrados em tutoriais e repositórios de código.


## Resultados esperados

- **Precisão na Detecção de Formas**: As formas geométricas, como círculos, quadrados e cruzes, devem ser detectadas com alta precisão, mesmo com variações de tamanho e posição.
- **Interface Interativa**: O usuário será capaz de ajustar parâmetros de segmentação e bordas em tempo real, melhorando a precisão da detecção conforme necessário.
- **Identificação de Quadrados Pretos**: Quadrados pretos serão identificados de forma confiável, com contornos visíveis.