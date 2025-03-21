import cv2
import numpy as np
import os
import math

# Parâmetros configuráveis
PARAMS = {
    'colors': [
        {'name': 'Yellow', 'lower': (20, 100, 100), 'upper': (30, 255, 255)},
        {'name': 'Blue', 'lower': (100, 100, 100), 'upper': (130, 255, 255)},
        # Adicione mais cores conforme necessário
    ],
    'canny_threshold1': 100,
    'canny_threshold2': 200,
    'kernel_size': 5
}

# Função de callback que não realiza nenhuma ação.
def nothing(x):
    pass

def preprocess_image(image_path, max_width=800, max_height=600):
    # Carregar a imagem
    image = cv2.imread(image_path)
    if image is None:
        print("Erro ao carregar a imagem")
        return None
    
    # Manter o tamanho proporcional, sem distorcer
    h, w = image.shape[:2]
    scale_factor = min(max_width / w, max_height / h)
    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)
    
    # Redimensionar proporcionalmente
    image = cv2.resize(image, (new_w, new_h))

    # Converter para HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Equalização de Histograma para normalizar a iluminação
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])

    return image, hsv

def calculate_histogram(hsv_image):
    # Calcular o histograma para o canal H (matiz)
    hist_hue = cv2.calcHist([hsv_image], [0], None, [256], [0, 256])
    return hist_hue

def adjust_hsv_limits_based_on_histogram(hist_hue, hue_margin = 15):
    # Encontre o valor de H com maior frequência (modo)
    max_hue_value = np.argmax(hist_hue)

    # Ajuste os limites com base no valor de H mais comum
    lower_hue = max(0, max_hue_value - hue_margin)
    upper_hue = min(255, max_hue_value + hue_margin)
    
    return lower_hue, upper_hue

def segment_colors(hsv, lower, upper):
    return cv2.inRange(hsv, lower, upper)

def detect_edges(image, threshold1, threshold2):
    # Convertendo a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicando o Canny para detecção de bordas
    return cv2.Canny(gray, threshold1, threshold2)

def morphological_operations(edges, kernel_size):
    # Definir um kernel para as transformações morfológicas
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

def detect_contours(edges):
    # Encontrar os contornos na imagem de bordas
    return cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

def detect_circular_shape(approx):
    perimeter = cv2.arcLength(approx, True)
    area = cv2.contourArea(approx)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * (area / (perimeter ** 2))
    return 0.75 < circularity < 1.25

def detect_cross(approx):
    angles = []
    for i in range(len(approx)):
        p1, p2, p3 = approx[i - 1][0], approx[i][0], approx[(i + 1) % len(approx)][0]
        v1, v2 = np.array(p1) - np.array(p2), np.array(p3) - np.array(p2)
        angle = np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
        angles.append(angle)
    return sum(80 <= a <= 100 for a in angles) >= 4

def classify_shapes(contours):
    shapes = []
    
    for contour in contours:
        # Aproximar o contorno para uma forma simples
        epsilon = 0.02 * cv2.arcLength(contour, True)  # Precisão da aproximação
        approx = cv2.approxPolyDP(contour, epsilon, True)

        shape_type = "Outro"

        # Classificar as formas
        if len(approx) == 3:
            shape_type = "Triangulo"
        elif len(approx) == 4:
            # Verificar se é quadrado ou retângulo
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            shape_type = "Quadrado" if 0.95 <= aspect_ratio <= 1.05 else "Retangulo"
        elif len(approx) > 4:
            if detect_circular_shape(approx):
                shape_type = "Circulo" 
        
        if detect_cross(approx):
            shape_type = "Cruz"
        shapes.append((approx, shape_type))
    
    return shapes

def detect_composite_shape(shapes):
    # Função para detectar formas compostas, com base na proximidade
    composite_shapes = []
    threshold_distance = 100  # Distância máxima para considerar duas formas como parte de uma base
    
    for i, (shape1, type1) in enumerate(shapes):
        for j, (shape2, type2) in enumerate(shapes):
            if i >= j:
                continue  # Evitar comparar o mesmo par de formas duas vezes
            
            # Calcular a distância entre os centros das formas
            M1 = cv2.moments(shape1)
            M2 = cv2.moments(shape2)
            
            if M1["m00"] == 0 or M2["m00"] == 0:
                continue  # Evitar divisão por zero
            
            cX1 = int(M1["m10"] / M1["m00"])
            cY1 = int(M1["m01"] / M1["m00"])
            cX2 = int(M2["m10"] / M2["m00"])
            cY2 = int(M2["m01"] / M2["m00"])

            # Calcular a distância Euclidiana entre os centros das formas
            dist = math.sqrt((cX2 - cX1)**2 + (cY2 - cY1)**2)

            # Verificar se as formas estão suficientemente próximas para formar uma base
            if dist < threshold_distance:
                # Considerar essas duas formas como parte de uma base composta
                composite_shapes.append((shape1, shape2))

    return composite_shapes

