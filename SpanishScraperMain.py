import SpanishScraperFunctions as scraper
import pandas as pd
from bs4 import BeautifulSoup

#instantiates a list to put the data in
df_list = []

#picks the list of subjects to scrape
subject_list = ["Ingeniería", "Mecánica","Técnica","Energía","Calderas","Máquinas","hidráulica","hidroeléctrica","eléctrica", "Electrotecnia","Telecomunicaciones", "Motores","Tratamiento mecanizado","Transmisión mecánica", "Engranajes", "Lubricación", "Minería","Ingeniería militar", "Ingeniería civil", "comunicación", "Construcciones", "Canales", "riegos", "drenajes", "sanitaria", "Saneamiento", "iluminación", "desechos","Alumbrado", "Luminotecnia", "transporte", "Vehículos", "Ingeniería naval", "Barcos", "buques", "navíos","Aeronáutica","agricultura","Silvicultura", "Ingeniería forestal", "Agronomía", "Técnicas agrícolas", "Fitopatología", "Cereales", "Forrajes","Árboles frutales", "Viticultura","Horticultura", "hortalizas", "Floricultura", "Jardinería","Zootecnia", "Ganadería", "cría de animals", "caza", "pesca", "apicultura", "sericultura", "piscultura", "gestión", "comercio", "industria", "Comunicaciones", "Correo", "filatelia", "contabilidad","Auditoría","Tecnología química", "Industrias afines", "Industria química","Productos químicos","Pirotecnia", "Explosivos", "Combustibles","Bebidas", "Estimulantes","aceites", "grasas", "ceras", "Adhesivos", "Gomas", "Resinas","vidrio", "cerámica", "cemento", "hormigón","colorantes", "tintas","Metalurgia","Joyería","hierro", "acero", "metales","madera", "cuero","papel", "carton", "textil","plásticos","cable", "cordelería", "Piedra","Relojería", "Balanzas", "básculas","control automático","impresoras","Aparatos ópticos", "instrumentos ópticos","Técnica acústica", "Instrumentos musicales","Herrería", "forja", "fundición","Ferretería", "Cerrajería", "Lámparas", "Estufas", "hornos", "calentadores","mueble, Tapicería","Guarnicionería", "Marroquinería", "Zapatería", "Bricolaje","Albañilería", "hormigón", "acero","Carpintería", "Ebanistería","calefacción", "ventilación", "climatización"]

#Scrapes each subject
for x in subject_list:
    df_list.append(scraper.Full_Subject_Scrape(x))

#gets both a raw and duplicates-removed frame 
FullDataFrame = pd.concat(df_list)
DuplicatesRemovedDataFrame = FullDataFrame.drop_duplicates(subset=['Title','Year'], keep = 'first')

#saves frames to your computer 
FullDataFrame.to_csv("FullSpanishData.csv")
DuplicatesRemovedDataFrame.to_csv("CleanSpanishData.csv")
