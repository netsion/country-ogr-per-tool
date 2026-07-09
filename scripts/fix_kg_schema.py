"""Fix KG org schema issues:
- invalid relationship_type → map to valid enum
- invalid industries → map to valid enum
- apec_stance dict → string (notes field)
- core_business dict → string (summary_zh field)
- social_accounts dict → list of dicts
"""
import json, glob, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# Maps from invalid value → valid value
RT_MAP = {
    'peer': 'sibling',
    'member': 'member_of',
    'parent_company': 'parent_org',
    'parent org': 'parent_org',
    'former_owner': 'other',
    'former_beneficial_owner': 'other',
    'former_shareholder': 'other',
    'former_competitor': 'other',
    'competitor': 'other',
    'joint_venture': 'strategic_alliance',
    'related venture': 'affiliated',
    'creditor': 'other',
    'listing venue': 'other',
    'shareholder': 'controlling_shareholder',
    'aircraft_lessor': 'supplier',
    'operating_base': 'other',
    'destination': 'customer',
    'engine_supplier': 'supplier',
    'aircraft_manufacturer': 'supplier',
    'successor_flag_carrier': 'successor',
    'hub_airport': 'partner',
    'interline_partner': 'partner',
    'industry_membership': 'member_of',
    'regulatory_blacklist': 'regulated_by',
    'national_regulator': 'regulator',
    'headquarters_hub': 'other',
    'operating base': 'other',
    'owner': 'controlling_shareholder',
    'predecessor_employer': 'other',
    'sister_project': 'sibling',
    'news_source': 'other',
    'award_grantor': 'other',
    'predecessor agency': 'predecessor',
    'successor agency': 'successor',
    'daughter_company': 'subsidiary',
    'branch': 'subsidiary',
    'subordinate': 'subsidiary',
    'regulator (national)': 'regulator',
    'avention_partner': 'partner',
    'alliance_partner': 'strategic_alliance',
    'supplier_partner': 'supplier',
    'business_partner': 'partner',
    'customer_partner': 'customer',
    'sister_company': 'sibling',
    'parent_state': 'parent_org',
    'parent_ministry': 'parent_org',
    'sub_brand': 'subsidiary',
}

