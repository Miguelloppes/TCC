'''
Dimencionador comprimento e largura

@author: Miguel Lopes de Moraes
@Version: 1.7
'''
import cv2
import numpy as np

def getContours(img,minArea=1000,numPoints_square=4):
    '''    
    Esta função é responsavel por achar os contornos do objeto e retornar os pontos mais extremos do mesmo 
    A mesma recebe os seguintes paramentros: 
        -img: Frame gerado pela camera;
        -minArea: Area minima de consideracao;
        -numPoints_square: Quantidade de pontos que devem ser retornado, por ser caixa devem ser considerados os quatros pontos mais extremos de uma caixa
    '''
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Achando os contornos da mascara gerada
    contours= sorted(contours, key=cv2.contourArea, reverse= True)
    print(contours)
    finalCountours = []
    for i in contours: #Rodando para todos os contornos gerados 
        area = cv2.contourArea(i) #Dados os contournos da imagem, retire a area 
        if area > minArea: #Se a area for maior do que a area mínima proposta o algortimo continua 
            peri = cv2.arcLength(i,True)#Achando o perimetro do objeto 
            approx = cv2.approxPolyDP(i,0.02*peri,True)#Aproximando esse perimentro a um poligono
            bbox = cv2.boundingRect(approx)#Aproximando o poligono em um retangulo / quadrado
            #Achando os quatros pontos extremos da caixa            
            if numPoints_square > 0:
                if len(approx) == numPoints_square:
                    finalCountours.append([len(approx),area,approx,bbox,i])
            else:
                finalCountours.append([len(approx),area,approx,bbox,i])
    finalCountours = sorted(finalCountours,key = lambda x:x[1] ,reverse= True)
    return img, finalCountours #Retornando a img com os valores dos pontos finais 

def reorder(finalPoints):
    '''
    Esta função é responsavel por reorganizar os pontos extremos da caixa e manter um padrao para os futuros calculos 
    A mesma recebe os seguintes paramentros: 
        -finalPoints: Os pontos gerados pela funcao getContours
    '''
    finalPointsNew = np.zeros_like(finalPoints)
    finalPoints = finalPoints.reshape((4,2))
    add = finalPoints.sum(1)
    finalPointsNew[0] = finalPoints[np.argmin(add)]
    finalPointsNew[3] = finalPoints[np.argmax(add)]
    diff = np.diff(finalPoints,axis=1)
    finalPointsNew[1]= finalPoints[np.argmin(diff)]
    finalPointsNew[2] = finalPoints[np.argmax(diff)]
    return finalPointsNew
 
def findDis(pts1,pts2):
    '''
    Esta função é a implementação da função matemática de distancia entre pontos
    Ela calcula a distancia entre os pontos extremos retornando os valor do comprimento e largura 
    A mesma recebe os seguintes paramentros: 
        -pts1: Conjunto x e y de um ponto extremo
        -ptss: Conjunto x e y de outro ponto extremo
    '''
    return ((pts2[0]-pts1[0])**2 + (pts2[1]-pts1[1])**2)**0.5

def display(frame,height,lenght,width):
    '''
    Esta função é responsável por mostrar na janela de execução os valores de comprimento, largura e altura
    Ela recebe como parametros:
        -frame: imagem da camera
        -depth: altura da caixa [cm]
        -lenght: comprimento da caixa [cm]
        -width: largura da caixa [cm]
    '''
    cv2.putText(frame, "Altura: " + str(round(height,3)), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)
    cv2.putText(frame, "Comprimento: " + str(lenght), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)
    cv2.putText(frame, "Largura: " + str(round(width,3)), (10,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)

def camera_find_points(mask,depth,distance_floor):
    '''
    Esta função é a função responsável por organizar todos a demais em uma só;
    Nela o algortimo gera os pontos, faz a reorganização e calcula a distancia chamando as devidas funções;
    Recebe como parametro: 
        -img: Frame da camera 
        -mask: a mascara que foi gerada pelas funcoes de segmentacao e o filtro canny 
        -depth: Profundidade encontrada pelo algoritmo 
        -distance: Distancia do chao até a camera
    '''
    imgContours , conts = getContours(mask,minArea=1000,numPoints_square=4) 
    #Funcoes de escala
    scale_x = -0.0162 * depth + 1.6004 
    scale_y = -0.0162 * depth + 1.6005 
    nX = nY = 0
    if len(conts) != 0:#Se os pontos gerados forem difrentes de 0
        for obj in conts: #Rodando para cada ponto achado
            cv2.polylines(imgContours,[obj[2]],True,(0,255,0),2)#Desenha um poligono na imagem em cima do objeto encontrado
            nPoints = reorder(obj[2]) #Usando a função de reorganização
            nW = round((findDis(nPoints[0][0],nPoints[1][0])/10),1) #Achando e arredondando os valor de Comprimento para 1 casa decimal
            nH = round((findDis(nPoints[0][0],nPoints[2][0])/10),1) #Achando e arredondando os valor de Largura para 1 casa decimal
            nX = round(nW*scale_x,2) #Multiplicando o valor de Comprimento pela escala e arredondado para 2 casas decimais
            nY = round(nH*scale_y,2) #Multiplicando o valor de Largura pela escala e arredondado para 2 casas decimais
 
    cv2.waitKey(1)

    return nX,nY