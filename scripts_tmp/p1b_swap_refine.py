# -*- coding: utf-8 -*-
"""P1-1b: refined second pass over the 348 held-back bracket cases.

Refined rules (conservative):
  - bracket pure-CJK AND (ends with entity suffix OR len>=5) AND not a place/status note
      -> swap {bracket}({prefix})
  - bracket "中文, 说明..." -> take first segment if it qualifies -> swap with that segment
  - status/note keywords (上市/现/前身/原名/更名/含/未...) -> leave in review
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
REVIEW = os.path.join(BASE, "output", "_social_audit", "p1_bracket_review.json")
DRY = "--dry" in sys.argv
CJK = re.compile(r"[\u4e00-\u9fff]")
BR = re.compile(r"^([^（(]*)[(（]([^)）]*)[)）]\s*$")

ENTITY_SUFFIX = re.compile(
    r"(公司|集团|航空|电力|银行|大学|学院|协会|委员会|基金会|基金|电视台|日报|媒体|"
    r"控股|投资|工业|能源|矿业|石油|电信|通信|科技|药业|医院|研究所|研究院|学会|"
    r"联盟|合作社|交易所|保险|证券|信托|事务所|商会|总会|联合会|教会|政党|出版社|"
    r"杂志|报社|电台|广播|剧院|乐团)$")
PLACE = re.compile(
    r"^(英国|美国|法国|德国|日本|中国|新加坡|香港|台湾|韩国|印度|澳大利亚|加拿大|巴西|"
    r"墨西哥|智利|阿根廷|秘鲁|哥伦比亚|西班牙|意大利|荷兰|瑞士|瑞典|挪威|丹麦|芬兰|"
    r"波兰|俄罗斯|乌克兰|土耳其|以色列|阿联酋|沙特|卡塔尔|科威特|巴林|阿曼|约旦|"
    r"黎巴嫩|伊拉克|伊朗|埃及|摩洛哥|突尼斯|阿尔及利亚|利比亚|南非|尼日利亚|加纳|"
    r"肯尼亚|埃塞俄比亚|坦桑尼亚|乌干达|赞比亚|津巴布韦|新西兰|巴新|斐济|越南|"
    r"泰国|马来西亚|印尼|菲律宾|柬埔寨|老挝|缅甸|孟加拉|巴基斯坦|斯里兰卡|尼泊尔|"
    r"蒙古|哈萨克|乌兹别克|吉尔吉斯|塔吉克|土库曼|阿塞拜疆|格鲁吉亚|亚美尼亚|"
    r"白俄罗斯|塞尔维亚|克罗地亚|斯洛伐克|捷克|匈牙利|奥地利|比利时|葡萄牙|希腊|"
    r"爱尔兰|冰岛|卢森堡|马耳他|塞浦路斯|巴林|英属|美国|英|美|法|德|日|中|新|韩)"
    r"([\u4e00-\u9fff]{1,4})?(市|省|州|地区|首都)?$")
NOTE = re.compile(r"上市|现|前身|原名|更名|又名|前称|简称|时任|曾任|后任|创办|成立|"
                  r"收购|合并|子公司|母公司|旗下|未|不详|待查|注|含|体系|另有|一说|"
                  r"^前|^后|分校|校区|营利|分支|分部|办事处|代表处|特许经营|家族|前称|"
                  r"营销|传播|节目|夫人|原配|之妻|之夫|长子|次子|女儿|儿子|父亲|母亲|亲属|"
                  r"会计师事务所|投资控股|资产管理|风险管控|国际咨询")


def save_json(f, d):
    tmp = f + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, f)


NON_CJK_SCRIPT = re.compile(r"[A-Za-zЀ-ӿ؀-ۿ฀-๿가-힯぀-ヿ]{2,}")


def qualify(zh):
    """High-confidence entity-name translation: pure CJK + strong suffix."""
    zh = zh.strip()
    if not zh or not CJK.search(zh):
        return False
    if len(zh) < 2 or len(zh) > 14:
        return False
    if NOTE.search(zh):
        return False
    if NON_CJK_SCRIPT.search(zh):
        return False
    if PLACE.match(zh):
        return False
    return bool(ENTITY_SUFFIX.search(zh))


def refine(value):
    m = BR.match(value or "")
    if not m:
        return None
    pre, inside = m.group(1).strip(), m.group(2).strip()
    if not pre or not inside:
        return None
    if " / " in pre or "/" in pre:
        return None  # multi-entity prefix, ambiguous
    # split "中文, 说明"
    parts = re.split(r"[,，;；]", inside)
    # any segment carrying note semantics -> whole bracket is a note
    for p in parts:
        if p.strip() and NOTE.search(p.strip()):
            return None
    cand = None
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if qualify(p) and not re.search(r"[A-Za-z]{3,}", p):
            cand = p
            break
    if cand:
        return f"{cand}({pre})"
    return None


def main():
    review = json.load(open(REVIEW, encoding="utf-8"))
    swapped = 0
    remain = []
    for item in review:
        new = refine(item["value"])
        if not new:
            remain.append(item)
            continue
        f = os.path.join(BASE, item["file"])
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            remain.append(item)
            continue
        arr, idx, key = re.match(r"(\w+)\[(\d+)\]\.(\w+)", item["field"]).groups()
        idx = int(idx)
        try:
            if d[arr][idx].get(key) == item["value"]:
                if not DRY:
                    d[arr][idx][key] = new
                    save_json(f, d)
                swapped += 1
            else:
                remain.append(item)
        except Exception:
            remain.append(item)
    print(("DRY-RUN" if DRY else "APPLIED"), f"second-pass swapped={swapped}, remaining={len(remain)}")
    if not DRY:
        with open(REVIEW, "w", encoding="utf-8") as fh:
            json.dump(remain, fh, ensure_ascii=False, indent=1)
        print("review file updated ->", REVIEW)


if __name__ == "__main__":
    main()
