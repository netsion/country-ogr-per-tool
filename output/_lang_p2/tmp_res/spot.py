import io, json, re
base = r"D:/ai-workspace/apec-osint-tool/output/_lang_p2"
pat = re.compile(r'[a-zA-Z]')
allowed = re.compile(r'^(TAFE|IE|ADA|SOCAR|LTAC|KHK|BDO|MB|EG|imagine|Makan Ceria|Amber International|Perennial Holdings|Straight Ahead|Room 32|KPMG|BNET|LONAB|PA[SŞ]HA|Bank Standard|Unibank|Faso|Avenue 226|Burkina24|GRAAD|APPRO-MAT BURKINA|Yam Pukri|AITV-RFO|INEDIT|OZONE|Artistes Productions|DEFICOM|OHADA|COP29|WUF13|EURONEST|PASHA|Murdoch|Kudos|De Wintern|Osborne|Prodigy Motorsport|Smith&Duda|Salt & Shein|Growth Farms|Transit Systems|SingTel Optus|Austereo|LBC|2UE|2CUZ|D&H|Fineko/ABC|Embawood|Westgate|Ziran|Medeks|BISON|La Vida|Altus|Buta|ASAN|SƏNİNLƏ|Laafi 7|Burkindlim|CAFEC-KA|CEPEC|INJAZ|BENEFIT|Silah Gulf|Retal|Mazad|Beyon|SICO|Alba Daiki|South32|ARRAY|Woolworths|McDonald|3BL|Reso|CHAPO|Fundament|Seed|4PM|Olive VFM|DHL|AirTrip|Procare|Ergo|TV One|Li(l|)ium)$')
suspects = []
for num in ["006","007","008","009","010"]:
    with io.open(f"{base}/results/batch_{num}.json", encoding="utf-8") as f:
        res = json.load(f)
    for r in res:
        z = r["zh"]
        if z and pat.search(z):
            # find latin tokens
            toks = re.findall(r'[A-Za-z][A-Za-z&.\'’\-/]*', z)
            for t in toks:
                if len(t) >= 4 and t.lower() in {"force","regiment","office","ministry","company","station","limited","school","college","university","the","and","of"}:
                    suspects.append((num, r["i"], z))
                elif not allowed.match(t):
                    suspects.append((num, r["i"], z))
for s in suspects[:40]:
    print(s)
print("suspects:", len(suspects))
