from lib import *

# ---------------------------------------------------------------- divider
add("div-connect", "connect", ("Hybrid connectivity", "Connectivité hybride"),
    tb("p", "Gen 2 is one more spoke in your Azure network.", "Gen 2 n'est qu'un réseau satellite (spoke) de plus dans votre réseau Azure.", "promise"),
    notes("30 s",
          [("This section answers one question: how does traffic get between your datacenter, Azure and AVS, safely and fast enough to migrate?",
            "Cette section répond à une question&nbsp;: comment le trafic circule-t-il entre votre centre de données, Azure et AVS, de façon sûre et assez rapide pour migrer?")],
          trans=("First, the short version for decision makers.", "D'abord, la version courte pour les décideurs.")),
    kind="divider")

# ---------------------------------------------------------------- exec + eli5
ex = panel("Executive summary", "Sommaire pour la direction", ul([
    ("AVS Gen 2 is deployed <b>inside an Azure virtual network</b>. It connects like any other spoke: peering, your existing ExpressRoute or VPN, your existing firewall.",
     "AVS Gen 2 est déployé <b>dans un réseau virtuel Azure</b>. Il se connecte comme tout autre réseau satellite&nbsp;: appairage, votre ExpressRoute ou VPN existant, votre pare-feu existant."),
    ("No separate circuit to design around: <b>reuse your hub</b>, security controls and monitoring.",
     "Aucun circuit distinct à concevoir&nbsp;: <b>réutilisez votre hub</b>, vos contrôles de sécurité et votre surveillance."),
    ("One decision you cannot change later: <b>non-overlapping IP ranges</b> for the private cloud, HCX and your workload segments.",
     "Une décision impossible à changer plus tard&nbsp;: des <b>plages IP sans chevauchement</b> pour le nuage privé, HCX et vos segments de charges."),
    ("<b>ExpressRoute is recommended</b> for migration traffic. Site-to-site VPN works, but is slower and more sensitive to packet size.",
     "<b>ExpressRoute est recommandé</b> pour le trafic de migration. Le VPN de site à site fonctionne, mais il est plus lent et plus sensible à la taille des paquets."),
], "big"), "p-exec")
el = panel("ELI5", "En termes simples", tb("p",
    "Your company campus already has a gate (ExpressRoute), security guards (Azure Firewall) and hallways (network peering). Gen 2 builds the new VMware wing inside the fence, so it uses the same gate, guards and hallways. The only thing to plan carefully is the room numbers (IP addresses), so that no two rooms share a number.",
    "Le campus de votre entreprise a déjà une barrière (ExpressRoute), des gardiens (Azure Firewall) et des corridors (l'appairage réseau). Gen 2 construit la nouvelle aile VMware à l'intérieur de la clôture&nbsp;: elle utilise donc la même barrière, les mêmes gardiens et les mêmes corridors. La seule chose à bien planifier, ce sont les numéros de local (les adresses IP), pour que deux locaux n'aient jamais le même numéro.", "eli5-text"), "p-eli5")
add("connect-exec", "connect", ("Connectivity, in plain terms", "La connectivité, simplement"),
    f'<div class="grid g-55-45">{ex}{el}</div>',
    notes("3 min",
          [("The biggest simplification in Gen 2: AVS is not a separate network island. It sits in a virtual network you own, so your network team uses the tools and patterns they already know.",
            "La plus grande simplification de Gen 2&nbsp;: AVS n'est pas un îlot réseau séparé. Il réside dans un réseau virtuel qui vous appartient; votre équipe réseau utilise donc les outils et modèles qu'elle connaît déjà."),
           ("The only irreversible decision is IP planning. Get the ranges right once and everything else can evolve.",
            "La seule décision irréversible, c'est le plan d'adressage IP. Choisissez bien les plages une fois et tout le reste peut évoluer."),
           ("Ask now: what do you have today? An ExpressRoute circuit, its bandwidth and provider, an Azure hub, which firewall vendor?",
            "Demandez maintenant&nbsp;: qu'avez-vous aujourd'hui? Un circuit ExpressRoute, sa bande passante et son fournisseur, un hub Azure, quel fournisseur de pare-feu?")],
          qa=[(("Do we need a new ExpressRoute circuit?", "Faut-il un nouveau circuit ExpressRoute?"),
               ("Not necessarily. Your existing circuit and gateway can carry AVS traffic if there is enough bandwidth. Check the gateway size: it is often the real limit, not the circuit.",
                "Pas nécessairement. Votre circuit et votre passerelle existants peuvent transporter le trafic AVS s'il y a assez de bande passante. Vérifiez la taille de la passerelle&nbsp;: c'est souvent la vraie limite, pas le circuit.")),
              (("Can we start with VPN?", "Pouvons-nous commencer avec un VPN?"),
               ("Yes, for a pilot or a small estate, or as a backup path. For HCX over VPN, lower the uplink MTU to 1350 and expect lower throughput.",
                "Oui, pour un projet pilote ou un petit parc, ou comme chemin de secours. Pour HCX sur VPN, abaissez le MTU de liaison montante à 1350 et attendez-vous à un débit plus faible."))],
          trans=("Here is the reference topology most of our customers end up with.", "Voici la topologie de référence que la plupart de nos clients adoptent.")),
    layer="exec")

