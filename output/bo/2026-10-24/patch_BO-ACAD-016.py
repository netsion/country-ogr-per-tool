# -*- coding: utf-8 -*-
"""Patch BO-ACAD-016: profile as image ref, add key people + event."""
import json

PATH = 'D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/orgs/BO-ACAD-016.json'

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

# profile 字段按 schema 为机构图片引用（Wikimedia Commons 上的科学院建筑照片）
data['profile'] = {
    'source_url': 'https://thumb.wikimedia.org/wikipedia/commons/thumb/7/72/Academia_Nacional_de_Ciencias_1.jpg/330px-Academia_Nacional_de_Ciencias_1.jpg',
    'local_path': None,
}

# 补充两名关键人物（均见于 UPSA 2026-07-02 院士入职仪式报道）
data['key_people'] += [
    {
        'person_id': None,
        'name': '加斯东·梅希亚·布朗 (Gastón Mejía Brown)',
        'title': '圣克鲁斯分会主席 (Presidente del Consejo Departamental Santa Cruz)',
        'title_description': '主持科学院圣克鲁斯分会及该地区研究理事会事务。',
        'description': '2026年7月2日在蒂莫西·基伦的院士入职仪式上代表分会致辞（UPSA报道）；同年9月出席66周年荣誉全会（官网新闻稿）。',
    },
    {
        'person_id': None,
        'name': '马里奥·苏亚雷斯·里格洛斯 (Mario Suárez Riglos)',
        'title': '正式院士 (Académico de Número)',
        'title_description': '科学院终身院士。',
        'description': '2026年7月2日在蒂莫西·基伦的院士入职仪式上介绍其科学生涯（UPSA报道）。',
    },
]

# 补充第5条近期事件：65周年
data['recent_events'] += [
    {
        'date': '2025-09-22',
        'title': '庆祝重建成立65周年',
        'description': '科学院围绕9月23日重建纪念日开展65周年庆祝活动，院长曼努埃尔·阿雷利亚诺·拉米雷斯以院长身份出席纪念活动；圣安德烈斯大学(UMSA)校办电台"圣安德烈斯广播电台97.6"对庆祝及表彰进行了报道。',
        'impact': '巩固与公立大学体系（UMSA）的传播与合作关系。',
        'source': 'https://www.facebook.com/radiosanandres97/videos/reconocimiento-a-las-mentes-que-transforman-bolivia-con-ciencia/834195132603066/',
    },
]

# notes 同步 profile 语义（profile 为图片引用而非文字画像）
data['collection_meta']['notes'] += ' profile字段按schema存为机构图片引用(Wikimedia Commons科学院建筑照片)。'

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('OK patched: profile=img_ref, key_people=%d, recent_events=%d' % (len(data['key_people']), len(data['recent_events'])))