def draw_composite_shapes(image, composite_shapes):
    image_with_composites = image.copy()
    
    for shape1, shape2 in composite_shapes:
        # Desenhar as formas compostas
        cv2.drawContours(image_with_composites, [shape1], -1, (0, 255, 0), 2)
        cv2.drawContours(image_with_composites, [shape2], -1, (0, 0, 255), 2)
    
    return image_with_composites

def draw_shapes(image, shapes):
    image_with_shapes = image.copy()
    for shape, shape_type in shapes:
        cv2.drawContours(image_with_shapes, [shape], -1, (0, 255, 0), 2)
        M = cv2.moments(shape)
        if M["m00"] != 0:
            cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            cv2.putText(image_with_shapes, shape_type, (cX - 50, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image_with_shapes

def overlay_params(image, params):
    # Exibir parâmetros ajustados em tempo real
    text = f"Canny Threshold1: {params['Canny Threshold1']} | Canny Threshold2: {params['Canny Threshold2']}"
    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return image

def detect_black_square(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Limiarizar a imagem para destacar os quadrados pretos
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Detectar contornos dos quadrados pretos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    black_squares = []
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            black_squares.append(approx)

    return black_squares

def draw_black_squares(image, black_squares):
    # Desenhar os quadrados pretos na imagem
    image_with_squares = image.copy()
    
    for square in black_squares:
        cv2.drawContours(image_with_squares, [square], -1, (0, 0, 0), 2)  # Preto
        # Opcionalmente, podemos desenhar um texto com a identificação
        M = cv2.moments(square)
        if M["m00"] != 0:
            cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            cv2.putText(image_with_squares, "Quadrado Preto", (cX - 50, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    return image_with_squares

def create_ui():
    # Criar a janela de controle
    cv2.namedWindow("Controle de Parametros")

    # Criação de sliders para ajustar parâmetros de segmentação de cores e Canny
    for param, value, max_val in [
        ("Canny Threshold1", 100, 255), ("Canny Threshold2", 200, 255),
        ("Kernel Size", 5, 20), ("Lower H", 20, 179), ("Lower S", 100, 255), ("Lower V", 100, 255),
        ("Upper H", 30, 179), ("Upper S", 255, 255), ("Upper V", 255, 255)
    ]:
        cv2.createTrackbar(param, "Controle de Parametros", value, max_val, nothing)

def get_slider_values():
    values = {param: cv2.getTrackbarPos(param, "Controle de Parametros") for param in [
        "Canny Threshold1", "Canny Threshold2", "Kernel Size",
        "Lower H", "Lower S", "Lower V", "Upper H", "Upper S", "Upper V"
    ]}
    return values


def process_images_in_folder(folder_path):

    # Criar a interface de usuário
    create_ui()
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        image, hsv = preprocess_image(image_path)
        if image is None:
            continue
        
        while True:
            params = get_slider_values()
            lower_bound = (params["Lower H"], params["Lower S"], params["Lower V"])
            upper_bound = (params["Upper H"], params["Upper S"], params["Upper V"])
            mask = segment_colors(hsv, lower_bound, upper_bound)
            edges = detect_edges(image, params["Canny Threshold1"], params["Canny Threshold2"])
            processed_edges = morphological_operations(edges, max(1, params["Kernel Size"]))
            contours = detect_contours(processed_edges)
            shapes = classify_shapes(contours)
            composite_shapes = detect_composite_shape(shapes)
            black_squares = detect_black_square(image)
            image_with_black_squares = draw_black_squares(image, black_squares)
            image_with_shapes = draw_shapes(image, shapes)
            image_with_composites = draw_composite_shapes(image, composite_shapes)
            image_with_params = overlay_params(image_with_composites, params)

            # Exibir resultados
            cv2.imshow("Imagem Original", image)
            cv2.imshow("Segmentacao", mask)
            cv2.imshow("Bordas", processed_edges)
            cv2.imshow("Imagem com Formas Normais", image_with_shapes)
            cv2.imshow("Imagem com Formas Compostas", image_with_composites)
            cv2.imshow("Quadrados Pretos", image_with_black_squares)
            
            # Sair ao pressionar 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    cv2.destroyAllWindows()

process_images_in_folder('C:/Users/cecil/OneDrive/Documentos/EDRA/CHOSEN')
