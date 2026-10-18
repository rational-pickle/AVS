from lib import *

# ================================================================ PERFORMANCE
add("div-perform", "perform", ("Performance and benchmarks", "Performance et bancs d'essai"),
    tb("p", "Prove it on your own workloads, with a fair and repeatable test.",
       "Prouvez-le sur vos propres charges, avec un test équitable et reproductible.", "promise"),
    notes("30 s",
          [("Performance conversations go better with data than with adjectives. This section shows what the hardware is, how to measure fairly, and how to predict migration speed.",
            "Les discussions sur la performance vont mieux avec des données qu'avec des adjectifs. Cette section montre le matériel, comment mesurer équitablement et comment prévoir la vitesse de migration.")],
          trans=("The short version.", "La version courte.")),
    kind="divider")

ex = panel("Executive summary", "Sommaire pour la direction", ul([
    ("AV64 hosts are current generation: <b>64 cores, 1&nbsp;TB RAM, all-NVMe vSAN ESA, 100&nbsp;Gbps</b> networking.",
     "Les hôtes AV64 sont de génération actuelle&nbsp;: <b>64 cœurs, 1&nbsp;To de RAM, vSAN ESA tout NVMe, réseau 100&nbsp;Gb/s</b>."),
    ("Run a <b>short, fair benchmark on your own workloads</b> before the first production wave: results you can defend.",
     "Faites un <b>banc d'essai court et équitable sur vos propres charges</b> avant la première vague de production&nbsp;: des résultats défendables."),
    ("Migration speed is <b>predictable</b>: bandwidth, HCX appliance capacity and storage set it, and simple math plans it.",
     "La vitesse de migration est <b>prévisible</b>&nbsp;: la bande passante, la capacité des appliances HCX et le stockage la déterminent, et un calcul simple la planifie."),
], "big"), "p-exec")
el = panel("ELI5", "En termes simples", tb("p",
    "A fair race uses the same runner, on the same track, with the same stopwatch. Benchmark the same VM, with the same test and the same settings, on your current platform and on AVS. Then compare the times.",
    "Une course équitable utilise le même coureur, sur la même piste, avec le même chronomètre. Testez la même VM, avec le même test et les mêmes réglages, sur votre plateforme actuelle et sur AVS. Puis comparez les temps.", "eli5-text"), "p-eli5")
add("perf-exec", "perform", ("Performance, in plain terms", "La performance, simplement"),
    f'<div class="grid g-55-45">{ex}{el}</div>',
    notes("2 min",
          [("For most estates, AV64 hosts are newer than the hardware being replaced, so the usual outcome is equal or better performance. But we do not ask you to take that on faith.",
            "Pour la plupart des parcs, les hôtes AV64 sont plus récents que le matériel remplacé; le résultat habituel est donc une performance égale ou meilleure. Mais nous ne vous demandons pas de nous croire sur parole."),
           ("We propose a short benchmark on two or three of your representative workloads during the pilot, with the method agreed upfront.",
            "Nous proposons un court banc d'essai sur deux ou trois de vos charges représentatives pendant le pilote, avec une méthode convenue d'avance.")],
          trans=("First, what is inside each host and how to size the cluster.", "D'abord, ce que contient chaque hôte et comment dimensionner la grappe.")),
    layer="exec")

spec = panel("AV64 host", "Hôte AV64", table(
    [("Component", "Composant"), ("Specification", "Spécification")],
    [
        [("CPU", "Processeur"), ("2 × Intel Xeon Platinum 8370C (Ice Lake), 32 cores each at 2.8&nbsp;GHz: 64 cores, 128 threads", "2 × Intel Xeon Platinum 8370C (Ice Lake), 32 cœurs chacun à 2,8&nbsp;GHz&nbsp;: 64 cœurs, 128 fils")],
        [("Memory", "Mémoire"), ("1,024 GB", "1&nbsp;024&nbsp;Go")],
        [("Storage", "Stockage"), ("vSAN ESA, 19.25&nbsp;TB raw NVMe per host (Gen 2)", "vSAN ESA, 19,25&nbsp;To NVMe brut par hôte (Gen 2)")],
        [("Network", "Réseau"), ("100 Gbps", "100&nbsp;Gb/s")],
        [("Scale", "Échelle"), ("3 to 16 hosts per cluster; 12 clusters and 96 hosts per private cloud", "3 à 16 hôtes par grappe; 12 grappes et 96 hôtes par nuage privé")],
    ], "tbl tbl-sm", colw=["28%", "72%"]), "p-deep")
pol = panel("vSAN policy and usable capacity", "Stratégie vSAN et capacité utilisable", table(
    [("Policy", "Stratégie"), ("Minimum hosts", "Hôtes minimum")],
    [["RAID-1, FTT 1", "3"], ["RAID-5, FTT 1", "4"], ["RAID-1, FTT 2", "5"], ["RAID-6, FTT 2", "6"], ["RAID-1, FTT 3", "7"]],
    "tbl tbl-sm", colw=["60%", "40%"])
    + '<div class="calc">' + t("Example: 4 hosts × 19.25&nbsp;TB = 77&nbsp;TB raw → RAID-1 FTT&nbsp;1 halves it: 38.5&nbsp;TB → keep 25% free: <b>about 29&nbsp;TB for VMs</b>, before compression and management overhead.",
                               "Exemple&nbsp;: 4 hôtes × 19,25&nbsp;To = 77&nbsp;To brut → RAID-1 FTT&nbsp;1 divise par deux&nbsp;: 38,5&nbsp;To → garder 25&nbsp;% libre&nbsp;: <b>environ 29&nbsp;To pour les VM</b>, avant compression et surcoût de gestion.") + '</div>', "p-deep")
