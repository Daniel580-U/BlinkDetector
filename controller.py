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


def getProximoTexto(string,start,stop):
   #aceita o PR que eu perdoo
   part
   for i in range(start,len(string)):
       if string[i] != stop:
           part += string[i]

   return part


#Configuracoes de tela
turtle_writer = turtle.Turtle()
turtle_writer.screen.setup(800,400)
turtle_writer.screen.screensize(800, 100)
turtle_writer.screen.setworldcoordinates(-10,-90,450,7.5)

#PDF LOAD
text = loadPDF('') # Aqui você deve inserir o nome do pdf que deseja visualizar
start = 0
stop = 25
step = 25

def print_results(list):
    for item in list:
        print(item)

#CONTROLADORADOS TEXTOS
while(1):
    command = int(input("2 to pass: "))
    if command == 2:
        turtle_writer.screen.clearscreen()
        result = get_next_part_of_text(text, start, stop)
        start = result[1] + 1
        stop = start + step
        arg = result[0]
        print_results([start, stop, arg])
        turtle_writer.write(arg, move=False, align="left", font=("Arial", 18, "normal"))
        turtle_writer.hideturtle()
        
        print( "give good")
        command = 0
    elif command == 2:
        break
    else:
        command = 0
    print("end of the book")
    turtle_writer.screen.setworldcoordinates(-10,-90,450,7.5)

turtle.done()

