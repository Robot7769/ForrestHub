---
title: Propojení
---

Systém ForrestHub je navržen tak, aby byl hrán na více zařízeních.
Hra se spustí na jednom počítači, který slouží jako server.
Podmínkou je, že všechna zařízení jsou připojena do stejné Wi-Fi sítě.

Níže je zobrazen graf, který znázorňuje propojení serveru s jednotlivými zařízeními.

```mermaid
graph TB
    Server((Server))

%% Zařízení připojená k serveru ze všech směrů
    PC1[Počítač 1]
    PC2[Počítač 2]
    Phone1[Telefon 1]
    Phone2[Telefon 2]
    Tablet1[Tablet 1]
    Tablet2[Tablet 2]

%% Spojení serveru se zařízeními
    Server --> PC1
    Server --> Phone1
    Server --> Tablet1
    Server --> PC2
    Server --> Phone2
    Server --> Tablet2

%% Stylování uzlů s pastelovými barvami
    style Server fill:#A8D5BA,stroke:#333,stroke-width:2px,color:#333
    style PC1 fill:#FFD6A5,stroke:#333,stroke-width:1px,color:#333
    style PC2 fill:#FFABAB,stroke:#333,stroke-width:1px,color:#333
    style Phone1 fill:#FFC3A0,stroke:#333,stroke-width:1px,color:#333
    style Phone2 fill:#FF677D,stroke:#333,stroke-width:1px,color:#333
    style Tablet1 fill:#D4A5A5,stroke:#333,stroke-width:1px,color:#333
    style Tablet2 fill:#A9DEF9,stroke:#333,stroke-width:1px,color:#333

```