# ---------------------------------------------------------------- topology
u = "topo"
d = ""
# on-prem
d += rect(10, 70, 280, 450, "bx-onprem-f", 10)
d += st(150, 96, "Your datacenter", "Votre centre de données", 19, 700, fill="#0B2545")
for i, (en, fr) in enumerate([("vSphere clusters", "Grappes vSphere"), ("HCX Connector, IX, NE", "HCX Connector, IX, NE"),
                              ("DNS and Active Directory", "DNS et Active Directory"), ("Edge router (BGP)", "Routeur de bordure (BGP)")]):
    d += box(30, 120 + i * 66, 240, 50, en, fr, "bx", 16, 500)
# hub
d += rect(450, 70, 340, 300, "bx-hub", 10)
d += st(620, 96, "Hub virtual network", "Réseau virtuel hub", 19, 700, fill="#0B2545")
d += box(470, 120, 300, 50, "ExpressRoute gateway", "Passerelle ExpressRoute", "bx", 16, 500)
d += box(470, 186, 300, 50, "VPN gateway (backup path)", "Passerelle VPN (chemin de secours)", "bx", 16, 500)
d += box(470, 252, 300, 50, "Azure Firewall or partner NVA", "Azure Firewall ou NVA partenaire", "bx-fw", 16, 600)
d += st(620, 336, "GatewaySubnet route table → firewall", "Table du GatewaySubnet → pare-feu", 14, 400, fill="#42566E")
# spokes
d += box(450, 420, 340, 100, "Spoke virtual networks", "Réseaux virtuels satellites", "bx-soft", 17, 600,
         sub=("apps, private endpoints to PaaS", "applications, points de terminaison privés PaaS"))
d += line(620, 370, 620, 418, "ln", "a", u, both=True)
d += st(632, 394, "peering", "appairage", 14, 400, anchor="start", fill="#42566E")
# internet
d += pill(620, 26, "Internet", "Internet", 150, 16, "pill-net")
d += line(620, 70, 620, 42, "ln-g", "g", u)
d += st(632, 56, "egress through the firewall", "sortie par le pare-feu", 14, 400, anchor="start", fill="#1E7B3A")
# AVS vnet
d += rect(950, 70, 480, 450, "bx-vnet", 10)
d += st(1190, 96, "AVS Gen 2 virtual network", "Réseau virtuel AVS Gen 2", 19, 700, fill="#0078D4")
inner = [
    ("avs-mgmt: vCenter, NSX Manager, HCX Manager", "avs-mgmt&nbsp;: vCenter, NSX Manager, HCX Manager", "bx"),
    ("avs-nsx-gw ×2: traffic leaving AVS", "avs-nsx-gw ×2&nbsp;: trafic sortant d'AVS", "bx"),
    ("avs-network-infra-gw: traffic into NSX", "avs-network-infra-gw&nbsp;: trafic entrant vers NSX", "bx"),
    ("NSX Tier-0 and Tier-1 gateways", "Passerelles NSX Tier-0 et Tier-1", "bx-nsx"),
]
for i, (en, fr, c) in enumerate(inner):
    d += box(966, 116 + i * 54, 448, 44, en, fr, c, 15, 500)
segs = [("App segment", "Segment applis"), ("DB segment", "Segment BD"), ("Extended (HCX)", "Étendu (HCX)")]
for i, (en, fr) in enumerate(segs):
    d += box(966 + i * 152, 336, 144, 40, en, fr, "bx-seg", 14, 500)
d += box(966, 392, 448, 44, "HCX management /24 and uplink /24", "HCX gestion /24 et liaison montante /24", "bx", 15, 500)
d += box(966, 450, 448, 44, "DNS Private Resolver (2 × /28)", "DNS Private Resolver (2 × /28)", "bx", 15, 500)
# links on-prem <-> hub
d += line(290, 145, 448, 145, "ln-er", "a", u, both=True)
d += st(369, 116, ["ExpressRoute", "private peering"], ["ExpressRoute", "appairage privé"], 14, 600, fill="#0B2545", lh=17)
d += line(290, 211, 448, 211, "ln", "a", u, both=True, dash=True)
d += st(369, 232, "site-to-site VPN", "VPN de site à site", 14, 400, fill="#42566E")
# hub <-> avs
d += line(790, 230, 948, 230, "ln-er", "a", u, both=True)
d += st(869, 196, ["VNet peering", "gateway transit"], ["appairage de réseaux", "transit de passerelle"], 14, 600, fill="#0B2545", lh=17)
topo = figure(svg(1440, 530, d, "Reference topology: datacenter to hub virtual network over ExpressRoute, hub peered to the AVS Gen 2 virtual network",
                  "Topologie de référence&nbsp;: centre de données vers le réseau virtuel hub par ExpressRoute, hub appairé au réseau virtuel AVS Gen 2", uid=u),
              "Traffic from your datacenter enters through the hub gateways, passes the firewall and reaches NSX segments over peering. AVS creates and manages the avs-* subnets.",
              "Le trafic de votre centre de données entre par les passerelles du hub, traverse le pare-feu et atteint les segments NSX par appairage. AVS crée et gère les sous-réseaux avs-*.")
