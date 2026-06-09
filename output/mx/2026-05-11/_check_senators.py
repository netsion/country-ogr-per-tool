import json, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

# Build name lookup from all 250 person files
persons = {}
for i in range(1, 251):
    path = f'persons/MX-PERSON-{i:06d}.json'
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        p = json.load(f)
    name_en = p.get('name_en', '').lower()
    name = p.get('name', '').lower()
    pid = p['person_id']
    score = p.get('collection_meta', {}).get('completeness_score', 0)
    persons[name_en] = (pid, score)
    if name != name_en:
        persons[name] = (pid, score)

def normalize(s):
    return re.sub(r'[áàä]', 'a', re.sub(r'[éèë]', 'e', re.sub(r'[íìï]', 'i',
        re.sub(r'[óòö]', 'o', re.sub(r'[úùü]', 'u', re.sub(r'[ñ]', 'n', s.lower()))))))

norm_persons = {normalize(k): v for k, v in persons.items()}

def find_person(name):
    key = name.lower().strip()
    if key in persons:
        return persons[key]
    nkey = normalize(key)
    if nkey in norm_persons:
        return norm_persons[nkey]
    parts = set(nkey.split())
    best = None
    best_score = 0
    for nk, (pid, score) in norm_persons.items():
        np = set(nk.split())
        overlap = len(parts & np) / max(len(parts | np), 1)
        if overlap > best_score:
            best_score = overlap
            best = (pid, score)
    if best_score >= 0.5:
        return best
    return None

# Senators
senators = [
    "Juan Antonio Martin del Campo", "Maria de Jesus Diaz Marmolejo", "Nora Ruvalcaba Gamez",
    "Julieta Ramirez Padilla", "Armando Ayala Robles", "Maximo Garcia Lopez",
    "Lucia Trasvina Waldenrath", "Homero Davis Castro", "Susana Zatarain Garcia",
    "Maria Martina Kantun Can", "Anibal Ostoa Ortega", "Daniel Barreda Pavon",
    "Sasil de Leon Villard", "Jose Manuel Cruz Castellanos", "Luis Armando Melgar Bravo",
    "Nora Yu Hernandez", "Juan Carlos Loera de la Rosa", "Mario Vazquez Robles",
    "Francisco Chiguil Figueroa", "Karen Castrejon Trujillo", "Cynthia Lopez Castro",
    "Luis Fernando Salazar Fernandez", "Cecilia Guadiana Mandujano", "Miguel Riquelme Solis",
    "Virgilio Mendoza Amezcua", "Ana Karen Hernandez Aceves", "Mely Romero Celis",
    "Alejandro Gonzalez Yanez", "Margarita Valdez Martinez", "Gina Campuzano Gonzalez",
    "Ricardo Sheffield Padilla", "Virginia Magana Fonseca", "Miguel Marquez Marquez",
    "Beatriz Mojica Morga", "Felix Salgado Macedonio", "Manuel Anorve Banos",
    "Simey Olvera Bautista", "Cuauhtemoc Ochoa Fernandez", "Carolina Viggiano Austria",
    "Carlos Lomeli Bolanos", "Rocio Corona Nakamura", "Francisco Ramirez Acuna",
    "Higinio Martinez Miranda", "Mariela Gutierrez Escalante", "Enrique Vargas del Villar",
    "Celeste Ascencio Ortega", "Raul Moron Orozco", "Araceli Saucedo Reyes",
    "Victor Mercado Salgado", "Juanita Guerra Mena", "Angel Garcia Yanez",
    "Jasmine Bugarin Rodriguez", "Pavel Jarero Velazquez", "Ivideliza Reyes Hernandez",
    "Waldo Fernandez Gonzalez", "Judith Diaz Delgado", "Luis Donaldo Colosio Riojas",
    "Antonino Morales Toledo", "Luisa Cortes Garcia", "Laura Estrada Mauro",
    "Ignacio Mier Velazco", "Lizeth Sanchez Garcia", "Nestor Camarillo Medina",
    "Guadalupe Murguia Gutierrez", "Agustin Dorantes Lambarri", "Beatriz Robles Gutierrez",
    "Anahi Gonzalez Hernandez", "Eugenio Segura Vazquez", "Mayuli Martinez Simon",
    "Ruth Gonzalez Silva", "Gilberto Hernandez Villafuerte", "Veronica Rodriguez Hernandez",
    "Imelda Castro Castro", "Enrique Inzunza Cazarez", "Paloma Sanchez Ramos",
    "Lorenia Valles Sampedro", "Heriberto Aguilar Castillo", "Ivan Jaimes Archundia",
    "Alejandra Arias Trevilla", "Oscar Canton Zetina", "Jose Sabino Herrera Dagdug",
    "Olga Patricia Sosa Ruiz", "Jose Ramon Gomez Leal", "Imelda Sanmiguel Sanchez",
    "Jose Antonio Alvarez Lima", "Ana Lilia Rivera Rivera", "Anabell Avalos Zempoalteca",
    "Raquel Bonilla Herrera", "Manuel Huerta Ladron de Guevara", "Miguel Angel Yunes Marquez",
    "Veronica Camino Farjat", "Jorge Carlos Ramirez Marin", "Rolando Zapata Bello",
    "Veronica Diaz Robles", "Saul Monreal Avila", "Claudia Anaya Mota",
    "Marko Cortes Mendoza", "Michel Gonzalez Marquez", "Ricardo Anaya Cortes",
    "Lilly Tellez Garcia", "Mauricio Vila Dosal", "Laura Esquivel Torres",
    "Alejandro Moreno Cardenas", "Pablo Angulo Brinceno", "Cristina Ruiz Sandoval",
    "Alberto Anaya Gutierrez", "Yeidckol Polevnsky Gurwitz", "Manuel Velasco Coello",
    "Maki Esther Ortiz Dominguez", "Luis Alfonso Silva Romo", "Clemente Castaneda Hoeflich",
    "Alejandra Barrales", "Amalia Garcia Medina", "Adan Augusto Lopez Hernandez",
    "Guadalupe Chavira de la Rosa", "Alejandro Esquer Verdugo", "Susana Harp Iturribarria",
    "Gerardo Fernandez Norona", "Laura Itzel Castillo Juarez", "Emmanuel Reyes Carmona",
    "Martha Lucia Micher Camarena", "Javier Corral Jurado", "Geovanna Banuelos de la Torre",
    "Alfonso Cepeda Salas", "Karina Ruiz Ruiz", "Alejandro Murat Hinojosa",
    "Edith Lopez Hernandez",
]