meth = panel("Sizing method", "Méthode de dimensionnement", ul([
    ("Azure Migrate AVS assessment, performance-based on CPU and memory use.", "Évaluation AVS d'Azure Migrate, basée sur l'utilisation réelle du processeur et de la mémoire."),
    ("The first cluster also hosts management: vCenter, NSX, HCX.", "La première grappe héberge aussi la gestion&nbsp;: vCenter, NSX, HCX."),
    ("N+1 HA: one host's worth of capacity is held in reserve.", "HA N+1&nbsp;: l'équivalent d'un hôte est gardé en réserve."),
    ("Prefer 4+ hosts: maintenance resilience and more Gen 2 route capacity.", "Privilégiez 4 hôtes ou plus&nbsp;: résilience en maintenance et plus de capacité de routage Gen 2."),
], "dense"), "p-deep")
add("sizing", "perform", ("AV64 host and sizing essentials", "Hôte AV64 et dimensionnement&nbsp;: l'essentiel"),
    f'<div class="grid g-36-34-30">{spec}{pol}{meth}</div>'
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/architecture-private-clouds#hosts", "Host types and limits", "Types d'hôtes et limites"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/introduction#av64-supported-raid-configuration", "AV64 RAID policies", "Stratégies RAID AV64")),
    notes("3 min",
          [("One host type in Gen 2: AV64. 64 physical cores, a terabyte of memory, about 19 terabytes of raw NVMe in vSAN ESA, and 100 gigabit networking.",
            "Un seul type d'hôte dans Gen 2&nbsp;: AV64. 64 cœurs physiques, un téraoctet de mémoire, environ 19 téraoctets de NVMe brut dans vSAN ESA et un réseau de 100 gigabits."),
           ("Walk the example: raw capacity is not usable capacity. Mirroring halves it, and the 25 percent free-space rule takes another quarter. That is why storage often decides the host count, and why Azure NetApp Files datastores can save hosts.",
            "Parcourez l'exemple&nbsp;: la capacité brute n'est pas la capacité utilisable. Le miroir la divise par deux, et la règle des 25&nbsp;% d'espace libre en retire encore un quart. C'est pourquoi le stockage décide souvent du nombre d'hôtes, et pourquoi les banques Azure NetApp Files peuvent économiser des hôtes."),
           ("Large VMs: each socket has 32 cores, so keep VMs within one NUMA node where you can.",
            "Grosses VM&nbsp;: chaque socket compte 32 cœurs; gardez les VM dans un seul nœud NUMA quand c'est possible.")],
          qa=[(("Can we overcommit CPU like we do today?", "Pouvons-nous surallouer le processeur comme aujourd'hui?"),
               ("Yes, it is vSphere. Agree on a target vCPU-to-core ratio from your current metrics, and avoid memory overcommit for production.",
                "Oui, c'est vSphere. Convenez d'un ratio cible de vCPU par cœur à partir de vos métriques actuelles, et évitez la surallocation de mémoire en production."))],
          trans=("Now, how to compare performance fairly.", "Voyons maintenant comment comparer la performance équitablement.")),
    layer="deep", skip=True)

u = "bench"
d = ""
stepsb = [
    (("Baseline today", "Mesurer aujourd'hui"), (["Same VMs, at peak;", "latency, IOPS, CPU ready"], ["Mêmes VM, en pointe;", "latence, IOPS, CPU ready"])),
    (("Test on AVS", "Tester sur AVS"), (["Same size, policy, tool;", "warm up; 3+ runs"], ["Même taille, stratégie, outil;", "réchauffage; 3+ essais"])),
    (("Compare", "Comparer"), (["p95 latency, throughput,", "transaction time"], ["Latence p95, débit,", "temps de transaction"])),
    (("Report", "Présenter"), (["Side-by-side table with", "conditions and cost"], ["Tableau comparatif avec", "conditions et coût"])),
]
for i, (h, s) in enumerate(stepsb):
    x = 10 + i * 355
    d += f'<circle cx="{x + 24}" cy="40" r="20" class="dot"/>' + st(x + 24, 40, str(i + 1), str(i + 1), 17, 700, fill="#FFFFFF")
    d += st(x + 56, 40, h[0], h[1], 21, 700, anchor="start", fill="#0B2545")
    d += rect(x, 72, 320, 96, "bx-soft", 6)
    d += st(x + 160, 120, s[0], s[1], 17.5, 400, fill="#0B2545", lh=23)
    if i < 3:
        d += line(x + 322, 120, x + 352, 120, "ln", "a", u)
benchfig = figure(svg(1440, 178, d, "Four-step benchmark: baseline, test on AVS, compare, report",
                      "Banc d'essai en quatre étapes&nbsp;: mesurer, tester sur AVS, comparer, présenter", uid=u),
                  "Same workload, same settings, both platforms: the only variable is the platform.",
                  "Même charge, mêmes réglages, deux plateformes&nbsp;: la seule variable est la plateforme.", "fig-tight")