add("topology", "connect", ("Reference topology: hub-and-spoke with AVS Gen 2", "Topologie de référence&nbsp;: hub-and-spoke avec AVS Gen 2"),
    topo + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-design-consideration", "Gen 2 design considerations", "Considérations de conception Gen 2"),
                ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-connect-on-premises", "Connect Gen 2 to on-premises", "Relier Gen 2 au site")),
    notes("4 min",
          [("Read left to right. Your datacenter connects to the hub with ExpressRoute, with VPN as a backup path. The hub holds the gateways and the firewall.",
            "Lisez de gauche à droite. Votre centre de données se connecte au hub par ExpressRoute, avec un VPN comme chemin de secours. Le hub contient les passerelles et le pare-feu."),
           ("The AVS virtual network is peered to the hub. Inside it, AVS creates and manages its own subnets, for management, for traffic leaving AVS and for traffic entering NSX. You do not edit those subnets.",
            "Le réseau virtuel AVS est appairé au hub. À l'intérieur, AVS crée et gère ses propres sous-réseaux&nbsp;: gestion, trafic sortant d'AVS et trafic entrant vers NSX. Vous ne modifiez pas ces sous-réseaux."),
           ("Variant: Virtual WAN works too, as long as the virtual hub is in the same region as the AVS virtual network; another region needs a support request.",
            "Variante&nbsp;: Virtual WAN fonctionne aussi, à condition que le hub virtuel soit dans la même région que le réseau virtuel AVS; une autre région exige une demande de support."),
           ("Constraints to mention: one private cloud per virtual network and per resource group, the private cloud and its virtual network in the same resource group, and global peering or ExpressRoute FastPath through a support request.",
            "Contraintes à mentionner&nbsp;: un nuage privé par réseau virtuel et par groupe de ressources, le nuage privé et son réseau virtuel dans le même groupe de ressources, et l'appairage mondial ou ExpressRoute FastPath sur demande de support.")],
          qa=[(("Can we use our existing Palo Alto or Fortinet appliances?", "Pouvons-nous utiliser nos appareils Palo Alto ou Fortinet existants?"),
               ("Yes. Standard Azure topologies with third-party network virtual appliances are supported; the route tables go in the same places as with Azure Firewall.",
                "Oui. Les topologies Azure standard avec des appliances virtuelles de partenaires sont prises en charge; les tables de routage se placent aux mêmes endroits qu'avec Azure Firewall.")),
              (("Is there anything Gen 2 cannot do on the network side?", "Y a-t-il des choses que Gen 2 ne peut pas faire côté réseau?"),
               ("A few, today: no public IP directly on the NSX edge, no Azure NAT Gateway, no subnet peering, and no service endpoints from AVS workloads. Internet goes through your firewall instead.",
                "Quelques-unes, pour l'instant&nbsp;: pas d'IP publique directement sur la bordure NSX, pas d'Azure NAT Gateway, pas d'appairage de sous-réseaux et pas de points de terminaison de service depuis les charges AVS. L'accès Internet passe plutôt par votre pare-feu."))],
          trans=("Everything in this picture depends on a clean IP plan, so let's look at that.", "Tout ce schéma repose sur un plan IP propre; regardons-le.")),
    layer="arch")

# ---------------------------------------------------------------- IP plan
ipt = table(
    [("Block", "Bloc"), ("Size", "Taille"), ("Purpose", "Usage"), ("Example", "Exemple")],
    [
        [("Private cloud", "Nuage privé"), "/22", ("Management, vMotion, vSAN and NSX gateway subnets, created and managed by AVS", "Sous-réseaux de gestion, vMotion, vSAN et passerelles NSX, créés et gérés par AVS"), "<code>10.100.0.0/22</code>"],
        [("HCX management", "HCX gestion"), "/24", ("HCX appliance management (required in Gen 2)", "Gestion des appliances HCX (exigé dans Gen 2)"), "<code>10.100.4.0/24</code>"],
        [("HCX uplink", "HCX liaison montante"), "/24", ("IX and NE tunnels to your datacenter", "Tunnels IX et NE vers votre centre de données"), "<code>10.100.5.0/24</code>"],
        [("DNS Private Resolver", "DNS Private Resolver"), "2 × /28", ("Inbound and outbound endpoints for a private DNS zone", "Points de terminaison entrant et sortant pour une zone DNS privée"), "<code>10.100.6.0/28</code>, <code>.16/28</code>"],
        [("NSX workload segments", "Segments NSX des charges"), ("/24 each, typically", "/24 chacun, en général"), ("Your VM networks; each one is added to the virtual network address space", "Vos réseaux de VM; chacun est ajouté à l'espace d'adressage du réseau virtuel"), "<code>10.110.0.0/16</code>"],
        [("Hub", "Hub"), "/27, /26", ("GatewaySubnet and AzureFirewallSubnet", "GatewaySubnet et AzureFirewallSubnet"), ("in the hub network", "dans le réseau hub")],
    ], "tbl", colw=["21%", "13%", "46%", "20%"])
