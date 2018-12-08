# Detector de Piscada + Visualizador de PDF
Este Projeto tem como intuito facilitar o acesso à leitura de livros/PDFs para pessoas que sofreram algum acidente ou que estão impossibilitadas de usar as mãos para a passagem de páginas de algum livro, utilizando-se de alguma controladora/leitora de PDFs em um notebook.

Este projeto foi baseado no tutorial do Adrian Rosebrock sobre [detecçao de piscada de olhos usando OpenCV, Python e Dlib.](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/) e também no código do [mans-men](https://github.com/mans-men/eye-blink-detection-demo), que usa o artigo citado anteriormente como base.

## Ambiente de Desenvolvimento
* [Linux Mint 19 Tara](https://linuxmint.com/)
* [OpenCV 3.4](https://github.com/opencv/opencv)
* [Python 3.6.7](https://www.python.org/)
* [dlib 19.16.99](https://github.com/davisking/dlib)
* [PyPDF2 1.26.0](https://pypi.org/project/PyPDF2/#description)

## Exemplo
Após fazer a instalação de todas as dependências listadas acima, abra o terminal e digite:
```
python3 blink-detector.py
```
Os argumentos padrão abrem a câmera e detectam o piscar dos olhos no vídeo:
![demonstração](https://github.com/ItaloBruno/Detector-de-Piscadas/blob/master/demonstração.png)

**Blink = Número de piscadas de quando a pessoa pisca ambos os olhos
Right = Número de piscadas de quando a pessoa pisca apenas o olho direito
Left  = Número de piscadas de quando a pessoa pisca apenas o olho esquerdo**

```
python detect_blinks.py -h
optional arguments:
  -h, --help            show this help message and exit
  -p SHAPE_PREDICTOR, --shape-predictor SHAPE_PREDICTOR
                        path to facial landmark predictor
  -v VIDEO, --video VIDEO
                        path to input video file
  -t THRESHOLD, --threshold THRESHOLD
                        threshold to determine closed eyes
  -f FRAMES, --frames FRAMES
                        the number of consecutive frames the eye must be below
                        the threshold
```
Você pode ver mais informações sobre os argumentos, analisar um **threshold** maior significa que um olho pode ser mais facilmente considerado como fechado, vice-versa. Para um maior **frames** significa apenas se os olhos fechados durarem por mais quadros, pode ser considerado como um olho fechado. Você também pode analisar um arquivo de vídeo analisando **video** args. O **shape-predictor** args indica o caminho do modelo treinado que é fornecido na demonstraçãos