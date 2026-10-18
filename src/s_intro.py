from lib import *

# ---------------------------------------------------------------- 1. Title
title_body = (
    '<div class="title-wrap">'
    + '<h1>Azure VMware Solution Gen&nbsp;2</h1>'
    + tb("p", "Hybrid connectivity, HCX migration and day-2 operations: a simple path from your datacenter to Azure",
         "Connectivité hybride, migration HCX et exploitation au quotidien&nbsp;: un chemin simple de votre centre de données vers Azure",
         "subtitle")
    + '<p class="prepared">' + t("Prepared for", "Préparé pour") + ' <span data-cfg="client"></span>'
    + '<span class="cfg-sep" data-cfg-sep></span><span data-cfg="presenter"></span>'
    + '<span class="cfg-sep" data-cfg-sep2></span><span data-cfg="date"></span></p>'
    + '</div>'
    + '<div class="hero-line" data-hero></div>'
)
add("title", None, ("Azure VMware Solution Gen 2", "Azure VMware Solution Gen 2"), title_body,
    notes("2 min",
          [("Welcome everyone. Today's goal is simple: you leave with a clear, low-risk path from your VMware datacenter to Azure VMware Solution.",
            "Bienvenue à tous. L'objectif d'aujourd'hui est simple&nbsp;: repartir avec un chemin clair et peu risqué entre votre centre de données VMware et Azure VMware Solution."),
           ("We focus on Gen 2, the current generation, where the private cloud lives inside your own Azure virtual network.",
            "Nous nous concentrons sur Gen 2, la génération actuelle, où le nuage privé vit dans votre propre réseau virtuel Azure."),
           ("Each big topic has three layers: an executive summary, a plain-language explanation, and a technical deep dive. We can skip deep dives depending on who is in the room.",
            "Chaque grand sujet a trois niveaux&nbsp;: un sommaire pour la direction, une explication en termes simples et une plongée technique. Nous pouvons sauter les plongées techniques selon l'auditoire."),
           ("Before we start: what is the one outcome that would make this meeting a success for you? A datacenter exit date, a renewal deadline, a specific application?",
            "Avant de commencer&nbsp;: quel est le résultat qui ferait de cette rencontre un succès pour vous? Une date de sortie du centre de données, une échéance de renouvellement, une application précise?")],
          trans=("Let me show you how the next 90 minutes are organized.",
                 "Voyons comment les 90 prochaines minutes sont organisées."),
          tip=("Keys: ←/→ navigate, L switches language, N shows these notes, P opens a separate presenter window (best when screen sharing), D hides deep dives for an executive audience, O opens the slide list, F goes full screen. Edit the client name, presenter and date in the deck-config block at the top of the HTML file.",
               "Touches&nbsp;: ←/→ pour naviguer, L change la langue, N affiche ces notes, P ouvre une fenêtre de présentateur séparée (idéal en partage d'écran), D masque les plongées techniques pour un auditoire de direction, O ouvre la liste des diapositives, F passe en plein écran. Modifiez le nom du client, du présentateur et la date dans le bloc deck-config au début du fichier HTML.")),
    kind="title")

# ---------------------------------------------------------------- 2. Agenda
agenda_rows = [
    ("intro", "8", "Why AVS Gen 2, and who does what", "Pourquoi AVS Gen 2 et qui fait quoi"),
    ("connect", "17", "Hybrid connectivity: network, IP plan, DNS, internet", "Connectivité hybride&nbsp;: réseau, plan IP, DNS, Internet"),
    ("migrate", "25", "HCX migration, network extension and re-IP", "Migration HCX, extension réseau et réadressage IP"),
    ("operate", "10", "Day-2 operations and monitoring", "Exploitation au quotidien et surveillance"),
    ("troubleshoot", "15", "Troubleshooting the hybrid path", "Dépannage du chemin hybride"),
    ("perform", "10", "Performance, sizing and benchmarks", "Performance, dimensionnement et bancs d'essai"),
    ("adopt", "5", "Adoption roadmap and next steps", "Feuille de route d'adoption et prochaines étapes"),
]
sec_name = {s[0]: (s[1], s[2]) for s in SECTIONS}
ag = '<ol class="agenda">'
for sid, mins, en, fr in agenda_rows:
    n = sec_name[sid]
    ag += (f'<li><span class="ag-sec">{t(n[0], n[1])}</span><span class="ag-desc">{t(en, fr)}</span>'
           f'<span class="ag-min">{mins} min</span></li>')