rules = panel("Rules that avoid rework", "Règles qui évitent de refaire le travail", ul([
    ("RFC 1918 ranges only, excluding <code>172.17.0.0/16</code>. No overlap with your datacenter or other virtual networks, except subnets you deliberately extend with HCX.",
     "Plages RFC 1918 seulement, sauf <code>172.17.0.0/16</code>. Aucun chevauchement avec votre centre de données ou d'autres réseaux virtuels, sauf les sous-réseaux que vous étendez volontairement avec HCX."),
    ("Avoid NSX-reserved ranges: <code>169.254.0.0/24</code>, <code>169.254.2.0/23</code>, <code>100.64.0.0/16</code>, <code>100.73.x.x</code>.",
     "Évitez les plages réservées par NSX&nbsp;: <code>169.254.0.0/24</code>, <code>169.254.2.0/23</code>, <code>100.64.0.0/16</code>, <code>100.73.x.x</code>."),
    ("Never edit the avs-* subnets or reuse the /22 for anything else. It cannot be changed after deployment.",
     "Ne modifiez jamais les sous-réseaux avs-* et ne réutilisez pas le /22 pour autre chose. Il ne peut pas être changé après le déploiement."),
    ("Route scale: at most 1,000 prefixes in the virtual network address space, including /32 routes. Segments are split into /28s: 4,096 per 3-host cloud, 6,144 with 4 hosts. Prefer fewer, larger prefixes.",
     "Échelle de routage&nbsp;: au plus 1&nbsp;000 préfixes dans l'espace d'adressage du réseau virtuel, routes /32 comprises. Les segments sont découpés en /28&nbsp;: 4&nbsp;096 pour un nuage de 3 hôtes, 6&nbsp;144 avec 4 hôtes. Privilégiez moins de préfixes, mais plus grands."),
], "dense"), "p-deep")
add("ip-plan", "connect", ("IP plan: decide once, before deployment", "Plan d'adressage IP&nbsp;: décider une fois, avant le déploiement"),
    f'<div class="grid g-58-42">{ipt}{rules}</div>'
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-design-consideration#routing-and-subnet-considerations", "Gen 2 subnets", "Sous-réseaux Gen 2"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-routing-architecture", "Gen 2 route limits", "Limites de routage Gen 2")),
    notes("3 min",
          [("This is the slide to photograph. Gen 2 needs a /22 for the private cloud plus two /24s for HCX management and uplink, then whatever you need for workload segments.",
            "C'est la diapositive à photographier. Gen 2 exige un /22 pour le nuage privé, plus deux /24 pour la gestion et la liaison montante HCX, puis ce qu'il vous faut pour les segments de charges."),
           ("Each NSX segment you create is added to the Azure virtual network address space automatically. That is what makes the network feel native, and it is also why route scale matters.",
            "Chaque segment NSX que vous créez est ajouté automatiquement à l'espace d'adressage du réseau virtuel Azure. C'est ce qui rend le réseau natif, et c'est aussi pourquoi l'échelle de routage compte."),
           ("Practical advice: reserve one large, summarizable block for AVS workloads, such as a /16, and carve /24s from it.",
            "Conseil pratique&nbsp;: réservez un grand bloc agrégeable pour les charges AVS, comme un /16, et découpez-y des /24.")],
          qa=[(("Can we change the /22 later?", "Pouvons-nous changer le /22 plus tard?"),
               ("No, so we validate it in a workshop before deployment. Workload segments, on the other hand, can be added at any time.",
                "Non; c'est pourquoi nous le validons en atelier avant le déploiement. Les segments de charges, eux, peuvent être ajoutés en tout temps.")),
              (("Why do we need two extra /24s?", "Pourquoi deux /24 supplémentaires?"),
               ("Gen 2 requires dedicated HCX management and uplink subnets, in addition to the /22 you give at deployment.",
                "Gen 2 exige des sous-réseaux HCX dédiés à la gestion et à la liaison montante, en plus du /22 fourni au déploiement."))],
          trans=("With addresses planned, the next question is how traffic is routed and inspected.", "Une fois les adresses planifiées, la question suivante est de savoir comment le trafic est acheminé et inspecté.")),
    layer="deep", skip=True)

