# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import PyPDF2
import turtle
import argparse
import imutils
import time
import dlib
import cv2
from PyPDF2 import PdfReader
import time

def analyze_blink_state(blink_count: int, total_time: float, eye_closed_time: float) -> str:
    """
    Analiza el estado de la persona basándose en los parpadeos y el tiempo de ojos cerrados.
    
    :param blink_count: Número de parpadeos detectados en el período de observación.
    :param total_time: Tiempo total de observación (en segundos).
    :param eye_closed_time: Tiempo acumulado de los ojos cerrados durante el período (en segundos).
    :return: Una cadena que indica el estado de la persona (por ejemplo, "Cansado", "Somnoliento", "Atento").
    """
    # Frecuencia de parpadeo (blinks por minuto)
    blink_frequency = (blink_count / total_time) * 60
    # Definir estados basados en frecuencia de parpadeo y tiempo con ojos cerrados
    if blink_frequency < 10 and eye_closed_time > 0.15 * total_time:
        return "Muy cansado o somnoliento"
    elif blink_frequency < 15 and eye_closed_time > 0.10 * total_time:
        return "Cansado"
    elif blink_frequency >= 15 and eye_closed_time < 0.08 * total_time:
        return "Atento"
    else:
        return "Estado ambiguo, observar más tiempo"


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    
    # return the eye aspect ratio
    return ear
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor",default="shape_predictor_68_face_landmarks.dat", help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="camera", help="path to input video file")
ap.add_argument("-t", "--threshold", type = float, default=0.25, help="threshold to determine closed eyes")
ap.add_argument("-f", "--frames", type = int, default=3, help="the number of consecutive frames the eye must be below the threshold")


def conf_tela():
    #Configuracoes de tela
    turtle_writer = turtle.Turtle()
    turtle_writer.screen.setup(900,500)
    turtle_writer.screen.screensize(900, 200)
    turtle_writer.screen.setworldcoordinates(-10,-90,450,7.5)
    return turtle_writer

#carrega todo o texto do pdf em uma variável
def loadPDF(nameFile: str):

    pdfReader = PdfReader(nameFile) 
    pdfText = ""

     # Iterar sobre las páginas
    for page in pdfReader.pages:
        # Extraer texto de cada página y concatenarlo
        pdfText += page.extract_text()
    
    return pdfText

#quebra a string para mostrar o text de parte em parte indo até o próximo ponto final
# retorn array com o texto e a última posicao
def get_next_part_of_text(string, start, stop):
    while string[stop] != '.':
        stop = stop + 1
    part = [string[start:stop], stop]

    return part

def avancar_pagina(turtle_writer, text, start, stop, step):
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


# main
def main():
    #PDF
    text = loadPDF('pdf.pdf') # Aqui você deve inserir o nome do pdf que deseja visualizar
    start = 0
    stop = 25
    step = 25
    turtle_writer = conf_tela()

    args = vars(ap.parse_args())
    EYE_AR_THRESH = args['threshold']
    EYE_AR_CONSEC_FRAMES = args['frames']
    
    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    COUNTER_LEFT_EYE = 0
    COUNTER_RIGHT_EYE = 0
    TOTAL_LEFT = 0
    TOTAL_RIGHT = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])
    
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    
    # start the video stream thread
    print("[INFO] starting video stream thread...")
    print("[INFO] print q to quit...")
    if args['video'] == "camera":
        vs = VideoStream(src=0).start()
        fileStream = False
    else:
        vs = FileVideoStream(args["video"]).start()
        fileStream = True
    
    time.sleep(1.0)

    rostros = [0]
    eye_closed_time = [0]
    frames_with_closed_eyes = [0]
    start_time = time.time()
    # loop over frames from the video stream
    while True:
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process
        if fileStream and not vs.more():
            break
        
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        frame = imutils.resize(frame, width=900)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        
        i = 0
        # loop over the face detections
        for rect in rects:

            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            
            x = rect.left() 
            y = rect.top()
            w = rect.width()
            h = rect.height()

            
            if i >=len(rostros):
                rostros.append(0)
                eye_closed_time.append(0)
                frames_with_closed_eyes.append(0)
            
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
        
            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0
        
            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        
            # check to see if the eye aspect ratio is below the blink
            # # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                frames_with_closed_eyes[i]  += 1
        
            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if frames_with_closed_eyes[i] >= EYE_AR_CONSEC_FRAMES:
                    rostros[i] += 1
                    eye_closed_time[i] += frames_with_closed_eyes[i] / 30.0
                    TOTAL += 1
                    print("{} - Ambos os olhos estão piscando :D".format(TOTAL))
                    avancar_pagina(turtle_writer, text, start, stop, step)
                    time.sleep(0.1)
                    turtle_writer.screen.setworldcoordinates(-10,-90,450,7.5)

                # reset the eye frame counter
                frames_with_closed_eyes[i]  = 0
                COUNTER_LEFT_EYE = 0
                COUNTER_RIGHT_EYE = 0
            total_time = time.time() - start_time
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Blinks:{}".format(rostros[i]), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            estado = analyze_blink_state(rostros[i], total_time, eye_closed_time[i])
            cv2.putText(frame, estado, (x+w, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            blink_frequency = (rostros[i] / total_time) * 60
            cv2.putText(frame, "Blink Count: {}".format(blink_frequency), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Total Time: {}".format(total_time), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Eye Closed Time: {}".format(eye_closed_time[i]), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.putText(frame, "Right: {:.2f}".format(rightEAR), (300, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.putText(frame, "Left: {:.2f}".format(leftEAR), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            i = i + 1

         
    	# show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
if __name__ == '__main__' :
    main()