ag += "</ol>"
legend = (
    '<div class="legend">'
    + tb("h3", "How each topic is built", "Comment chaque sujet est construit")
    + '<div class="lg-item"><span class="badge b-exec">' + t(*LAYERS["exec"]) + '</span>'
    + tb("p", "Business value, risk and cost in three or four lines.", "Valeur d'affaires, risque et coût en trois ou quatre lignes.") + '</div>'
    + '<div class="lg-item"><span class="badge b-eli5">' + t(*LAYERS["eli5"]) + '</span>'
    + tb("p", "The idea explained with an everyday analogy.", "L'idée expliquée avec une analogie du quotidien.") + '</div>'
    + '<div class="lg-item"><span class="badge b-deep">' + t(*LAYERS["deep"]) + '</span>'
    + tb("p", "Architecture, configuration, limits and gotchas for engineers.", "Architecture, configuration, limites et pièges pour les ingénieurs.") + '</div>'
    + '<div class="lg-item"><span class="badge b-arch">' + t(*LAYERS["arch"]) + '</span>'
    + tb("p", "Diagrams that show how the pieces connect.", "Diagrammes qui montrent comment les éléments se relient.") + '</div>'
    + '</div>'
)
add("agenda", "intro", ("Agenda: 90 minutes", "Ordre du jour&nbsp;: 90 minutes"),
    f'<div class="grid g-agenda">{ag}{legend}</div>',
    notes("1 min",
          [("Seven stops, the same line you see at the top of every slide, so you always know where we are.",
            "Sept arrêts, la même ligne que vous voyez en haut de chaque diapositive, pour toujours savoir où nous en sommes."),
           ("Migration gets the most time because that is where most of the decisions are, including whether you keep or change IP addresses.",
            "La migration reçoit le plus de temps parce que c'est là que se prennent la plupart des décisions, dont celle de conserver ou de changer les adresses IP."),
           ("Please interrupt at any time. The deep dives are there for your engineers; if we are short on time, I will skip them and share the deck afterwards.",
            "N'hésitez pas à m'interrompre. Les plongées techniques sont là pour vos ingénieurs; si le temps manque, je les sauterai et je vous transmettrai la présentation.")],
          trans=("Let's start with why customers choose AVS in the first place.",
                 "Commençons par les raisons pour lesquelles les clients choisissent AVS.")),
    layer="plan")

