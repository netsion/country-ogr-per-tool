# Singapore Organization Knowledge Graph

## State Power Structure (国家权力架构)

```mermaid
graph TD
    subgraph "Head of State 国家元首"
        PRES[President 总统]
    end

    subgraph "Executive 行政机关"
        CAB[Cabinet 内阁]
        PMO[PMO 总理公署]
        MOF[MOF 财政部]
        MINDEF[MINDEF 国防部]
        MFA[MFA 外交部]
        MHA[MHA 内政部]
        MOE[MOE 教育部]
        MOH[MOH 卫生部]
        MTI[MTI 贸工部]
        MOT[MOT 交通部]
        MND[MND 国家发展部]
        MOM[MOM 人力部]
        MINLAW[MINLAW 律政部]
        MCCY[MCCY 文化部]
        MDDI[MDDI 数码部]
        MSF[MSF 社会部]
        MSE[MSE 环境部]
    end

    subgraph "Legislature 立法机关"
        PARL[Parliament 国会]
    end

    subgraph "Judiciary 司法机关"
        SC[Supreme Court 最高法院]
        STC[State Courts 国家法院]
        FJC[Family Justice Courts 家事法院]
    end

    subgraph "Independent Organs 独立机关"
        AGC[AGC 总检察署]
        AGO[AGO 审计总署]
        PSC[PSC 公共服务委员会]
    end

    PRES -->|任命| CAB
    CAB --> PMO
    CAB --> MOF
    CAB --> MINDEF
    CAB --> MFA
    CAB --> MHA
    CAB --> MOE
    CAB --> MOH
    CAB --> MTI
    CAB --> MOT
    CAB --> MND
    CAB --> MOM
    CAB --> MINLAW
    CAB --> MCCY
    CAB --> MDDI
    CAB --> MSF
    CAB --> MSE
    SC -->|上诉管辖| STC
    SC -->|上诉管辖| FJC
```

## Government & SOE Hierarchy

```mermaid
graph TD
    GOV000[Government of Singapore] --> SOE001[Temasek Holdings]
    GOV000 --> SOE005[GIC]
    GOV000 --> GOV001[MAS]
    GOV000 --> GOV002[EDB]
    GOV000 --> GOV003[ACRA]
    GOV000 --> GOV005[HDB]
    GOV000 --> GOV006[CPF]
    GOV000 --> GOV007[IMDA]
    GOV000 --> GOV010[GovTech]

    SOE001 --> SOE002[Singtel]
    SOE001 --> SOE003[Singapore Airlines]
    SOE001 --> SOE004[PSA International]
    SOE001 --> SOE006[SMRT]
    SOE001 --> SOE007[Mediacorp]
    SOE001 --> SOE008[CapitaLand]
    SOE001 --> SOE009[Surbana Jurong]
```

## Military & Security Structure

```mermaid
graph TD
    MIL001[MINDEF] --> MIL002[Singapore Armed Forces]
    MIL001 --> MIL005[MSD]
    MIL001 --> MIL006[DSTA]
    MIL002 --> MIL002A[Singapore Army]
    MIL002 --> MIL002B[Republic of Singapore Navy]
    MIL002 --> MIL002C[Republic of Singapore Air Force]
    MIL002 --> MIL003[Digital and Intelligence Service]
    MIL003 --> MIL003A[Defence Cyber Command]
    MIL003 --> MIL003B[SAF C4 Command]
    GOV000[Government] --> MIL004[ISD - Internal Security]
```

## Financial & Corporate Sector

```mermaid
graph TD
    FIN001[DBS Bank] --> FIN001H[DBS Group Holdings]
    FIN002[OCBC Bank]
    FIN003[UOB]
    CORP001[Sea Limited] --> CORP001A[Garena]
    CORP001 --> CORP001B[Shopee]
    CORP001 --> CORP001C[Monee]
    CORP002[Grab Holdings]
    CORP003[Wilmar International]
    CORP004[Olam Group]
```

## Media Ecosystem

```mermaid
graph TD
    SOE007[Mediacorp] --> MEDIA002[CNA]
    SOE007 --> MEDIA002B[Channel 5/8]
    MEDIA001[SPH Media] --> MEDIA003[The Straits Times]
    MEDIA001 --> MEDIA004[Lianhe Zaobao]
    MEDIA001 --> MEDIA005[TODAY]
    MEDIA001 --> MEDIA006[The Business Times]
```

## Academic & Research

```mermaid
graph TD
    ACAD001[NUS] --> ACAD001A[NUS Press]
    ACAD002[NTU]
    ACAD003[SMU]
    ACAD004[SUTD]
    ACAD005[SIT]
    ACAD006[A*STAR]
    ACAD007[RSIS]
```

## Legend

| Category | Color |
|----------|-------|
| GOV - Government | Blue |
| SOE - State-Owned Enterprise | Green |
| CORP - Corporate | Orange |
| FIN - Financial | Gold |
| ACAD - Academic | Purple |
| MEDIA - Media | Red |
| MIL - Military | Dark Gray |
| NGO - Non-Government | Teal |
| INTL - International | Cyan |
| PARTY - Political Party | Brown |