tools = table(
    [("Layer", "Niveau"), ("Tools", "Outils"), ("What it proves", "Ce que cela prouve")],
    [
        [("Storage", "Stockage"), ("HCIBench, vSAN performance service", "HCIBench, service de performance vSAN"), ("IOPS and latency under a defined profile", "IOPS et latence selon un profil défini")],
        [("Network", "Réseau"), ("iperf3 between sites and to Azure; HCX Transport Analytics", "iperf3 entre sites et vers Azure; HCX Transport Analytics"), ("Bandwidth, latency, loss on the real path", "Bande passante, latence et perte sur le vrai chemin")],
        [("Application", "Application"), ("HammerDB for SQL; JMeter or k6 for web; your synthetic transactions", "HammerDB pour SQL; JMeter ou k6 pour le Web; vos transactions synthétiques"), ("What users actually feel", "Ce que les utilisateurs ressentent vraiment")],
        [("Platform", "Plateforme"), ("VCF Operations, Azure Monitor", "VCF Operations, Azure Monitor"), ("Before and after, over days", "Avant et après, sur plusieurs jours")],
    ], "tbl tbl-sm", colw=["16%", "46%", "38%"])
brules = panel("Rules for credible results", "Règles pour des résultats crédibles", ul([
    ("Application response time beats synthetic peak IOPS.", "Le temps de réponse applicatif l'emporte sur les IOPS synthétiques de pointe."),
    ("Never benchmark during migrations or vSAN resyncs.", "Ne testez jamais pendant des migrations ou des resynchronisations vSAN."),
    ("Write down VM size, storage policy and tool settings.", "Notez la taille de VM, la stratégie de stockage et les réglages de l'outil."),
    ("Report percentiles, not only averages.", "Présentez des percentiles, pas seulement des moyennes."),
], "dense"), "p-deep")
add("benchmark", "perform", ("A fair benchmark in four steps", "Un banc d'essai équitable en quatre étapes"),
    benchfig + f'<div class="grid g-62-38">{tools}{brules}</div>'
    + refs(("https://techdocs.broadcom.com/us/en/vmware-cis/hcx/vmware-hcx/4-10/vmware-hcx-user-guide-4-10/preparing-for-hcx-installations/network-underlay-minimum-requirements.html", "HCX underlay minimums", "Minimums HCX du réseau sous-jacent")),
    notes("3 min",
          [("The method is what makes results credible. Same VM, same size, same storage policy, same tool and parameters, on both platforms.",
            "C'est la méthode qui rend les résultats crédibles. Même VM, même taille, même stratégie de stockage, même outil et mêmes paramètres, sur les deux plateformes."),
           ("Use HCIBench for vSAN, iperf3 for the network, and, most important, an application-level test, because that is what your users feel.",
            "Utilisez HCIBench pour vSAN, iperf3 pour le réseau et, surtout, un test au niveau applicatif, parce que c'est ce que vos utilisateurs ressentent."),
           ("Report the 95th percentile latency, not just averages; averages hide the spikes people complain about.",
            "Présentez la latence au 95e percentile, pas seulement les moyennes; les moyennes cachent les pics dont les gens se plaignent.")],
          qa=[(("Can you benchmark before we commit?", "Pouvez-vous faire un banc d'essai avant notre engagement?"),
               ("Yes, the pilot is designed for exactly that: a small private cloud, two or three representative workloads, and an agreed report format.",
                "Oui, le pilote est conçu pour cela&nbsp;: un petit nuage privé, deux ou trois charges représentatives et un format de rapport convenu."))],
          trans=("And now the number everybody wants: how fast can we migrate?", "Et maintenant le chiffre que tout le monde veut&nbsp;: à quelle vitesse pouvons-nous migrer?")),
    layer="deep")

u = "pipe"
d = ""
scale = 90  # px per Gbps
x0 = 380
rowsp = [
    (("ExpressRoute gateway (ErGw3Az)", "Passerelle ExpressRoute (ErGw3Az)"), [(10, "solid")], ("10 Gbps", "10 Gb/s")),
    (("Three service meshes", "Trois Service Mesh"), [(1.6, "solid"), (0.4, "soft"), (1.6, "solid"), (0.4, "soft"), (1.6, "solid"), (0.4, "soft")], ("≈ 4.8 to 6 Gbps", "≈ 4,8 à 6 Gb/s")),
    (("One IX appliance", "Un appliance IX"), [(1.6, "solid"), (0.4, "soft")], ("≈ 1.6 to 2 Gbps", "≈ 1,6 à 2 Gb/s")),
    (("One migration", "Une migration"), [(1, "solid")], ("≈ 1 Gbps", "≈ 1 Gb/s")),
]
for g in range(0, 11, 2):
    gx = x0 + g * scale
    d += f'<line class="tick" x1="{gx}" y1="4" x2="{gx}" y2="206"/>'
    d += st(gx, 222, f"{g}", f"{g}", 15, 500, fill="#42566E")
d += st(x0 + 10 * scale + 26, 222, "Gbps", "Gb/s", 15, 600, anchor="start", fill="#42566E")
for i, (lab, segs, val) in enumerate(rowsp):
    y = 8 + i * 50
    d += st(x0 - 18, y + 18, lab[0], lab[1], 19, 600, anchor="end", fill="#0B2545")
    x = x0
    for w, k in segs:
        d += f'<rect class="{"bar" if k == "solid" else "bar-soft"}" x="{x}" y="{y}" width="{w * scale - 3:.1f}" height="36" rx="3"/>'
        x += w * scale
    d += st(x + 14, y + 18, val[0], val[1], 19, 700, anchor="start", fill="#0078D4")