# ---------------------------------------------------------------- 3. Why AVS
why_left = panel("What you get", "Ce que vous obtenez", ul([
    ("<b>The same VMware stack</b> (vSphere 8, vSAN, NSX, HCX): no application changes, no retraining, your runbooks still apply.",
     "<b>La même pile VMware</b> (vSphere 8, vSAN, NSX, HCX)&nbsp;: aucun changement aux applications, aucune nouvelle formation, vos procédures restent valides."),
    ("<b>Microsoft runs the platform</b>: hardware, hypervisor patching and host replacement, with one support entry point.",
     "<b>Microsoft exploite la plateforme</b>&nbsp;: matériel, correctifs de l'hyperviseur et remplacement des hôtes, avec un seul point d'entrée pour le support."),
    ("<b>Inside your Azure network</b>: Gen 2 sits in your virtual network, one hop from Azure data, AI, backup and security services.",
     "<b>Dans votre réseau Azure</b>&nbsp;: Gen 2 réside dans votre réseau virtuel, à un saut des services Azure de données, d'IA, de sauvegarde et de sécurité."),
    ("<b>Speed with a safety net</b>: live migration in waves, rollback options, and hosts added on demand within your quota.",
     "<b>Rapidité avec filet de sécurité</b>&nbsp;: migration à chaud par vagues, options de retour arrière et hôtes ajoutés sur demande selon votre quota."),
], "big"), "p-exec")
why_right = panel("What to know upfront", "Ce qu'il faut savoir d'emblée", ul([
    ("<b>Licensing</b>: new AVS capacity requires a portable VMware Cloud Foundation (VCF) subscription from Broadcom. Microsoft still operates the full stack.",
     "<b>Licences</b>&nbsp;: toute nouvelle capacité AVS exige un abonnement VMware Cloud Foundation (VCF) transférable acheté chez Broadcom. Microsoft exploite toujours l'ensemble de la pile."),
    ("<b>Windows Server and SQL Server</b>: Azure Hybrid Benefit applies, and Extended Security Updates come at no extra charge.",
     "<b>Windows Server et SQL Server</b>&nbsp;: Azure Hybrid Benefit s'applique et les mises à jour de sécurité étendues (ESU) sont offertes sans frais supplémentaires."),
    ("<b>Minimum footprint</b>: 3 AV64 hosts per cluster; 4 or more recommended for production.",
     "<b>Empreinte minimale</b>&nbsp;: 3 hôtes AV64 par grappe; 4 ou plus recommandés en production."),
    ("<b>Regions</b>: Gen 2 is available in Canada Central and Canada East, among others.",
     "<b>Régions</b>&nbsp;: Gen 2 est offert notamment dans Canada Centre et Canada Est."),
]), "p-note")
add("why", "intro", ("Why AVS: move fast without re-platforming", "Pourquoi AVS&nbsp;: migrer vite sans changer de plateforme"),
    f'<div class="grid g-55-45">{why_left}{why_right}</div>'
    + refs(("https://azure.microsoft.com/en-us/pricing/details/azure-vmware/", "AVS pricing", "Tarifs AVS"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/vmware-cloud-foundations-license-portability", "Portable VCF on AVS", "VCF transférable sur AVS"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-introduction", "Gen 2 regions", "Régions Gen 2")),
    notes("3 min",
          [("The headline: AVS lets you leave the datacenter on your timeline without rewriting or re-platforming anything. Your VMs keep running on vSphere.",
            "Le message clé&nbsp;: AVS vous permet de quitter le centre de données à votre rythme, sans réécrire ni changer de plateforme. Vos VM continuent de tourner sur vSphere."),
           ("Typical triggers we see: hardware refresh, a datacenter contract ending, or a VMware renewal. AVS buys time and options at once.",
            "Les déclencheurs typiques&nbsp;: renouvellement du matériel, fin d'un contrat de centre de données ou renouvellement VMware. AVS donne du temps et des options du même coup."),
           ("Be transparent on licensing: since October 2025, new AVS capacity needs a portable VCF subscription bought from Broadcom. The AVS price covers the Azure infrastructure and the managed service.",
            "Soyez transparent sur les licences&nbsp;: depuis octobre 2025, toute nouvelle capacité AVS exige un abonnement VCF transférable acheté chez Broadcom. Le prix AVS couvre l'infrastructure Azure et le service géré.")],
          qa=[(("Is AVS cheaper than staying on-premises?", "AVS coûte-t-il moins cher que de rester sur site?"),
               ("It depends on what you count. Compare full cost: hardware refresh, facilities, power, and the staff time spent patching and replacing hardware. The Azure Migrate AVS assessment gives a node count and a monthly estimate from your real usage.",
                "Cela dépend de ce qu'on compte. Comparez le coût complet&nbsp;: renouvellement du matériel, locaux, électricité et le temps du personnel consacré aux correctifs et au remplacement du matériel. L'évaluation AVS d'Azure Migrate fournit un nombre de nœuds et une estimation mensuelle à partir de votre utilisation réelle.")),
              (("We have license-included AVS today. What changes?", "Nous avons déjà AVS avec licence incluse. Qu'est-ce qui change?"),
               ("Existing reservations and pay-as-you-go nodes have specific transition dates. Check your exact dates with the Microsoft account team and the portable VCF licensing reference.",
                "Les réservations existantes et les nœuds à l'utilisation ont des dates de transition précises. Validez vos dates exactes avec l'équipe de compte Microsoft et la référence sur les licences VCF transférables."))],
          trans=("Here is what Gen 2 actually looks like.", "Voici à quoi ressemble concrètement Gen 2.")),
    layer="exec")