IND_MAP = {
    'research': 'research_development',
    'vocational_education': 'education',
    'civil_engineering': 'engineering',
    'architecture': 'construction',
    'energy_engineering': 'energy_renewable',
    'seismic_engineering': 'engineering',
    'mobile_network_operator': 'mobile_telecommunications',
    'digital_services': 'software',
    'food_and_beverage': 'food_beverage',
    'airline': 'aviation',
    'low_cost_carrier': 'aviation',
    'passenger_transport': 'public_transport',
    'air_transport': 'aviation',
    'charter_airline': 'aviation',
    'cargo_transport': 'logistics_warehousing',
    'ground_handling_services': 'aviation',
    'flight_inspection_services': 'aviation',
    'digital_wallet_and_fintech': 'fintech',
    'mobile_tv_streaming': 'broadcasting',
    'retail_devices': 'consumer_electronics',
    'retail_banking': 'banking',
    'corporate_banking': 'banking',
    'islamic_banking': 'banking',
    'consumer_lending': 'financial_services',
    'news_media': 'media_publishing',
    'online_media': 'digital_media',
    'news_agency': 'media_publishing',
    'print_media': 'media_publishing',
    'digital_wallet': 'fintech',
    'mobile_telephony': 'mobile_telecommunications',
    'fixed_line': 'telecommunications',
    'isp': 'internet_services',
    'mobile_payments': 'fintech',
    'digital_banking': 'banking',
    'investment_banking': 'banking',
    'microfinance': 'financial_services',
    'leasing': 'financial_services',
    'factoring': 'financial_services',
    'trade_finance': 'trade_finance',
    'payment_system': 'payment_services',
    'money_transfer': 'payment_services',
    'currency_exchange': 'financial_services',
    'savings_bank': 'banking',
    'state_bank': 'banking',
    'commercial_bank': 'banking',
    'development_bank': 'banking',
    'mortgage_lending': 'financial_services',
    'agricultural_bank': 'banking',
    'private_banking': 'banking',
    'corporate_finance': 'financial_services',
    'wealth_management': 'asset_management',
    'asset_custody': 'asset_management',
    'pension_fund': 'asset_management',
    'mutual_fund': 'asset_management',
    'insurance_life': 'insurance',
    'insurance_nonlife': 'insurance',
    'insurance_reinsurance': 'insurance',
    'insurance_brokerage': 'insurance',
    'retail_pharmacy': 'pharmaceuticals',
    'pharmaceutical_distribution': 'pharmaceuticals',
    'pharmaceutical_manufacturing': 'pharmaceuticals',
    'medical_devices': 'healthcare',
    'hospital_services': 'healthcare',
    'clinic_services': 'healthcare',
    'oil_refining': 'energy_oil_gas',
    'oil_extraction': 'energy_oil_gas',
    'gas_distribution': 'energy_oil_gas',
    'electricity_generation': 'electricity_gas',
    'electricity_distribution': 'electricity_gas',
    'heat_generation': 'electricity_gas',
    'coal_mining': 'mining',
    'gold_mining': 'metal_mining',
    'uranium_mining': 'mining',
    'rare_earth_mining': 'mining',
    'iron_ore_mining': 'metal_mining',
    'copper_mining': 'metal_mining',
    'construction_materials': 'construction',
    'cement': 'construction',
    'concrete': 'construction',
    'residential_construction': 'construction',
    'commercial_construction': 'construction',
    'infrastructure_construction': 'construction',
    'road_construction': 'construction',
    'civil_construction': 'construction',
    'railway_construction': 'construction',
    'water_supply': 'water',
    'wastewater': 'water',
    'irrigation': 'agriculture_food',
    'agricultural_production': 'agriculture_food',
    'livestock': 'agriculture_food',
    'dairy': 'food_beverage',
    'meat_processing': 'food_beverage',
    'flour_milling': 'food_beverage',
    'bakery': 'food_beverage',
    'beverage_production': 'food_beverage',
    'tobacco_production': 'tobacco',
    'cotton_processing': 'textiles_apparel',
    'garment_manufacturing': 'textiles_apparel',
    'textile_manufacturing': 'textiles_apparel',
    'wool_processing': 'textiles_apparel',
    'leather_goods': 'textiles_apparel',
    'it_services': 'information_technology',
    'software_development': 'software',
    'saas': 'software',
    'cloud_services': 'cloud_computing',
    'data_center': 'cloud_computing',
    'cybersecurity_services': 'cybersecurity',
    'ecommerce_platform': 'ecommerce',
    'online_retail': 'ecommerce',
    'marketplace': 'ecommerce',
    'digital_advertising': 'digital_media',
    'content_creation': 'digital_media',
    'streaming_services': 'broadcasting',
    'tv_broadcasting': 'broadcasting',
    'radio_broadcasting': 'broadcasting',
    'print_publishing': 'media_publishing',
    'book_publishing': 'media_publishing',
    'newspaper': 'media_publishing',
    'magazine': 'media_publishing',
    'news_website': 'digital_media',
    'logistics': 'logistics_warehousing',
    'freight_forwarding': 'logistics_warehousing',
    'courier_services': 'logistics_warehousing',
    'warehouse': 'logistics_warehousing',
    'customs_brokerage': 'logistics_warehousing',
    'shipping': 'maritime_shipping',
    'port_services': 'port_operations',
    'road_transport': 'transportation',
    'rail_transport': 'railway',
    'urban_transport': 'public_transport',
    'taxi_services': 'public_transport',
    'bus_services': 'public_transport',
    'aviation_services': 'aviation',
    'airport_services': 'aviation',
    'air_traffic_control': 'aviation',
    'hotel': 'hospitality_tourism',
    'resort': 'hospitality_tourism',
    'travel_agency': 'tourism',
    'tour_operator': 'tourism',
    'restaurant': 'food_beverage',
    'cafe': 'food_beverage',
    'real_estate_development': 'real_estate',
    'property_management': 'real_estate',
    'real_estate_brokerage': 'real_estate',
    'rental_services': 'real_estate',
    'legal_services_': 'legal_services',
    'audit_services': 'professional_services',
    'accounting': 'professional_services',
    'consulting_services': 'consulting',
    'engineering_consulting': 'consulting',
    'management_consulting': 'consulting',
    'hr_services': 'professional_services',
    'marketing_services': 'professional_services',
    'advertising': 'professional_services',
    'design_services': 'professional_services',
    'education_services': 'education',
    'higher_education_': 'higher_education',
    'vocational_training': 'education',
    'language_training': 'education',
    'test_preparation': 'education',
    'tutoring': 'education',
    'educational_technology': 'education',
    'research_institute': 'research_development',
    'scientific_research': 'research_development',
    'applied_research': 'research_development',
    'sports_administration': 'sports',
    'sports_promotion': 'sports',
    'fitness': 'sports',
    'cultural_promotion': 'public_administration',
    'cultural_heritage_': 'public_administration',
    'religious_affairs_administration': 'public_administration',
    'youth_policy': 'public_administration',
    'veterans_services': 'public_administration',
    'disaster_management': 'public_administration',
    'civil_defense_': 'public_administration',
    'emergency_services': 'public_administration',
    'border_protection': 'internal_security',
    'customs_administration': 'public_administration',
    'migration_services': 'public_administration',
    'tax_administration': 'public_administration',
    'public_procurement': 'public_administration',
    'national_security': 'intelligence_security',
    'state_security': 'intelligence_security',
    'military_forces': 'defence_military',
    'armed_forces': 'defence_military',
    'national_guard': 'defence_military',
    'border_troops': 'defence_military',
    'air_defense': 'defence_military',
    'air_force': 'defence_military',
    'navy': 'defence_military',
    'land_forces': 'defence_military',
    'special_forces': 'defence_military',
    'military_education': 'defence_military',
    'military_industrial': 'weapons_armaments',
    'weapons_production': 'weapons_armaments',
    'ammunition_production': 'weapons_armaments',
    'parliament': 'legislative',
    'government_administration': 'public_administration',
    'executive_branch': 'public_administration',
    'judicial_administration': 'judicial',
    'prosecution': 'judicial',
    'legal_affairs': 'legal_services',
    'foreign_ministry': 'foreign_affairs',
    'diplomatic_services': 'foreign_affairs',
    'consular_services': 'foreign_affairs',
    'trade_representation': 'international_trade',
    'international_cooperation': 'foreign_affairs',
    'european_integration': 'foreign_affairs',
    'un_representation': 'foreign_affairs',
    'international_organizations': 'foreign_affairs',
    'eaeu_affairs': 'foreign_affairs',
    'sco_affairs': 'foreign_affairs',
    'csto_affairs': 'foreign_affairs',
    'cis_affairs': 'foreign_affairs',
    'ots_affairs': 'foreign_affairs',
    'central_bank': 'monetary_policy',
    'monetary_authority': 'monetary_policy',
    'financial_regulator': 'regulatory',
    'financial_regulation': 'regulatory',
    'banking_regulation': 'regulatory',
    'insurance_regulation': 'regulatory',
    'securities_regulation': 'regulatory',
    'competition_regulation': 'regulatory',
    'consumer_protection': 'regulatory',
    'data_protection_': 'regulatory',
    'environmental_regulation': 'regulatory',
    'technical_regulation': 'regulatory',
    'anti_monopoly': 'regulatory',
    'statistics': 'regulatory',
    'intellectual_property': 'regulatory',
    'customs_regulation': 'regulatory',
    'tax_regulation': 'regulatory',
    'financial_intelligence': 'regulatory',
    'anti_corruption': 'regulatory',
    'accounting_regulation': 'regulatory',
    'audit_regulation': 'regulatory',
    'civil_service_': 'civil_service',
    'personnel_policy': 'civil_service',
    'administrative_reform': 'civil_service',
    'party_political': 'political_party',
    'political_organization': 'political_party',
    'trade_union': 'social_services',
    'professional_association': 'professional_services',
    'chamber_of_commerce': 'professional_services',
    'employers_association': 'professional_services',
    'women_organization': 'social_services',
    'youth_organization': 'social_services',
    'civil_society': 'social_services',
    'human_rights': 'social_services',
    'environmental_protection': 'sustainability',
    'environmental_advocacy': 'sustainability',
    'social_protection': 'social_services',
    'child_protection': 'social_services',
    'disability_rights': 'social_services',
    'consumer_rights': 'social_services',
    'transparency_advocacy': 'social_services',
    'anti_corruption_advocacy': 'social_services',
    'election_observation': 'social_services',
    'free_media_advocacy': 'social_services',
    'religious_education': 'education',
    'islamic_finance_': 'financial_services',
    'motor_transport': 'transportation',
    'pipeline_transport': 'transportation',
    'aircraft_manufacturing': 'aerospace_defense',
    'aerospace_manufacturing': 'aerospace_defense',
    'space_research': 'space',
    'satellite_communications': 'space',
    'petrochemicals_': 'petrochemicals',
    'chemical_manufacturing': 'chemicals',
    'fertilizer_production': 'chemicals',
    'plastics_production': 'chemicals',
    'steel_making': 'steel',
    'steel_distribution': 'steel',
    'renewable_energy': 'energy_renewable',
    'solar_energy': 'energy_renewable',
    'wind_energy': 'energy_renewable',
    'hydro_energy': 'energy_renewable',
    'small_hydro': 'energy_renewable',
    'bioenergy': 'energy_renewable',
    'geothermal_energy': 'energy_renewable',
    'oil_storage': 'energy_oil_gas',
    'gas_storage': 'energy_oil_gas',
    'oil_transport': 'energy_oil_gas',
    'gas_transport': 'energy_oil_gas',
    'lectricity_transmission': 'electricity_gas',
    'power_engineering': 'electricity_gas',
    'power_equipment': 'electricity_gas',
    'metrology': 'regulatory',
    'standardization': 'regulatory',
    'accreditation': 'regulatory',
    'market_surveillance': 'regulatory',
    'technical_inspection': 'regulatory',
    'industrial_safety': 'regulatory',
    'nuclear_safety': 'regulatory',
    'radiation_safety': 'regulatory',
    'mining_technical_inspection': 'regulatory',
    'vector_control': 'public_health',
    'epidemiology': 'public_health',
    'sanitary_inspection': 'public_health',
    'quarantine': 'public_health',
    'pharmacovigilance': 'public_health',
    'medical_education': 'healthcare',
    'veterinary': 'agriculture_food',
    'phytosanitary': 'agriculture_food',
    'plant_protection': 'agriculture_food',
    'agricultural_research': 'research_development',
    'veterinary_medicine': 'agriculture_food',
    'agricultural_insurance': 'insurance',
    'agricultural_subsidies': 'public_administration',
    'land_management': 'public_administration',
    'cadastre': 'public_administration',
    'mapping': 'public_administration',
    'geodesy': 'public_administration',
    'cartography': 'public_administration',
    'state_property': 'public_administration',
    'privatization': 'public_administration',
    'state_procurement': 'public_administration',
    'confiscated_property': 'public_administration',
    'bankruptcy': 'judicial',
    'bailiff': 'judicial',
    'notary': 'legal_services',
    'advocacy': 'legal_services',
    'medation': 'legal_services',
    'arbitration': 'legal_services',
    'court_administration': 'judicial',
    'enforcement': 'judicial',
    'correctional_services': 'judicial',
    'probation': 'judicial',
    'forensics': 'judicial',
    'criminal_investigation': 'internal_security',
    'police_services': 'internal_security',
    'public_order': 'internal_security',
    'traffic_police': 'internal_security',
    'drug_control': 'internal_security',
    'organized_crime': 'internal_security',
    'cybercrime': 'cybersecurity',
    'economic_crime': 'internal_security',
    'corruption_investigation': 'internal_security',
    'migration_control': 'internal_security',
    'passport_services': 'public_administration',
    'civil_registry': 'public_administration',
    'visa_services': 'public_administration',
    'asylum': 'public_administration',
    'refugees': 'social_services',
    'stateless_persons': 'public_administration',
    'consular_affairs': 'foreign_affairs',
    'international_treaties': 'foreign_affairs',
    'international_law': 'foreign_affairs',
    'diplomatic_protocol': 'foreign_affairs',
    'state_visits': 'foreign_affairs',
    'summitry': 'foreign_affairs',
    'international_development': 'humanitarian_aid',
    'technical_assistance': 'humanitarian_aid',
    'humanitarian_assistance': 'humanitarian_aid',
    'disaster_relief': 'humanitarian_aid',
    'refugee_assistance': 'humanitarian_aid',
    ' poverty_reduction': 'social_services',
    'social_inclusion': 'social_services',
    'gender_equality': 'social_services',
    'women_empowerment': 'social_services',
    'child_rights': 'social_services',
    'education_for_all': 'education',
    'health_for_all': 'public_health',
    'hiv_aids': 'public_health',
    'malaria': 'public_health',
    'tuberculosis': 'public_health',
    'covid_19': 'public_health',
    'immunization': 'public_health',
    'maternal_health': 'public_health',
    'reproductive_health': 'public_health',
    'nutrition': 'public_health',
    'mental_health': 'public_health',
    'substance_abuse': 'public_health',
    'non_communicable_diseases': 'public_health',
    'occupational_health': 'public_health',
    'environmental_health': 'public_health',
    'water_sanitation': 'water',
    'hygiene': 'water',
    'solid_waste': 'environmental_services',
    'hazardous_waste': 'environmental_services',
    'medical_waste': 'environmental_services',
    'electronic_waste': 'environmental_services',
    'air_pollution': 'environmental_services',
    'water_pollution': 'environmental_services',
    'soil_pollution': 'environmental_services',
    'noise_pollution': 'environmental_services',
    'climate_change': 'sustainability',
    'biodiversity': 'sustainability',
    'desertification': 'sustainability',
    'deforestation': 'sustainability',
    'reforestation': 'sustainability',
    'national_parks': 'sustainability',
    'protected_areas': 'sustainability',
    'wildlife': 'sustainability',
    'endangered_species': 'sustainability',
    'invasive_species': 'sustainability',
    'genetic_resources': 'sustainability',
    'biosafety': 'sustainability',
    'biotechnology_': 'biotechnology',
    'genetic_engineering': 'biotechnology',
    'gene_editing': 'biotechnology',
    'synthetic_biology': 'biotechnology',
    'bioinformatics': 'biotechnology',
    'biomedical': 'biotechnology',
    'biopharmaceuticals': 'biotechnology',
    'biomanufacturing': 'biotechnology',
    'industrial_biotechnology': 'biotechnology',
    'environmental_biotechnology': 'biotechnology',
    'marine_biotechnology': 'biotechnology',
    'agricultural_biotechnology': 'biotechnology',
}