# ---------------------------------------------------------------- routing
u = "rt"
d = ""
d += rect(10, 90, 130, 330, "bx-onprem-f", 8)
d += st(75, 255, ["Your", "datacenter"], ["Votre centre", "de données"], 17, 700, fill="#0B2545")
d += rect(190, 60, 250, 390, "bx-hub", 8)
d += st(315, 82, "Hub", "Hub", 17, 700, fill="#0B2545")
d += box(205, 110, 220, 70, "GatewaySubnet", "GatewaySubnet", "bx", 16, 600, sub=("route table: NSX prefixes", "table : préfixes NSX"), subsize=14)
d += box(205, 240, 220, 70, "Firewall or NVA", "Pare-feu ou NVA", "bx-fw", 16, 600)
d += box(205, 370, 220, 56, "Internet", "Internet", "bx-soft", 16, 600)
d += rect(480, 60, 410, 390, "bx-vnet", 8)
d += st(685, 82, "AVS Gen 2 virtual network", "Réseau virtuel AVS Gen 2", 17, 700, fill="#0078D4")
d += box(495, 110, 230, 70, "avs-network-infra-gw", "avs-network-infra-gw", "bx", 15, 600, sub=("inbound: no route table", "entrant : aucune table"), subsize=14)
d += box(495, 240, 230, 70, "avs-nsx-gw, avs-nsx-gw-1", "avs-nsx-gw, avs-nsx-gw-1", "bx", 15, 600, sub=("outbound: route table here", "sortant : table ici"), subsize=14)
d += box(495, 366, 230, 64, "avs-mgmt", "avs-mgmt", "bx", 15, 600, sub=("vCenter, NSX, HCX Manager", "vCenter, NSX, HCX Manager"), subsize=14)
d += box(760, 110, 116, 320, ["NSX", "Tier-0", "Tier-1"], ["NSX", "Tier-0", "Tier-1"], "bx-nsx", 16, 600)
# inbound path (blue)
d += line(140, 135, 203, 135, "ln-b", "b", u)
d += line(290, 180, 290, 238, "ln-b", "b", u)
d += path("M425,258 C455,258 455,145 493,145", "ln-b", "b", u)
d += line(725, 145, 758, 145, "ln-b", "b", u)
# outbound path (green)
d += line(758, 275, 727, 275, "ln-g", "g", u)
d += path("M495,290 C462,290 460,292 427,292", "ln-g", "g", u)
d += line(340, 238, 340, 182, "ln-g", "g", u)
d += line(203, 160, 142, 160, "ln-g", "g", u)
d += line(315, 310, 315, 368, "ln-g", "g", u)
d += st(326, 340, "0.0.0.0/0", "0.0.0.0/0", 14, 600, anchor="start", fill="#1E7B3A")
# legend
d += line(500, 30, 540, 30, "ln-b", "b", u)
d += st(548, 30, "into AVS", "vers AVS", 15, 500, anchor="start", fill="#0078D4")
d += line(660, 30, 700, 30, "ln-g", "g", u)
d += st(708, 30, "out of AVS", "depuis AVS", 15, 500, anchor="start", fill="#1E7B3A")
rt = figure(svg(900, 460, d, "Inbound traffic is steered to the firewall by the GatewaySubnet route table; outbound traffic by the route table on the avs-nsx-gw subnets",
                "Le trafic entrant est dirigé vers le pare-feu par la table du GatewaySubnet; le trafic sortant par la table des sous-réseaux avs-nsx-gw", uid=u),
            "Two route tables control inspection: one on the hub GatewaySubnet (in) and one on the avs-nsx-gw subnets (out).",
            "Deux tables de routage contrôlent l'inspection&nbsp;: une sur le GatewaySubnet du hub (entrant) et une sur les sous-réseaux avs-nsx-gw (sortant).")