# ---------------------------------------------------------------- 4. AVS Gen 2 in one picture
u = "pic"
d = ""
# region frame
d += rect(10, 10, 860, 470, "bx-region", 10)
d += st(30, 36, "Azure region (for example Canada Central)", "Région Azure (par exemple Canada Centre)", 16, 600, anchor="start", fill="#42566E")
# vnet frame
d += rect(30, 56, 820, 404, "bx-vnet", 8)
d += st(50, 80, "Your Azure virtual network", "Votre réseau virtuel Azure", 16, 600, anchor="start", fill="#0078D4")
# private cloud stack
d += rect(50, 96, 470, 344, "bx-pc", 8)
d += st(285, 120, "AVS Gen 2 private cloud", "Nuage privé AVS Gen 2", 18, 700, fill="#0B2545")
layers = [
    ("HCX 4.11 Enterprise: migration", "HCX 4.11 Enterprise&nbsp;: migration", "st-hcx"),
    ("NSX 4.2: networking and firewall", "NSX 4.2&nbsp;: réseau et pare-feu", "st-nsx"),
    ("vCenter + vSphere 8 (ESXi)", "vCenter + vSphere 8 (ESXi)", "st-vc"),
    ("vSAN ESA: all-NVMe storage", "vSAN ESA&nbsp;: stockage tout NVMe", "st-vsan"),
    ("AV64 bare-metal hosts (3 to 16 per cluster)", "Hôtes physiques AV64 (3 à 16 par grappe)", "st-hw"),
]
y = 140
for en, fr, c in layers:
    d += box(70, y, 430, 50, en, fr, c, 17, 500)
    y += 58
# azure services in vnet
d += rect(550, 96, 280, 344, "bx-soft", 8)
d += st(690, 120, "Also in the network", "Aussi dans le réseau", 17, 700, fill="#0B2545")
svcs = [("Azure Firewall or NVA", "Azure Firewall ou NVA"), ("DNS Private Resolver", "DNS Private Resolver"),
        ("Azure NetApp Files", "Azure NetApp Files"), ("Private endpoints to PaaS", "Points de terminaison privés"),
        ("Backup and monitoring", "Sauvegarde et surveillance")]
y = 140
for en, fr in svcs:
    d += box(566, y, 248, 50, en, fr, "bx-svc", 15, 500)
    y += 58
d += line(520, 268, 548, 268, "ln-b", "b", u, both=True)
# on-prem link
d += line(440, 480, 440, 536, "ln", "a", u, both=True)
d += st(452, 508, "ExpressRoute or VPN", "ExpressRoute ou VPN", 15, 500, anchor="start", fill="#42566E")
d += box(250, 538, 380, 46, "Your datacenter", "Votre centre de données", "bx-onprem", 17, 600)
pic = figure(svg(880, 600, d, "AVS Gen 2 private cloud stack inside an Azure virtual network, connected to the datacenter",
                 "Pile du nuage privé AVS Gen 2 dans un réseau virtuel Azure, reliée au centre de données", uid=u),
             "The private cloud is a set of dedicated hosts placed inside your virtual network; Azure services sit next to it.",
             "Le nuage privé est un ensemble d'hôtes dédiés placés dans votre réseau virtuel; les services Azure sont juste à côté.", "fig-tight")
eli5 = panel("ELI5", "En termes simples", tb("p",
    "Think of Azure as an office tower. AVS Gen 2 gives you your own private floor, with the same furniture you have at home (VMware). The building manager (Microsoft) handles electricity, elevators and repairs. Because your floor is inside the tower, every other service is one elevator ride away.",
    "Imaginez Azure comme une tour de bureaux. AVS Gen 2 vous donne votre propre étage privé, avec les mêmes meubles qu'à la maison (VMware). Le gestionnaire de l'immeuble (Microsoft) s'occupe de l'électricité, des ascenseurs et des réparations. Comme votre étage est dans la tour, tous les autres services sont à un trajet d'ascenseur.", "eli5-text sm"), "p-eli5")
facts = ('<div class="facts">'
         + '<div><b>AV64</b>' + t("64 cores, 1&nbsp;TB RAM, 19.25&nbsp;TB raw NVMe, 100&nbsp;Gbps", "64 cœurs, 1&nbsp;To de RAM, 19,25&nbsp;To NVMe brut, 100&nbsp;Gb/s") + '</div>'
         + '<div><b>' + t("Scale", "Échelle") + '</b>' + t("3 to 16 hosts per cluster; up to 12 clusters and 96 hosts per private cloud", "3 à 16 hôtes par grappe; jusqu'à 12 grappes et 96 hôtes par nuage privé") + '</div>'
         + '<div><b>' + t("Network model", "Modèle réseau") + '</b>' + t("Deployed in your virtual network: peering, NSGs and route tables work as usual", "Dans votre réseau virtuel&nbsp;: appairage, NSG et tables de routage fonctionnent comme d'habitude") + '</div>'
         + '</div>')