# Key deputies (leadership + commission presidents)
deputies = [
    "Kenia Lopez Rabadan", "Sergio Carlos Gutierrez Luna", "Paulina Rubio Fernandez",
    "Raul Bolanos Cacho Cue", "Julieta Villalpando Riquelme", "Alan Sahir Marquez Becerra",
    "Nayeli Arlen Fernandez Cruz", "Magdalena del Socorro Nunez Monreal",
    "Fuensanta Guadalupe Guerrero Esquivel", "Laura Ballesteros Mancilla",
    "Ricardo Monreal Avila", "Elias Lixa Abimerhi", "Ruben Moreira Valdez",
    "Carlos Alberto Puente Salas", "Reginaldo Sandoval Flores", "Ivonne Ortega Pacheco",
    "Leonel Godoy Rangel", "Carlos Alberto Ulloa Perez", "Merilyn Gomez Pozos",
    "Julio Cesar Moreno Rivera", "Luis Arturo Oliver Cen", "Humberto Coss y Leon Zuniga",
    "Pedro Vazquez Gonzalez", "Rocio Adriana Abreu Artinano", "Miguel Angel Salim Alle",
    "Yoloczin Lizbeth Dominguez Serna", "Anais Miriam Burgos Hernandez",
    "Gabriela Benavides Cobos", "Tey Mollinedo Cano", "Marcela Guerra Castillo",
    "Ana Karina Rojo Pimentel", "Paola Michell Longoria Lopez", "Tania Palacios Kuri",
    "Javier Octavio Herrera Borunda", "Leticia Barrera Maldonado", "Hugo Eric Flores Cervantes",
    "Noemi Luna Ayala",
]

found_s = 0
missing_s = []
for name in senators:
    result = find_person(name)
    if result:
        found_s += 1
    else:
        missing_s.append(name)

found_d = 0
missing_d = []
for name in deputies:
    result = find_person(name)
    if result:
        found_d += 1
    else:
        missing_d.append(name)

print(f'SENATE: {found_s}/128 already in dataset, {len(missing_s)} MISSING')
print()
print(f'DEPUTIES (key): {found_d}/{len(deputies)} already in dataset, {len(missing_d)} MISSING')
print()

all_missing = missing_s + missing_d
print(f'TOTAL MISSING: {len(all_missing)}')
print()
print('Missing senators:')
for n in missing_s:
    print(f'  {n}')
print()
print('Missing key deputies:')
for n in missing_d:
    print(f'  {n}')