gotchas = panel("Gotchas we see in the field", "Pièges observés sur le terrain", ul([
    ("Peering advertises AVS subnets as specific routes. A broad supernet in your GatewaySubnet route table loses on longest-prefix match: <b>list each NSX segment prefix</b>, or traffic bypasses the firewall and returns asymmetrically.",
     "L'appairage annonce les sous-réseaux AVS comme routes précises. Un grand super-réseau dans la table du GatewaySubnet perd (préfixe le plus long)&nbsp;: <b>listez chaque préfixe NSX</b>, sinon le trafic contourne le pare-feu et devient asymétrique."),
    ("<b>Never</b> associate a route table with avs-network-infra-gw.",
     "N'associez <b>jamais</b> de table de routage à avs-network-infra-gw."),
    ("Keep route tables and NSGs in the AVS resource group. References from another group or subscription (route table, DDoS plan) can stop NSX segments from being programmed.",
     "Gardez tables de routage et NSG dans le groupe de ressources AVS. Une référence à un autre groupe ou abonnement (table, plan DDoS) peut bloquer la programmation des segments NSX."),
    ("Azure Policy that enforces NSG or route-table naming can block deployment: exempt the AVS virtual network during deployment.",
     "Une Azure Policy imposant un nommage de NSG ou de tables peut bloquer le déploiement&nbsp;: exemptez le réseau virtuel AVS le temps du déploiement."),
    ("/32 routes (HCX MON, DNS forwarder) work from the local virtual network; from a peered one, open a support request.",
     "Les routes /32 (HCX MON, redirecteur DNS) fonctionnent depuis le réseau virtuel local; depuis un réseau appairé, ouvrez une demande de support."),
], "dense"), "p-warn")
add("routing", "connect", ("Routing and inspection: where route tables go", "Routage et inspection&nbsp;: où placer les tables de routage"),
    f'<div class="grid g-58-42">{rt}{gotchas}</div>'
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-design-consideration#azure-route-table-udr-association-consideration", "Route table guidance", "Consignes sur les tables de routage"),
           ("https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview#how-azure-selects-routes-for-traffic-routing", "How Azure selects routes", "Sélection des routes dans Azure")),
    notes("3 min",
          [("If you inspect traffic, you need two route tables. Inbound: on the hub GatewaySubnet, sending AVS prefixes to the firewall. Outbound: on the two avs-nsx-gw subnets, sending on-premises prefixes and the default route to the firewall.",
            "Pour inspecter le trafic, il faut deux tables de routage. Entrant&nbsp;: sur le GatewaySubnet du hub, envoyant les préfixes AVS au pare-feu. Sortant&nbsp;: sur les deux sous-réseaux avs-nsx-gw, envoyant les préfixes du site et la route par défaut au pare-feu."),
           ("The classic mistake is a single broad route like 10.0.0.0/8. Azure always prefers the most specific route, so the peering routes win and the firewall sees only one direction of the conversation.",
            "L'erreur classique est une seule grande route comme 10.0.0.0/8. Azure préfère toujours la route la plus précise&nbsp;: les routes d'appairage l'emportent et le pare-feu ne voit qu'un sens de la conversation."),
           ("Validate with Network Watcher next hop and effective routes, in both directions, before the first migration.",
            "Validez avec le prochain saut (next hop) de Network Watcher et les routes effectives, dans les deux sens, avant la première migration.")],
          qa=[(("Do we have to inspect east-west traffic between AVS and Azure?", "Faut-il inspecter le trafic est-ouest entre AVS et Azure?"),
               ("It is a policy choice. Many customers inspect north-south and on-premises traffic in the hub, and use the NSX distributed firewall for east-west inside AVS.",
                "C'est un choix de politique. Beaucoup de clients inspectent le trafic nord-sud et vers le site dans le hub, et utilisent le pare-feu distribué NSX pour l'est-ouest à l'intérieur d'AVS."))],
          trans=("Two more things every Gen 2 design must settle: DNS and internet access.", "Deux autres éléments à régler dans toute conception Gen 2&nbsp;: le DNS et l'accès Internet.")),
    layer="deep", skip=True)

# ---------------------------------------------------------------- DNS & internet
u = "dns"
d = ""
d += box(10, 50, 200, 70, "Your DNS servers", "Vos serveurs DNS", "bx-onprem", 16, 600, sub=("datacenter", "centre de données"), subsize=14)
d += box(330, 50, 220, 70, "Resolver inbound", "Résolveur entrant", "bx", 16, 600, sub=("in the AVS VNet", "dans le VNet AVS"), subsize=14)
d += box(640, 50, 190, 70, "Azure DNS", "Azure DNS", "bx-soft", 16, 600, sub=("168.63.129.16", "168.63.129.16"), subsize=14)
d += box(620, 220, 230, 80, ["Private zone", "for the private cloud"], ["Zone privée", "du nuage privé"], "bx-nsx", 15, 600)
d += st(735, 326, "vCenter, NSX, HCX names", "noms vCenter, NSX, HCX", 13, 400, fill="#42566E")
d += box(10, 220, 200, 70, "AVS workload VMs", "VM de charges AVS", "bx", 16, 600)
d += box(330, 220, 220, 70, "NSX DNS forwarder", "Redirecteur DNS NSX", "bx", 16, 600, sub=("FQDN zone", "zone FQDN"), subsize=14)
d += line(210, 85, 328, 85, "ln-b", "b", u)
d += st(269, 32, ["conditional", "forwarder"], ["redirecteur", "conditionnel"], 13, 600, fill="#0078D4", lh=15)
d += line(550, 85, 638, 85, "ln", "a", u)
d += line(735, 120, 735, 218, "ln", "a", u)
d += line(210, 255, 328, 255, "ln", "a", u)
d += line(440, 220, 440, 122, "ln", "a", u)
dns = figure(svg(860, 340, d, "Private DNS: on-premises DNS forwards the private cloud zone to the DNS Private Resolver inbound endpoint, which asks Azure DNS",
                 "DNS privé&nbsp;: le DNS du site redirige la zone du nuage privé vers le point d'entrée du DNS Private Resolver, qui interroge Azure DNS", uid=u),
             "With a private zone, management names resolve only through the resolver in the AVS virtual network.",
             "Avec une zone privée, les noms de gestion se résolvent uniquement par le résolveur du réseau virtuel AVS.")