add("picture", "intro", ("AVS Gen 2 in one picture", "AVS Gen 2 en une image"),
    f'<div class="grid g-40-60"><div class="stack">{eli5}{facts}</div>{pic}</div>',
    notes("3 min",
          [("Read the picture from the bottom up: dedicated bare-metal AV64 hosts, vSAN storage, vSphere and vCenter, NSX networking, and HCX for migration. This is the same software you run today.",
            "Lisez l'image de bas en haut&nbsp;: hôtes physiques AV64 dédiés, stockage vSAN, vSphere et vCenter, réseau NSX et HCX pour la migration. C'est le même logiciel que vous utilisez aujourd'hui."),
           ("The key Gen 2 idea is the blue box: the private cloud is placed inside your Azure virtual network. Firewall, DNS, storage and PaaS endpoints are neighbours, not a separate world.",
            "L'idée clé de Gen 2, c'est la boîte bleue&nbsp;: le nuage privé est placé dans votre réseau virtuel Azure. Pare-feu, DNS, stockage et points de terminaison PaaS sont des voisins, pas un monde à part."),
           ("Versions at time of writing per Microsoft Learn: vCenter and ESXi 8.0 U3, NSX 4.2.3, HCX 4.11. Microsoft upgrades these for you.",
            "Versions au moment de la rédaction selon Microsoft Learn&nbsp;: vCenter et ESXi 8.0 U3, NSX 4.2.3, HCX 4.11. Microsoft les met à niveau pour vous.")],
          qa=[(("We read about a Microsoft-managed ExpressRoute circuit and Global Reach. Does that apply?", "Nous avons lu qu'il y avait un circuit ExpressRoute géré par Microsoft et Global Reach. Est-ce que ça s'applique?"),
               ("That describes the first generation. Gen 2 is deployed into your virtual network, so connectivity is standard Azure networking: peering, your own ExpressRoute or VPN gateway, your own firewall.",
                "Cela décrit la première génération. Gen 2 est déployé dans votre réseau virtuel; la connectivité est donc du réseau Azure standard&nbsp;: appairage, votre propre passerelle ExpressRoute ou VPN, votre propre pare-feu.")),
              (("Are the hosts shared with other customers?", "Les hôtes sont-ils partagés avec d'autres clients?"),
               ("No. Hosts are dedicated bare-metal servers, tested and securely wiped before they join your cluster.",
                "Non. Les hôtes sont des serveurs physiques dédiés, testés et effacés de façon sécurisée avant de rejoindre votre grappe."))],
          trans=("If Microsoft runs the platform, what exactly stays with your team? That is the next slide.",
                 "Si Microsoft exploite la plateforme, qu'est-ce qui reste exactement à votre équipe? C'est la prochaine diapositive.")),
    layer="arch")

# ---------------------------------------------------------------- 5. Shared responsibility
u = "srm"
d = ""
rows = [
    ("ms", "Azure datacenters, power, racks and network hardware", "Centres de données Azure, électricité, baies et matériel réseau"),
    ("ms", "Bare-metal hosts: health monitoring and failed-host replacement", "Hôtes physiques&nbsp;: surveillance de la santé et remplacement des hôtes en panne"),
    ("ms", "ESXi, vCenter, vSAN, NSX: deployment, patching, upgrades", "ESXi, vCenter, vSAN, NSX&nbsp;: déploiement, correctifs, mises à niveau"),
    ("ms", "NSX provider setup and backup of vCenter and NSX configuration", "Configuration NSX du fournisseur et sauvegarde de la configuration vCenter et NSX"),
    ("cu", "Azure networking: virtual network, gateways, firewall, route tables, NSGs, DNS", "Réseau Azure&nbsp;: réseau virtuel, passerelles, pare-feu, tables de routage, NSG, DNS"),
    ("cu", "NSX workload segments, gateway and distributed firewall rules, NAT", "Segments NSX des charges, règles de pare-feu de passerelle et distribué, NAT"),
    ("cu", "HCX Connector, service mesh, network extension, HCX upgrades on both sides", "HCX Connector, Service Mesh, extension réseau, mises à niveau HCX des deux côtés"),
    ("cu", "vSAN storage policies, capacity headroom, identity and access", "Stratégies de stockage vSAN, marge de capacité, identités et accès"),
    ("cu", "VMs, guest OS, applications, patching, antivirus", "VM, système d'exploitation invité, applications, correctifs, antivirus"),
    ("pa", "Workload backup and disaster recovery (with partner solutions)", "Sauvegarde des charges et reprise après sinistre (avec des solutions de partenaires)"),
]
RH, RS = 48, 55
y = 10
for kind, en, fr in reversed(rows):
    cls = {"ms": "srm-ms", "cu": "srm-cu", "pa": "srm-pa"}[kind]
    d += rect(230, y, 1200, RH, cls, 4)
    fill = "#FFFFFF" if kind == "ms" else "#0B2545"
    d += st(254, y + RH / 2, en, fr, 20, 500, anchor="start", fill=fill)
    y += RS
