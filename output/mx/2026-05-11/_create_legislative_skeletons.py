import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

missing_senators = [
    "Juan Antonio Martin del Campo", "Maria de Jesus Diaz Marmolejo", "Nora Ruvalcaba Gamez",
    "Julieta Ramirez Padilla", "Armando Ayala Robles", "Maximo Garcia Lopez",
    "Lucia Trasvina Waldenrath", "Homero Davis Castro", "Susana Zatarain Garcia",
    "Maria Martina Kantun Can", "Anibal Ostoa Ortega", "Daniel Barreda Pavon",
    "Sasil de Leon Villard", "Jose Manuel Cruz Castellanos", "Luis Armando Melgar Bravo",
    "Nora Yu Hernandez", "Juan Carlos Loera de la Rosa", "Mario Vazquez Robles",
    "Francisco Chiguil Figueroa", "Cynthia Lopez Castro",
    "Luis Fernando Salazar Fernandez", "Cecilia Guadiana Mandujano", "Miguel Riquelme Solis",
    "Virgilio Mendoza Amezcua", "Ana Karen Hernandez Aceves", "Mely Romero Celis",
    "Margarita Valdez Martinez", "Gina Campuzano Gonzalez",
    "Ricardo Sheffield Padilla", "Virginia Magana Fonseca", "Miguel Marquez Marquez",
    "Beatriz Mojica Morga", "Felix Salgado Macedonio",
    "Simey Olvera Bautista", "Cuauhtemoc Ochoa Fernandez",
    "Carlos Lomeli Bolanos", "Rocio Corona Nakamura", "Francisco Ramirez Acuna",
    "Higinio Martinez Miranda", "Mariela Gutierrez Escalante", "Enrique Vargas del Villar",
    "Celeste Ascencio Ortega", "Raul Moron Orozco", "Araceli Saucedo Reyes",
    "Victor Mercado Salgado", "Juanita Guerra Mena", "Angel Garcia Yanez",
    "Jasmine Bugarin Rodriguez", "Pavel Jarero Velazquez", "Ivideliza Reyes Hernandez",
    "Waldo Fernandez Gonzalez", "Judith Diaz Delgado", "Luis Donaldo Colosio Riojas",
    "Antonino Morales Toledo", "Luisa Cortes Garcia", "Laura Estrada Mauro",
    "Ignacio Mier Velazco", "Lizeth Sanchez Garcia", "Nestor Camarillo Medina",
    "Agustin Dorantes Lambarri", "Beatriz Robles Gutierrez",
    "Anahi Gonzalez Hernandez", "Eugenio Segura Vazquez", "Mayuli Martinez Simon",
    "Ruth Gonzalez Silva", "Gilberto Hernandez Villafuerte", "Veronica Rodriguez Hernandez",
    "Imelda Castro Castro", "Enrique Inzunza Cazarez", "Paloma Sanchez Ramos",
    "Lorenia Valles Sampedro", "Heriberto Aguilar Castillo", "Ivan Jaimes Archundia",
    "Alejandra Arias Trevilla", "Oscar Canton Zetina", "Jose Sabino Herrera Dagdug",
    "Olga Patricia Sosa Ruiz", "Jose Ramon Gomez Leal", "Imelda Sanmiguel Sanchez",
    "Jose Antonio Alvarez Lima", "Ana Lilia Rivera Rivera", "Anabell Avalos Zempoalteca",
    "Raquel Bonilla Herrera", "Manuel Huerta Ladron de Guevara", "Miguel Angel Yunes Marquez",
    "Veronica Camino Farjat", "Jorge Carlos Ramirez Marin", "Rolando Zapata Bello",
    "Veronica Diaz Robles", "Claudia Anaya Mota",
    "Marko Cortes Mendoza", "Ricardo Anaya Cortes", "Lilly Tellez Garcia",
    "Mauricio Vila Dosal", "Laura Esquivel Torres",
    "Pablo Angulo Brinceno", "Cristina Ruiz Sandoval",
    "Yeidckol Polevnsky Gurwitz", "Maki Esther Ortiz Dominguez", "Luis Alfonso Silva Romo",
    "Alejandra Barrales", "Amalia Garcia Medina", "Adan Augusto Lopez Hernandez",
    "Guadalupe Chavira de la Rosa", "Alejandro Esquer Verdugo", "Susana Harp Iturribarria",
    "Emmanuel Reyes Carmona", "Martha Lucia Micher Camarena", "Javier Corral Jurado",
    "Geovanna Banuelos de la Torre", "Alfonso Cepeda Salas", "Karina Ruiz Ruiz",
    "Alejandro Murat Hinojosa", "Edith Lopez Hernandez",
]