pipefig = figure(svg(1440, 232, d, "Throughput ceilings: gateway 10 Gbps, one IX about 1.6 to 2 Gbps, one migration about 1 Gbps; more service meshes add capacity",
                     "Plafonds de débit&nbsp;: passerelle 10 Gb/s, un IX environ 1,6 à 2 Gb/s, une migration environ 1 Gb/s; plus de Service Mesh ajoutent de la capacité", uid=u),
                 "One IX appliance, not the pipe, is often the narrowest point: scale out service meshes. Light segments reach the documented 2 Gbps ceiling.",
                 "Un seul appliance IX, plutôt que le lien, est souvent le point le plus étroit&nbsp;: ajoutez des Service Mesh. Les segments pâles atteignent le plafond documenté de 2 Gb/s.", "fig-tight")
math = panel("Do the math", "Faites le calcul", tb("p",
    "Days of transfer ≈ <b>TB ÷ (10.8 × effective Gbps)</b>", "Jours de transfert ≈ <b>To ÷ (10,8 × Gb/s effectifs)</b>", "formula")
    + table([("40&nbsp;TB to move", "40&nbsp;To à déplacer"), ("Effective rate", "Débit effectif"), ("Transfer time", "Durée du transfert")],
            [[("1 Gbps gateway at 70%", "Passerelle 1 Gb/s à 70&nbsp;%"), ("0.7 Gbps", "0,7 Gb/s"), ("≈ 5.3 days", "≈ 5,3 jours")],
             [("One IX near its ceiling", "Un IX près de son plafond"), ("1.4 Gbps", "1,4 Gb/s"), ("≈ 2.6 days", "≈ 2,6 jours")],
             [("Three meshes, 10 Gbps path", "Trois Mesh, chemin 10 Gb/s"), ("4.2 Gbps", "4,2 Gb/s"), ("≈ 21 hours", "≈ 21 heures")]],
            "tbl tbl-sm", colw=["48%", "25%", "27%"]), "p-deep")
keep = panel("Keep in mind", "À retenir", ul([
    ("Bulk and RAV replicate before switchover: transfer time is not downtime.", "Bulk et RAV répliquent avant la bascule&nbsp;: la durée du transfert n'est pas une interruption."),
    ("Baseline HCX: up to 200 concurrent Bulk or RAV migrations per service mesh; HCX vMotion runs one at a time.", "HCX de base&nbsp;: jusqu'à 200 migrations Bulk ou RAV simultanées par Service Mesh; HCX vMotion s'exécute une à la fois."),
    ("Also check source disk reads and destination vSAN writes; on Gen 2, add buffer for sync slowdowns.", "Vérifiez aussi les lectures à la source et les écritures vSAN; sur Gen 2, prévoyez une marge pour les ralentissements de synchro."),
], "dense"), "p-note")
add("throughput", "perform", ("How fast can we migrate? Do the math", "À quelle vitesse migrer? Faites le calcul"),
    pipefig + f'<div class="grid g-55-45 mt">{math}{keep}</div>'
    + refs(("https://knowledge.broadcom.com/external/article/373010", "KB 373010: HCX migration scale", "KB 373010&nbsp;: échelle des migrations HCX"),
           ("https://knowledge.broadcom.com/external/article/416441/vmware-hcx-underlay-network-speed-perfo.html", "KB 416441: IX 2 Gbps boundary", "KB 416441&nbsp;: limite IX de 2 Gb/s")),
    notes("3 min",
          [("The picture shows the ceilings. A 10 gigabit gateway is wonderful, but one IX appliance moves roughly 1.6 to 2 gigabits per second, and one migration about 1. To use the pipe, run several service meshes, typically one per cluster pair.",
            "L'image montre les plafonds. Une passerelle de 10 gigabits, c'est excellent, mais un appliance IX déplace environ 1,6 à 2 gigabits par seconde, et une migration environ 1. Pour exploiter le lien, utilisez plusieurs Service Mesh, en général un par paire de grappes."),
           ("The formula on the right fits on a napkin: terabytes divided by 10.8 times the effective gigabits per second gives days of continuous transfer.",
            "La formule à droite tient sur une serviette de table&nbsp;: les téraoctets divisés par 10,8 fois les gigabits par seconde effectifs donnent des jours de transfert continu."),
           ("Key reassurance: with Bulk and RAV, replication happens before the switchover window, so a long transfer does not mean long downtime. On Gen 2, add buffer for the sync slowdowns Microsoft has documented.",
            "Point rassurant&nbsp;: avec Bulk et RAV, la réplication se fait avant la fenêtre de bascule; un long transfert ne signifie donc pas une longue interruption. Sur Gen 2, prévoyez une marge pour les ralentissements de synchronisation documentés par Microsoft.")],
          trans=("A few tuning tips that make a measurable difference.", "Quelques optimisations qui font une différence mesurable.")),
    layer="decide")