def fix_industry(v):
    if v in IND_MAP:
        return IND_MAP[v]
    # try without common variations
    key = v.strip().lower().replace(' ', '_')
    if key in IND_MAP:
        return IND_MAP[key]
    return None

def fix_rt(v):
    if v in RT_MAP:
        return RT_MAP[v]
    key = v.strip().lower()
    if key in RT_MAP:
        return RT_MAP[key]
    return None

def fix_apec_stance(v):
    if isinstance(v, str) or v is None:
        return v
    if isinstance(v, dict):
        # Prefer notes, then affiliation, then summary
        for k in ('notes', 'note', 'summary', 'summary_zh', 'description', 'comment', 'comments'):
            if v.get(k):
                return v[k]
        # Combine
        parts = []
        for k, val in v.items():
            if val and isinstance(val, str):
                parts.append(f"{k}: {val}")
        return '; '.join(parts) if parts else None
    return str(v)

def fix_core_business(v):
    if isinstance(v, str) or v is None:
        return v
    if isinstance(v, dict):
        for k in ('summary_zh', 'summary', 'description', 'overview', 'core_business_zh'):
            if v.get(k):
                return v[k]
        # Combine
        parts = []
        for k, val in v.items():
            if val and isinstance(val, str):
                parts.append(val if k in ('summary_zh', 'summary') else f"{k}: {val}")
            elif isinstance(val, list):
                parts.append(f"{k}: {', '.join(str(x) for x in val)}")
        return '; '.join(parts) if parts else None
    return str(v)

