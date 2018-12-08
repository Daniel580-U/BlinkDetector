import PyPDF2
import turtle

#carrega todo o texto do pdf em uma variável
def loadPDF(nameFile: str):
    pdfFileObj = open(nameFile, 'rb') 

    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    numpages = pdfReader.numPages
    pdfText = ""

    for page in range(1,numpages,1):
        pageObj = pdfReader.getPage(page) 
        page_string = pageObj.extractText()
        pdfText = pdfText + page_string
    
    pdfFileObj.close() 
    return pdfText

#quebra a string para mostrar o text de parte em parte indo até o próximo ponto final
# retorn array com o texto e a última posicao
def get_next_part_of_text(string, start, stop):
    part = [string[start:stop], stop]
    return part

#Configuracoes de tela
turtle_writer = turtle.Turtle()
turtle_writer.screen.setup(900,500)
turtle_writer.screen.screensize(900, 200)
turtle_writer.screen.setworldcoordinates(-10,-90,450,7.5)

#PDF LOAD
text = loadPDF('aspectos.pdf')
start = 0
stop = 25
step = 25

#CONTROLADORADOS TEXTOS
while(1):
    command = int(input("1 to pass: "))
    if command == 1:
        turtle_writer.screen.clearscreen()
        result = get_next_part_of_text(text, start, stop)
        start = result[1] + 1
        stop = start + step
        arg = result[0]
        print(start)
        print(stop)
        print(result)
        turtle_writer.write(arg, move=False, align="left", font=("Arial", 20, "normal"))
        turtle_writer.hideturtle()
        
        print( "deu bom")
        command = 0
    elif command == 2:
        break
    else:
        command = 0
    print("FIM DO LIVRO")
    turtle_writer.screen.setworldcoordinates(-10,-90,450,7.5)

turtle.done()