tw = panel("Workloads", "Charges de travail", ul([
    ("Right-size from measured use, not from on-premises allocations.", "Ajustez la taille selon l'utilisation mesurée, pas selon les allocations sur site."),
    ("Keep large VMs within one NUMA node where possible (32 cores per socket).", "Gardez les grosses VM dans un seul nœud NUMA quand c'est possible (32 cœurs par socket)."),
    ("Use VMXNET3, PVSCSI and current VMware Tools.", "Utilisez VMXNET3, PVSCSI et des VMware Tools à jour."),
    ("Avoid long-lived snapshots.", "Évitez les instantanés de longue durée."),
    ("RAID-1 for latency-sensitive writes; RAID-5 or 6 for capacity.", "RAID-1 pour les écritures sensibles à la latence; RAID-5 ou 6 pour la capacité."),
    ("Place dependent Azure services in the same region and availability zone; Gen 2 lets you choose the zone.", "Placez les services Azure dépendants dans la même région et la même zone de disponibilité; Gen 2 permet de choisir la zone."),
], "dense"), "p-deep")
tm = panel("Migrations", "Migrations", ul([
    ("Set full CPU reservations on IX appliances.", "Réglez des réservations complètes de processeur sur les appliances IX."),
    ("One service mesh per cluster pair, with IX appliances on different hosts.", "Un Service Mesh par paire de grappes, avec les appliances IX sur des hôtes différents."),
    ("Use WAN Optimization on constrained links; test with and without on fast ones.", "Utilisez WAN Optimization sur les liens limités; testez avec et sans sur les liens rapides."),
    ("Stagger large waves; do not run Transport Analytics during migrations.", "Échelonnez les grandes vagues; ne lancez pas Transport Analytics pendant les migrations."),
    ("Ask for ExpressRoute FastPath (support request on Gen 2) for high-throughput flows.", "Demandez ExpressRoute FastPath (demande de support sur Gen 2) pour les flux à haut débit."),
], "dense"), "p-deep")
add("tuning", "perform", ("Tuning tips that matter", "Optimisations qui comptent"),
    f'<div class="grid g-50-50">{tw}{tm}</div>'
    + refs(("https://knowledge.broadcom.com/external/article/447245/hcx-migration-performance-caps-at-14-gbp.html", "KB 447245: scaling HCX throughput", "KB 447245&nbsp;: augmenter le débit HCX")),
    notes("2 min",
          [("On the workload side, the biggest win is right-sizing from real usage; many on-premises VMs are oversized, and that directly drives host count.",
            "Côté charges, le plus grand gain vient de l'ajustement selon l'utilisation réelle; beaucoup de VM sur site sont surdimensionnées, ce qui fait directement grimper le nombre d'hôtes."),
           ("On the migration side: CPU reservations on IX appliances and more service meshes. Broadcom documents that adding CPU alone does not raise the per-IX ceiling; scaling out does.",
            "Côté migration&nbsp;: réservations de processeur sur les appliances IX et plus de Service Mesh. Broadcom indique qu'ajouter du processeur seul ne relève pas le plafond par IX; l'ajout d'appliances, oui.")],
          trans=("Let's bring it all together into a roadmap.", "Rassemblons le tout dans une feuille de route.")),
    layer="deep", skip=True)

# ================================================================ ADOPT
add("div-adopt", "adopt", ("Adoption roadmap", "Feuille de route d'adoption"),
    tb("p", "Small steps, early proof, steady waves.", "Petits pas, preuves rapides, vagues régulières.", "promise"),
    notes("30 s",
          [("Everything we discussed fits in five phases.", "Tout ce dont nous avons parlé tient en cinq phases.")],
          trans=("Here they are.", "Les voici.")),
    kind="divider")

u = "road"
d = ""
pxw = 70
gx0 = 250
phases = [
    (("Assess", "Évaluer"), 0, 4, "bar", False),
    (("Connect", "Connecter"), 3, 6, "bar", False),
    (("Pilot", "Pilote"), 6, 9, "bar-pick", False),
    (("Migrate in waves", "Migrer par vagues"), 8, 16, "bar", True),
    (("Optimize", "Optimiser"), 10, 16, "bar-soft", True),
]
for w in range(0, 17, 2):
    xx = gx0 + w * pxw
    d += f'<line class="tick" x1="{xx}" y1="12" x2="{xx}" y2="300"/>'
    d += st(xx, 318, f"{w}", f"{w}", 13, 400, fill="#42566E")
d += st(gx0 + 8 * pxw, 342, "weeks (illustrative)", "semaines (à titre indicatif)", 14, 600, fill="#42566E")
for i, (nm, a, b, cls, cont) in enumerate(phases):
    y = 20 + i * 56
    d += st(gx0 - 16, y + 20, nm[0], nm[1], 18, 700, anchor="end", fill="#0B2545")
    d += f'<rect class="{cls}" x="{gx0 + a * pxw}" y="{y}" width="{(b - a) * pxw - 4}" height="40" rx="4"/>'
    if cont:
        d += line(gx0 + b * pxw - 4, y + 20, gx0 + b * pxw + 34, y + 20, "ln-b", "b", u, dash=True)
roadfig = figure(svg(1440, 352, d, "Illustrative roadmap: assess weeks 0 to 4, connect 3 to 6, pilot 6 to 9, waves from week 8, optimize from week 10",
                     "Feuille de route indicative&nbsp;: évaluer semaines 0 à 4, connecter 3 à 6, pilote 6 à 9, vagues dès la semaine 8, optimiser dès la semaine 10", uid=u),
                 "Phases overlap on purpose: connectivity work starts while the assessment finishes.",
                 "Les phases se chevauchent volontairement&nbsp;: le travail de connectivité commence pendant que l'évaluation se termine.", "fig-tight")