dns_txt = panel("DNS", "DNS", ul([
    ("<b>Public zone</b>: management names resolve from anywhere (to private IPs).",
     "<b>Zone publique</b>&nbsp;: les noms de gestion se résolvent de partout (vers des IP privées)."),
    ("<b>Private zone</b>: add Azure DNS Private Resolver (two /28) and a conditional forwarder on your DNS servers.",
     "<b>Zone privée</b>&nbsp;: ajoutez Azure DNS Private Resolver (deux /28) et un redirecteur conditionnel sur vos serveurs DNS."),
    ("Do not set custom DNS on the AVS virtual network with a private zone: it breaks scaling, upgrades and patching.",
     "N'utilisez pas de DNS personnalisé sur le réseau virtuel AVS avec une zone privée&nbsp;: cela bloque la mise à l'échelle, les mises à niveau et les correctifs."),
], "dense"), "p-deep")
net_txt = panel("Internet", "Internet", ul([
    ("Off by default. Egress through Azure Firewall, a partner NVA or a Virtual WAN secured hub.",
     "Désactivé par défaut. Sortie par Azure Firewall, une NVA partenaire ou un hub sécurisé Virtual WAN."),
    ("Add <code>0.0.0.0/0</code> to the firewall on avs-nsx-gw and avs-nsx-gw-1 (and avs-mgmt for appliances).",
     "Ajoutez <code>0.0.0.0/0</code> vers le pare-feu sur avs-nsx-gw et avs-nsx-gw-1 (et avs-mgmt pour les appliances)."),
    ("Publish apps with firewall DNAT or Application Gateway. Not in Gen 2: public IP on the NSX edge, Azure NAT Gateway.",
     "Publiez les applications avec le DNAT du pare-feu ou Application Gateway. Non offert dans Gen 2&nbsp;: IP publique sur la bordure NSX, Azure NAT Gateway."),
], "dense"), "p-deep")
add("dns-internet", "connect", ("DNS and internet access", "DNS et accès Internet"),
    f'<div class="grid g-56-44">{dns}<div class="stack">{dns_txt}{net_txt}</div></div>'
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/native-dns-forward-lookup-zone", "Gen 2 DNS zones", "Zones DNS Gen 2"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-internet-connectivity-design-considerations", "Gen 2 internet options", "Options Internet Gen 2")),
    notes("3 min",
          [("DNS first. You choose a public or private zone for the management names. Security-minded customers usually pick private; then the names resolve only inside the AVS virtual network unless you add a resolver.",
            "D'abord le DNS. Vous choisissez une zone publique ou privée pour les noms de gestion. Les clients soucieux de sécurité choisissent en général la zone privée; les noms ne se résolvent alors que dans le réseau virtuel AVS, à moins d'ajouter un résolveur."),
           ("The fix is simple: DNS Private Resolver in the AVS virtual network, and a conditional forwarder for the private cloud zone on your DNS servers. Workload VMs use the NSX DNS forwarder.",
            "La solution est simple&nbsp;: DNS Private Resolver dans le réseau virtuel AVS et un redirecteur conditionnel pour la zone du nuage privé sur vos serveurs DNS. Les VM de charges utilisent le redirecteur DNS NSX."),
           ("Internet: it is off until you turn it on, and in Gen 2 it always goes through a firewall you control. Good for security teams.",
            "Internet&nbsp;: il reste désactivé tant que vous ne l'activez pas, et dans Gen 2 il passe toujours par un pare-feu que vous contrôlez. Une bonne nouvelle pour les équipes de sécurité.")],
          qa=[(("Our servers must keep using our Active Directory DNS.", "Nos serveurs doivent continuer d'utiliser notre DNS Active Directory."),
               ("That is fine. Point the VMs, or the NSX DNS forwarder, at your AD DNS servers, and add the conditional zones you need.",
                "Aucun problème. Pointez les VM, ou le redirecteur DNS NSX, vers vos serveurs DNS AD et ajoutez les zones conditionnelles nécessaires."))],
          trans=("Last connectivity topic: is the link big enough for migration?", "Dernier sujet de connectivité&nbsp;: le lien est-il assez gros pour migrer?")),
    layer="deep", skip=True)

# ---------------------------------------------------------------- link choice & sizing
lt = table(
    [("", ""), ("ExpressRoute", "ExpressRoute"), ("Site-to-site VPN", "VPN de site à site")],
    [
        [("Best for", "Idéal pour"), ("Production and migration waves", "Production et vagues de migration"), ("Pilots, small estates, backup path", "Pilotes, petits parcs, chemin de secours")],
        [("HCX uplink MTU", "MTU liaison montante HCX"), "1500", ("1350 (IPsec overhead)", "1350 (surcoût IPsec)")],
        [("Predictability", "Prévisibilité"), ("Private path with an SLA", "Chemin privé avec SLA"), ("Internet-dependent", "Dépend d'Internet")],
        [("Usual limit", "Limite habituelle"), ("Gateway size, then circuit", "Taille de la passerelle, puis circuit"), ("VPN gateway size, internet quality", "Taille de la passerelle VPN, qualité Internet")],
    ], "tbl", colw=["26%", "37%", "37%"])