missing_deputies = [
    "Paulina Rubio Fernandez", "Julieta Villalpando Riquelme", "Alan Sahir Marquez Becerra",
    "Nayeli Arlen Fernandez Cruz", "Magdalena del Socorro Nunez Monreal",
    "Fuensanta Guadalupe Guerrero Esquivel", "Laura Ballesteros Mancilla",
    "Elias Lixa Abimerhi", "Leonel Godoy Rangel", "Carlos Alberto Ulloa Perez",
    "Merilyn Gomez Pozos", "Julio Cesar Moreno Rivera", "Luis Arturo Oliver Cen",
    "Humberto Coss y Leon Zuniga", "Pedro Vazquez Gonzalez",
    "Rocio Adriana Abreu Artinano", "Miguel Angel Salim Alle",
    "Yoloczin Lizbeth Dominguez Serna", "Anais Miriam Burgos Hernandez",
    "Gabriela Benavides Cobos", "Tey Mollinedo Cano", "Marcela Guerra Castillo",
    "Ana Karina Rojo Pimentel", "Paola Michell Longoria Lopez", "Tania Palacios Kuri",
    "Javier Octavio Herrera Borunda", "Leticia Barrera Maldonado",
    "Hugo Eric Flores Cervantes",
]

all_missing = [(n, "senator", "MX-GOV-003") for n in missing_senators] + \
              [(n, "deputy", "MX-GOV-004") for n in missing_deputies]

print(f"Total: {len(all_missing)} persons ({len(missing_senators)} senators + {len(missing_deputies)} deputies)")

start_id = 251
for idx, (name, role, org_id) in enumerate(all_missing):
    pid = f"MX-PERSON-{start_id + idx:06d}"
    skeleton = {
        "person_id": pid,
        "wikidata_qid": None,
        "name": name,
        "name_en": name,
        "name_zh": None,
        "aliases": [],
        "nationality": "MX",
        "gender": None,
        "birth_date": None,
        "birth_place": None,
        "contacts": [],
        "current_positions": [],
        "education": [],
        "work_experience": [
            {
                "start_date": "2024-09-01",
                "end_date": None,
                "organization": f"{name}",
                "org_id": org_id,
                "position": f"联邦参议员 (Senador/a)" if role == "senator" else f"联邦众议员 (Diputado/a)"
            }
        ],
        "person_relationships": [],
        "social_accounts": [],
        "family_members": [],
        "political_stances": [],
        "major_achievements": [],
        "biography_summary": None,
        "profile": {"source_url": None, "local_path": None},
        "collection_meta": {
            "collection_date": "2026-05-22",
            "phase": "phase4_person_profile",
            "data_sources": [],
            "completeness_score": 9,
            "notes": None,
            "quotes": []
        }
    }
    path = f"persons/{pid}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(skeleton, f, ensure_ascii=False, indent=2)

print(f"Created {len(all_missing)} skeleton files: MX-PERSON-000251 to MX-PERSON-{start_id + len(all_missing) - 1:06d}")
print(f"Senators: 000251-000{start_id + len(missing_senators) - 1}")
print(f"Deputies: 000{start_id + len(missing_senators)}-000{start_id + len(all_missing) - 1:06d}")