pd = ('<div class="phase-grid">'
      + '<div><b>' + t("Assess", "Évaluer") + '</b>' + t("Azure Migrate discovery and AVS assessment; dependencies; keep-IP or re-IP per app; VCF subscription; host quota", "Découverte et évaluation AVS Azure Migrate; dépendances; IP conservée ou réadressée par application; abonnement VCF; quota d'hôtes") + '</div>'
      + '<div><b>' + t("Connect", "Connecter") + '</b>' + t("Landing zone and hub; ExpressRoute; Gen 2 private cloud; DNS, firewall, identity; HCX service mesh", "Zone d'atterrissage et hub; ExpressRoute; nuage privé Gen 2; DNS, pare-feu, identité; Service Mesh HCX") + '</div>'
      + '<div><b>' + t("Pilot", "Pilote") + '</b>' + t("10 to 20 low-risk VMs; prove backup, monitoring, rollback; run the benchmark", "10 à 20 VM peu risquées; valider sauvegarde, surveillance, retour arrière; faire le banc d'essai") + '</div>'
      + '<div><b>' + t("Migrate in waves", "Migrer par vagues") + '</b>' + t("Regular cadence; gateway cutovers; remove extensions as subnets empty", "Cadence régulière; bascules de passerelles; retrait des extensions à mesure que les sous-réseaux se vident") + '</div>'
      + '<div><b>' + t("Optimize", "Optimiser") + '</b>' + t("Right-size; reserved capacity; decommission hardware; modernize to Azure services", "Ajuster les tailles; capacité réservée; mise hors service du matériel; modernisation vers les services Azure") + '</div>'
      + '</div>')
add("roadmap", "adopt", ("A phased path to AVS", "Un parcours en phases vers AVS"),
    roadfig + pd,
    notes("3 min",
          [("Five phases. The timeline is illustrative; the assessment tells us the real one.",
            "Cinq phases. L'échéancier est indicatif; l'évaluation nous donnera le vrai."),
           ("The pilot is the hinge: it proves connectivity, operations, backup and rollback on real workloads before anything critical moves, and it produces the benchmark report.",
            "Le pilote est la charnière&nbsp;: il valide la connectivité, l'exploitation, la sauvegarde et le retour arrière sur de vraies charges avant tout déplacement critique, et il produit le rapport de banc d'essai."),
           ("Quick wins you can start next week: run the assessment, settle the IP plan, and pick one non-critical application to take end to end.",
            "Gains rapides dès la semaine prochaine&nbsp;: lancer l'évaluation, arrêter le plan IP et choisir une application non critique à mener de bout en bout.")],
          trans=("So, what happens after today?", "Alors, que se passe-t-il après aujourd'hui?")),
    layer="plan")

n1 = panel("Next two weeks", "Deux prochaines semaines", ul([
    ("Deploy the Azure Migrate appliance and run the AVS assessment", "Déployer l'appliance Azure Migrate et lancer l'évaluation AVS"),
    ("IP planning workshop: /22, HCX /24s, workload segments", "Atelier de plan IP&nbsp;: /22, /24 HCX, segments de charges"),
    ("Confirm region, such as Canada Central or Canada East, and request host quota", "Confirmer la région, comme Canada Centre ou Canada Est, et demander le quota d'hôtes"),
    ("Confirm your portable VCF subscription entitlement", "Confirmer vos droits d'abonnement VCF transférable"),
], ""), "p-exec")
n2 = panel("Decisions we need from you", "Décisions requises de votre part", ul([
    ("ExpressRoute bandwidth and gateway size", "Bande passante ExpressRoute et taille de passerelle"),
    ("Keep-IP or re-IP policy, per application group", "Politique IP conservée ou réadressée, par groupe d'applications"),
    ("Inspection and egress: Azure Firewall or your NVA", "Inspection et sortie&nbsp;: Azure Firewall ou votre NVA"),
    ("Backup and disaster recovery solution", "Solution de sauvegarde et de reprise après sinistre"),
    ("Pilot applications and their owners", "Applications pilotes et leurs responsables"),
], ""), "p-deep")
n3 = panel("How we help", "Notre accompagnement", ul([
    ("Landing zone and connectivity design", "Conception de la zone d'atterrissage et de la connectivité"),
    ("HCX setup and pilot runbook", "Configuration HCX et procédure du pilote"),
    ("Benchmark plan and report", "Plan et rapport de banc d'essai"),
    ("Wave plan and hypercare model", "Plan de vagues et modèle de soutien renforcé"),
], ""), "p-eli5")
add("next-steps", "adopt", ("Next steps", "Prochaines étapes"),
    f'<div class="grid g-34-33-33">{n1}{n2}{n3}</div>'
    + callout("cta", "Proposed next step:", "Prochaine étape proposée&nbsp;:",
              "agree on the pilot scope today, and book the IP planning workshop within two weeks.",
              "convenir aujourd'hui de la portée du pilote et fixer l'atelier de plan IP d'ici deux semaines."),
    notes("3 min",
          [("Close with three concrete things: what happens in the next two weeks, which decisions we need from them, and what we bring.",
            "Concluez avec trois choses concrètes&nbsp;: ce qui se passe dans les deux prochaines semaines, les décisions requises de leur part et ce que nous apportons."),
           ("Ask for the commitment explicitly: agree on the pilot scope and a date for the IP planning workshop.",
            "Demandez l'engagement explicitement&nbsp;: convenir de la portée du pilote et d'une date pour l'atelier de plan IP."),
           ("Then open the floor. The appendix has the FAQ, re-IP script examples and all references.",
            "Ouvrez ensuite la discussion. L'annexe contient la FAQ, des exemples de scripts de réadressage et toutes les références.")],
          qa=[(("What does the pilot cost?", "Combien coûte le pilote?"),
               ("Mainly a minimum three-host AV64 private cloud for the pilot period plus connectivity; we size it precisely after the assessment, and reservations can lower the run cost once you commit.",
                "Surtout un nuage privé AV64 d'au moins trois hôtes pour la durée du pilote, plus la connectivité; nous le dimensionnons précisément après l'évaluation, et les réservations peuvent réduire le coût d'exploitation une fois engagé."))]),
    layer="exec")