def fix_social_accounts(v):
    """If social_accounts is a dict (instead of list), convert to list of dicts."""
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        out = []
        for platform, url in v.items():
            if not url or not isinstance(url, str):
                continue
            # Skip non-platform metadata keys
            base = platform.split('_')[0].lower()
            if base in ('website', 'source', 'notes', 'note', 'description', 'comment'):
                # If it's website - add as platform=website
                if base == 'website' and url:
                    out.append({
                        'platform': 'website',
                        'account_name': None,
                        'url': url,
                        'source': 'official_website'
                    })
                continue
            out.append({
                'platform': base,
                'account_name': None,
                'url': url,
                'source': 'official_website'
            })
        return out
    return v

# Now process all KG org files
files = sorted(glob.glob('output/kg/2026-06-21/orgs/*.json'))
total_fixes = 0
unmapped_ind = set()
unmapped_rt = set()
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    pid = os.path.basename(f).replace('.json', '')
    changed = False
    # Fix relationship_type
    for i, item in enumerate(d.get('related_entities', [])):
        rt = item.get('relationship_type', '')
        if rt and rt not in {'parent_org','subsidiary','controlling_shareholder','minority_shareholder','sibling','partner','regulator','regulated_by','member_of','predecessor','successor','affiliated','supplier','customer','strategic_alliance'}:
            new = fix_rt(rt)
            if new:
                item['relationship_type'] = new
                changed = True
            else:
                unmapped_rt.add(rt)
                item['relationship_type'] = 'other'  # fallback
                changed = True
    # Fix industries
    new_ind = []
    for ind in d.get('industries', []):
        if ind in {'aerospace_defense','agriculture_food','asset_management','automotive','aviation','banking','biotechnology','broadcasting','chemicals','civil_service','cloud_computing','construction','consulting','consumer_electronics','cryptocurrency_digital_assets','cybersecurity','defence_military','digital_media','ecommerce','education','electricity_gas','electronic_components','energy_oil_gas','energy_renewable','engineering','environmental_services','financial_services','fintech','fisheries_aquaculture','food_beverage','foreign_affairs','forestry_timber','gaming','healthcare','higher_education','hospitality_tourism','humanitarian_aid','industrial_manufacturing','information_technology','infrastructure','insurance','intelligence_security','internal_security','international_trade','internet_services','investment','judicial','legal_services','legislative','logistics_warehousing','maritime_shipping','media_publishing','metal_mining','microelectronics','mining','mobile_telecommunications','monetary_policy','nonprofit','nuclear_energy','payment_services','petrochemicals','pharmaceuticals','port_operations','professional_services','public_administration','public_health','public_transport','railway','real_estate','regulatory','research_development','retail','robotics','semiconductors','social_services','software','space','sports','steel','supply_chain','surveillance','sustainability','telecommunications','textiles_apparel','think_tank','tobacco','tourism','trade_finance','transportation','urban_planning','utilities','venture_capital','water','weapons_armaments'}:
            new_ind.append(ind)
        else:
            new = fix_industry(ind)
            if new:
                new_ind.append(new)
                changed = True
            else:
                unmapped_ind.add(ind)
    if new_ind != d.get('industries', []):
        d['industries'] = new_ind
    # Fix apec_stance dict
    if not isinstance(d.get('apec_stance'), (str, type(None))):
        d['apec_stance'] = fix_apec_stance(d.get('apec_stance'))
        changed = True
    # Fix core_business dict
    if not isinstance(d.get('core_business'), (str, type(None))):
        d['core_business'] = fix_core_business(d.get('core_business'))
        changed = True
    # Fix social_accounts dict
    if not isinstance(d.get('social_accounts'), list):
        d['social_accounts'] = fix_social_accounts(d.get('social_accounts'))
        changed = True
    if changed:
        # Atomic write
        tmp = f + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as out:
            json.dump(d, out, ensure_ascii=False, indent=2)
        os.replace(tmp, f)
        total_fixes += 1

print(f'Fixed {total_fixes} files')
print(f'Unmapped industries: {sorted(unmapped_ind)[:50]}')
print(f'Total unmapped industries count: {len(unmapped_ind)}')
print(f'Unmapped relationship_types: {sorted(unmapped_rt)}')
