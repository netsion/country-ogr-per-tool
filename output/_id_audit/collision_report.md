# ID 碰撞与引用影响审计

- person 画像 17,679，org 画像 6,054
- 同一 org_id 挂多个不同组织：**0** 个 ID
- 同一 person_id 挂多个不同人物：**0** 个 ID

## 引用分类

| 引用方向 | profile_ok | profile_wrong | collision_shadow | registered_no_profile | registry_wrong_name | ghost | null_id |
|---|---:|---:|---:|---:|---:|---:|---:|
| work_org | 60,515 | 49 | 0 | 5,690 | 829 | 11 | 63,038 |
| person_rel | 32,617 | 27 | 0 | 6,595 | 93 | 61 | 13,908 |
| family | 1,663 | 0 | 0 | 188 | 6 | 6 | 16,401 |
| key_people | 18,047 | 7 | 0 | 4,464 | 224 | 26 | 2,674 |
| related_org | 18,298 | 139 | 0 | 5,467 | 192 | 130 | 8,634 |

## 碰撞最严重的国家（org ID）

| 国家 | 碰撞 org_id 数 | 碰撞 person_id 数 |
|---|---:|---:|

## 典型案例