# ================================================================ APPENDIX
faq = [
    (("Do we have to change our VMs?", "Faut-il modifier nos VM?"),
     ("No. Same vSphere. HCX live migration needs hardware version 9 or later.", "Non. Même vSphere. La migration à chaud HCX exige la version matérielle 9 ou plus.")),
    (("Can we keep our IP addresses?", "Pouvons-nous conserver nos adresses IP?"),
     ("Yes, with HCX network extension, or change them during Bulk Migration.", "Oui, avec l'extension réseau HCX, ou les changer pendant Bulk Migration.")),
    (("How much downtime?", "Quelle interruption?"),
     ("None with vMotion or RAV; about one reboot with Bulk Migration.", "Aucune avec vMotion ou RAV; environ un redémarrage avec Bulk Migration.")),
    (("Who patches what?", "Qui applique quels correctifs?"),
     ("Microsoft: hosts, ESXi, vCenter, vSAN, NSX. You: VMs, guest OS, NSX configuration, HCX upgrades.", "Microsoft&nbsp;: hôtes, ESXi, vCenter, vSAN, NSX. Vous&nbsp;: VM, système invité, configuration NSX, mises à niveau HCX.")),
    (("Can we go back?", "Pouvons-nous revenir en arrière?"),
     ("Yes. HCX migrates in both directions, and Bulk keeps the source VM for rollback.", "Oui. HCX migre dans les deux sens, et Bulk conserve la VM source pour un retour arrière.")),
    (("What about licensing?", "Et les licences?"),
     ("Bring a portable VCF subscription from Broadcom. Windows Server and SQL Server get Azure Hybrid Benefit and no-cost ESUs.", "Apportez un abonnement VCF transférable de Broadcom. Windows Server et SQL Server profitent d'Azure Hybrid Benefit et des ESU sans frais.")),
]
fh = '<div class="faq">' + "".join(f'<div><h3>{t(q[0], q[1])}</h3><p>{t(a[0], a[1])}</p></div>' for q, a in faq) + '</div>'
add("faq", "appendix", ("Frequently asked questions", "Questions fréquentes"), fh,
    notes(("as needed", "au besoin"), [("Use this slide to close the Q&amp;A or as a leave-behind.", "Utilisez cette diapositive pour conclure la période de questions ou comme aide-mémoire.")]),
    layer="appendix")

w_code = (
    "# Example: re-IP a Windows VM after vMotion or RAV\n"
    "$s = @'\n"
    "$if = 'Ethernet0'\n"
    "Get-NetIPAddress -InterfaceAlias $if -AddressFamily IPv4 |\n"
    "  Remove-NetIPAddress -Confirm:$false\n"
    "Remove-NetRoute -InterfaceAlias $if -DestinationPrefix 0.0.0.0/0 `\n"
    "  -Confirm:$false\n"
    "New-NetIPAddress -InterfaceAlias $if -IPAddress 10.110.4.21 `\n"
    "  -PrefixLength 24 -DefaultGateway 10.110.4.1\n"
    "Set-DnsClientServerAddress -InterfaceAlias $if `\n"
    "  -ServerAddresses 10.0.0.10,10.0.0.11\n"
    "Register-DnsClient\n"
    "'@\n"
    "Invoke-VMScript -VM app01 -GuestCredential $cred `\n"
    "  -ScriptType Powershell -ScriptText $s")
l_code = (
    "# Example: re-IP a Linux VM with NetworkManager\n"
    "nmcli con mod \"System eth0\" ipv4.method manual \\\n"
    "  ipv4.addresses 10.110.4.22/24 ipv4.gateway 10.110.4.1 \\\n"
    "  ipv4.dns \"10.0.0.10 10.0.0.11\"\n"
    "nmcli con up \"System eth0\"\n\n"
    "# Then update DNS records, for example:\n"
    "# nsupdate, or your IPAM / DNS API")