# brackets
def bracket(y1, y2, en, fr, color):
    return (f'<path d="M218,{y1} L202,{y1} L202,{y2} L218,{y2}" fill="none" stroke="{color}" stroke-width="3"/>'
            + st(186, (y1 + y2) / 2, en, fr, 21, 700, anchor="end", fill=color, lh=25))
# rows reversed: partner at top, customer next 5 rows, microsoft bottom 4
top = lambda k: 10 + k * RS
d += bracket(top(0), top(0) + RH, ["You +", "partners"], ["Vous +", "partenaires"], "#42566E")
d += bracket(top(1), top(5) + RH, "You", "Vous", "#0B2545")
d += bracket(top(6), top(9) + RH, "Microsoft", "Microsoft", "#0078D4")
srm = figure(svg(1440, top(9) + RH + 10, d, "Shared responsibility: Microsoft runs hardware and the VMware platform; you run networking configuration, HCX, workloads",
                 "Responsabilité partagée&nbsp;: Microsoft exploite le matériel et la plateforme VMware; vous gérez la configuration réseau, HCX et les charges", uid=u),
             "Microsoft owns the bottom of the stack; your team owns configuration and everything that runs on it.",
             "Microsoft est responsable du bas de la pile; votre équipe est responsable de la configuration et de tout ce qui s'exécute dessus.")
add("responsibility", "intro", ("Who does what: shared responsibility", "Qui fait quoi&nbsp;: la responsabilité partagée"),
    srm + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/introduction#azure-vmware-solution-responsibility-matrix---microsoft-vs-customer",
                "Responsibility matrix", "Matrice de responsabilités")),
    notes("2 min",
          [("Microsoft owns everything in blue: the physical layer, the hosts, and the lifecycle of ESXi, vCenter, vSAN and NSX, including backups of the vCenter and NSX configuration.",
            "Microsoft est responsable de tout ce qui est en bleu&nbsp;: la couche physique, les hôtes et le cycle de vie d'ESXi, vCenter, vSAN et NSX, y compris la sauvegarde de la configuration vCenter et NSX."),
           ("Your team keeps the work that creates value: network design and security, workloads, and data protection. Your VMware skills carry over directly.",
            "Votre équipe garde le travail qui crée de la valeur&nbsp;: conception et sécurité réseau, charges de travail et protection des données. Vos compétences VMware se transfèrent directement."),
           ("Two items people miss: HCX upgrades are yours on both sides, and keeping enough free vSAN capacity is yours too.",
            "Deux éléments souvent oubliés&nbsp;: les mises à niveau HCX vous reviennent des deux côtés, et le maintien d'une capacité vSAN libre suffisante aussi.")],
          qa=[(("Who patches ESXi, and when?", "Qui applique les correctifs ESXi, et quand?"),
               ("Microsoft. You get notices through Azure Service Health, and Maintenance Orchestrator in the portal lets you schedule or reschedule maintenance windows.",
                "Microsoft. Vous recevez des avis par Azure Service Health, et Maintenance Orchestrator dans le portail permet de planifier ou de reporter les fenêtres de maintenance.")),
              (("Do we get full admin rights?", "Avons-nous tous les droits d'administration?"),
               ("You get the CloudAdmin role in vCenter and NSX. Privileged operations, such as adding an LDAPS identity source or changing certain storage settings, go through Run Command in the Azure portal.",
                "Vous obtenez le rôle CloudAdmin dans vCenter et NSX. Les opérations privilégiées, comme l'ajout d'une source d'identité LDAPS ou certains réglages de stockage, passent par Run Command dans le portail Azure."))],
          trans=("Now, the foundation of everything else: connectivity.", "Passons maintenant à la fondation de tout le reste&nbsp;: la connectivité.")),
    layer="exec")