gw = table(
    [("ExpressRoute gateway", "Passerelle ExpressRoute"), ("Max bandwidth", "Bande passante max."), ("FastPath", "FastPath")],
    [
        ["ERGw1Az", ("1 Gbps", "1 Gb/s"), ("No", "Non")],
        ["ERGw2Az", ("2 Gbps", "2 Gb/s"), ("No", "Non")],
        ["ErGw3Az", ("10 Gbps", "10 Gb/s"), ("Yes", "Oui")],
        ["ErGwScale", ("1 Gbps per scale unit (1 to 40)", "1 Gb/s par unité (1 à 40)"), ("Yes, from 10 units", "Oui, dès 10 unités")],
    ], "tbl tbl-sm", colw=["34%", "42%", "24%"])
hcxmin = table(
    [("HCX underlay minimum", "Minimum du réseau sous-jacent HCX"), ("vMotion, RAV", "vMotion, RAV"), ("Bulk, OSAM", "Bulk, OSAM")],
    [
        [("Bandwidth", "Bande passante"), ("250 Mbps (150 with WAN Opt.)", "250 Mb/s (150 avec WAN Opt.)"), ("50 Mbps", "50 Mb/s")],
        [("Latency, loss", "Latence, perte"), ("≤ 150 ms, ≤ 0.1%", "≤ 150 ms, ≤ 0,1&nbsp;%"), ("≤ 150 ms, ≤ 1%", "≤ 150 ms, ≤ 1&nbsp;%")],
        [("MTU", "MTU"), "≥ 1150", "≥ 1150"],
    ], "tbl tbl-sm", colw=["34%", "38%", "28%"])
add("link-sizing", "connect", ("Choosing and sizing the link for migration", "Choisir et dimensionner le lien pour la migration"),
    f'<div class="grid g-50-50">{lt}<div class="stack">{gw}{hcxmin}</div></div>'
    + callout("tip", "Rule of thumb:", "Règle pratique&nbsp;:",
              "the gateway is often the hidden bottleneck. A 1 Gbps gateway caps migrations even on a 10 Gbps circuit. FastPath on Gen 2 is enabled through a support request.",
              "la passerelle est souvent le goulot caché. Une passerelle de 1 Gb/s plafonne les migrations même sur un circuit de 10 Gb/s. FastPath sur Gen 2 s'active par demande de support.")
    + refs(("https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-virtual-network-gateways", "ExpressRoute gateway SKUs", "SKU de passerelles ExpressRoute"),
           ("https://techdocs.broadcom.com/us/en/vmware-cis/hcx/vmware-hcx/4-10/vmware-hcx-user-guide-4-10/preparing-for-hcx-installations/network-underlay-minimum-requirements.html", "HCX underlay requirements", "Exigences HCX du réseau sous-jacent")),
    notes("3 min",
          [("Two numbers decide migration speed on the network side: the ExpressRoute gateway size and the HCX minimums. Live migration needs at least 250 megabits per second, or 150 with WAN Optimization; Bulk Migration needs 50.",
            "Deux chiffres déterminent la vitesse de migration côté réseau&nbsp;: la taille de la passerelle ExpressRoute et les minimums HCX. La migration à chaud exige au moins 250 mégabits par seconde, ou 150 avec WAN Optimization; Bulk Migration en exige 50."),
           ("Latency up to 150 milliseconds is supported, which covers Canada-to-Canada regions easily. Packet loss matters more than people expect for vMotion.",
            "Une latence jusqu'à 150 millisecondes est prise en charge, ce qui couvre facilement les liaisons entre régions canadiennes. La perte de paquets compte plus qu'on ne le pense pour vMotion."),
           ("Over VPN, set the HCX uplink MTU to 1350 on both sides, otherwise fragmentation causes random failures.",
            "Sur VPN, réglez le MTU de liaison montante HCX à 1350 des deux côtés, sinon la fragmentation cause des échecs aléatoires.")],
          qa=[(("Will migrations slow down production traffic?", "Les migrations vont-elles ralentir le trafic de production?"),
               ("They share the same circuit, so plan for it: schedule waves, apply QoS on your side, watch circuit and gateway utilization, and use scheduled switchover windows.",
                "Elles partagent le même circuit; il faut donc le prévoir&nbsp;: planifiez les vagues, appliquez de la qualité de service de votre côté, surveillez l'utilisation du circuit et de la passerelle et utilisez des fenêtres de bascule planifiées."))],
          trans=("The network is ready. Let's move some VMs.", "Le réseau est prêt. Déplaçons des VM.")),
    layer="decide")