add("reip-scripts", "appendix", ("Appendix: re-IP script examples", "Annexe&nbsp;: exemples de scripts de réadressage"),
    f'<div class="grid g-55-45">' + panel("Windows, through VMware Tools (PowerCLI)", "Windows, par VMware Tools (PowerCLI)", code(w_code), "p-code sm")
    + panel("Linux (RHEL, Rocky, Ubuntu with NetworkManager)", "Linux (RHEL, Rocky, Ubuntu avec NetworkManager)", code(l_code), "p-code sm") + '</div>'
    + callout("warn", "Test first:", "À tester d'abord&nbsp;:",
              "interface and connection names vary by image. Validate on pilot VMs, keep console access ready, and run the script from a host that still reaches the VM through VMware Tools.",
              "les noms d'interface et de connexion varient selon l'image. Validez sur les VM pilotes, gardez l'accès console prêt et exécutez le script depuis un hôte qui joint encore la VM par VMware Tools."),
    notes(("as needed", "au besoin"),
          [("These are examples, not production scripts. The point is that re-IP after a live migration is a small, repeatable script run through VMware Tools, so it works even while the network settings are changing.",
            "Ce sont des exemples, pas des scripts de production. L'idée est que le réadressage après une migration à chaud est un petit script reproductible exécuté par VMware Tools; il fonctionne donc même pendant que les paramètres réseau changent.")]),
    layer="appendix", skip=True)

groups = [
    (("AVS Gen 2", "AVS Gen 2"), [
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-introduction", "Introduction to Gen 2", "Introduction à Gen 2"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-design-consideration", "Gen 2 design considerations", "Considérations de conception Gen 2"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-routing-architecture", "Gen 2 route architecture", "Architecture de routage Gen 2"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-internet-connectivity-design-considerations", "Gen 2 internet options", "Options Internet Gen 2"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-dns-forward-lookup-zone", "Gen 2 DNS zones", "Zones DNS Gen 2"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-connect-on-premises", "Connect Gen 2 to on-premises", "Relier Gen 2 au site"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-create-azure-vmware-virtual-network-private-cloud", "Create a Gen 2 private cloud", "Créer un nuage privé Gen 2"),
    ]),
    (("Platform and licensing", "Plateforme et licences"), [
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/introduction", "AVS introduction and responsibility matrix", "Introduction AVS et matrice de responsabilités"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/architecture-private-clouds", "Hosts, clusters and limits", "Hôtes, grappes et limites"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/vmware-cloud-foundations-license-portability", "Portable VCF on AVS", "VCF transférable sur AVS"),
        ("https://azure.microsoft.com/en-us/pricing/details/azure-vmware/", "AVS pricing", "Tarifs AVS"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/azure-vmware-solution-platform-updates", "What's new in AVS", "Nouveautés d'AVS"),
        ("https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-virtual-network-gateways", "ExpressRoute gateway SKUs", "SKU de passerelles ExpressRoute"),
    ]),
    (("HCX and migration", "HCX et migration"), [
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/install-vmware-hcx", "Install HCX", "Installer HCX"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/configure-vmware-hcx", "Configure HCX Connector", "Configurer HCX Connector"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/architecture-migrate", "HCX migration options", "Options de migration HCX"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/tutorial-network-checklist", "Network checklist and ports", "Liste réseau et ports"),
        ("https://techdocs.broadcom.com/us/en/vmware-cis/hcx/vmware-hcx/4-10/vmware-hcx-user-guide-4-10/preparing-for-hcx-installations/network-underlay-minimum-requirements.html", "HCX underlay minimums", "Minimums HCX du réseau sous-jacent"),
        ("https://knowledge.broadcom.com/external/article/373010", "HCX Bulk and RAV scale (KB 373010)", "Échelle Bulk et RAV HCX (KB 373010)"),
        ("https://learn.microsoft.com/en-us/azure/migrate/how-to-create-azure-vmware-solution-assessment", "Azure Migrate AVS assessment", "Évaluation AVS d'Azure Migrate"),
    ]),
    (("Operations and troubleshooting", "Exploitation et dépannage"), [
        ("https://techcommunity.microsoft.com/blog/azuremigrationblog/vmware-hcx-troubleshooting-with-azure-vmware-solution/4109114", "HCX troubleshooting with AVS", "Dépannage HCX avec AVS"),
        ("https://knowledge.broadcom.com/external/article/396477/hcxixne-tunnels-down.html", "HCX tunnels down (KB 396477)", "Tunnels HCX inactifs (KB 396477)"),
        ("https://azure.github.io/azure-monitor-baseline-alerts/patterns/specialized/avs/", "Azure Monitor Baseline Alerts for AVS", "Alertes de base Azure Monitor pour AVS"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/configure-alerts-for-azure-vmware-solution", "Configure AVS alerts", "Configurer les alertes AVS"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/configure-identity-source-vcenter", "Identity sources for vCenter", "Sources d'identité pour vCenter"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/using-run-command", "Run Command", "Run Command"),
        ("https://learn.microsoft.com/en-us/azure/azure-vmware/attach-azure-netapp-files-to-azure-vmware-solution-hosts", "Azure NetApp Files datastores", "Banques Azure NetApp Files"),
    ]),
]
rh = '<div class="refgrid">'
for (gen, gfr), items in groups:
    rh += f'<div><h3>{t(gen, gfr)}</h3><ul>' + "".join(f'<li>{link(u2, e, f)}</li>' for u2, e, f in items) + '</ul></div>'
rh += '</div>'
add("references", "appendix", ("References", "Références"), rh,
    notes(("as needed", "au besoin"), [("All links point to Microsoft Learn, Microsoft Tech Community or Broadcom documentation, checked in October 2026. Gen 2 documentation evolves quickly; recheck limits before design sign-off.",
                          "Tous les liens mènent à Microsoft Learn, à Microsoft Tech Community ou à la documentation Broadcom, vérifiés en octobre 2026. La documentation Gen 2 évolue vite; revalidez les limites avant d'approuver la conception.")]),
    layer="appendix")
