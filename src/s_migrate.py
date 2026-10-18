from lib import *

# ---------------------------------------------------------------- divider
add("div-migrate", "migrate", ("Migrate with HCX", "Migrer avec HCX"),
    tb("p", "Move running VMs without re-platforming, and choose per application whether to keep or change IP addresses.",
       "Déplacez des VM en marche sans changer de plateforme, et choisissez par application de conserver ou de changer les adresses IP.", "promise"),
    notes("30 s",
          [("This is the longest section because it holds the most decisions: migration type, network extension, re-IP and wave planning.",
            "C'est la plus longue section parce qu'elle contient le plus de décisions&nbsp;: type de migration, extension réseau, réadressage IP et planification des vagues.")],
          trans=("The short version first.", "D'abord la version courte.")),
    kind="divider")

# ---------------------------------------------------------------- exec + eli5
ex = panel("Executive summary", "Sommaire pour la direction", ul([
    ("<b>HCX Enterprise is included</b> with AVS: no extra license for the migration tooling.",
     "<b>HCX Enterprise est inclus</b> avec AVS&nbsp;: aucune licence supplémentaire pour l'outil de migration."),
    ("<b>Zero-downtime options</b> for critical applications, and scheduled parallel migration for scale.",
     "<b>Des options sans interruption</b> pour les applications critiques, et une migration parallèle planifiée pour le volume."),
    ("<b>Keep IP addresses</b> with Layer-2 network extension, or <b>re-IP during the move</b>: decided per application.",
     "<b>Conservez les adresses IP</b> grâce à l'extension réseau de couche 2, ou <b>réadressez pendant le déplacement</b>&nbsp;: décidé par application."),
    ("<b>Built-in safety net</b>: Bulk Migration keeps the source VM for rollback, and HCX can migrate back to your datacenter.",
     "<b>Un filet de sécurité intégré</b>&nbsp;: Bulk Migration conserve la VM source pour un retour arrière, et HCX peut migrer de nouveau vers votre centre de données."),
], "big"), "p-exec")
el = panel("ELI5", "En termes simples", tb("p",
    "HCX is a moving company with a private, armoured tunnel between your old house and your new one. It can carry the TV while it is still playing (vMotion), pack whole rooms overnight and unpack them in the morning (Bulk Migration), and forward your mail from the old address until everyone knows the new one (network extension).",
    "HCX est une entreprise de déménagement avec un tunnel privé et blindé entre votre ancienne maison et la nouvelle. Elle peut transporter le téléviseur pendant qu'il joue encore (vMotion), emballer des pièces entières pendant la nuit et les déballer le matin (Bulk Migration), et faire suivre votre courrier de l'ancienne adresse jusqu'à ce que tout le monde connaisse la nouvelle (extension réseau).", "eli5-text"), "p-eli5")
add("migrate-exec", "migrate", ("Migration, in plain terms", "La migration, simplement"),
    f'<div class="grid g-55-45">{ex}{el}</div>'
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/architecture-migrate", "HCX migration options", "Options de migration HCX")),
    notes("3 min",
          [("Three messages for decision makers: the tooling is included, critical apps can move without downtime, and every move has a way back.",
            "Trois messages pour les décideurs&nbsp;: l'outil est inclus, les applications critiques peuvent migrer sans interruption, et chaque déplacement a un chemin de retour."),
           ("The IP decision is a business decision as much as a technical one: keeping IPs is faster to start; changing them gives a cleaner end state. We will look at both.",
            "La décision sur les IP est autant d'affaires que technique&nbsp;: conserver les IP permet de démarrer plus vite; les changer donne un état final plus propre. Nous verrons les deux."),
           ("Be honest about one Gen 2 detail: Microsoft notes that Bulk and Replication Assisted vMotion can be slower during their sync phases on Gen 2 today, so we plan longer replication windows. vMotion remains fast where it fits.",
            "Soyez honnête sur un détail Gen 2&nbsp;: Microsoft indique que Bulk et Replication Assisted vMotion peuvent être plus lents pendant leurs phases de synchronisation sur Gen 2 actuellement; nous prévoyons donc des fenêtres de réplication plus longues. vMotion reste rapide quand il convient.")],
          qa=[(("How long will the whole migration take?", "Combien de temps prendra la migration complète?"),
               ("It depends on data volume, bandwidth and how many VMs your teams can validate per window. We will do the math in the performance section; most programs start with a pilot and then run regular waves.",
                "Cela dépend du volume de données, de la bande passante et du nombre de VM que vos équipes peuvent valider par fenêtre. Nous ferons le calcul dans la section performance; la plupart des programmes commencent par un pilote, puis des vagues régulières."))],
          trans=("Let's open the hood and see how HCX connects the two sites.", "Ouvrons le capot pour voir comment HCX relie les deux sites.")),
    layer="exec")

# ---------------------------------------------------------------- HCX architecture
u = "hcx"
d = ""
d += rect(10, 40, 500, 440, "bx-onprem-f", 10)
d += st(260, 66, "Your datacenter (source)", "Votre centre de données (source)", 19, 700, fill="#0B2545")
d += box(30, 90, 190, 56, "vCenter", "vCenter", "bx", 17, 600)
d += box(250, 90, 240, 56, "HCX Connector", "HCX Connector", "bx-hcx", 17, 600, sub=("you deploy the OVA", "vous déployez l'OVA"), subsize=13)
d += rect(30, 170, 460, 230, "bx-group", 8)
d += st(260, 192, "Service mesh appliances", "Appliances du Service Mesh", 15, 600, fill="#42566E")
d += box(50, 210, 420, 56, "IX: Interconnect", "IX&nbsp;: Interconnect", "bx", 16, 600, sub=("migration, vMotion, replication", "migration, vMotion, réplication"), subsize=13)
d += box(50, 276, 420, 46, "WAN-OPT (optional)", "WAN-OPT (facultatif)", "bx-soft", 15, 500)
d += box(50, 332, 420, 56, "NE: Network Extension", "NE&nbsp;: Network Extension", "bx", 16, 600, sub=("Layer-2 extension", "extension de couche 2"), subsize=13)
d += st(260, 440, "Network profiles: management, uplink, vMotion, replication", "Profils réseau&nbsp;: gestion, liaison montante, vMotion, réplication", 14, 500, fill="#42566E")
# AVS side
d += rect(930, 40, 500, 440, "bx-vnet", 10)
d += st(1180, 66, "AVS Gen 2 (destination)", "AVS Gen 2 (destination)", 19, 700, fill="#0078D4")
d += box(950, 90, 460, 56, "HCX Cloud Manager", "HCX Cloud Manager", "bx-hcx", 17, 600, sub=("deployed by Microsoft as an add-on", "déployé par Microsoft comme module"), subsize=13)
d += rect(950, 170, 460, 230, "bx-group", 8)
d += st(1180, 192, "Service mesh appliances", "Appliances du Service Mesh", 15, 600, fill="#42566E")
d += box(970, 210, 420, 56, "IX: Interconnect", "IX&nbsp;: Interconnect", "bx", 16, 600)
d += box(970, 276, 420, 46, "WAN-OPT (optional)", "WAN-OPT (facultatif)", "bx-soft", 15, 500)
d += box(970, 332, 420, 56, "NE: Network Extension", "NE&nbsp;: Network Extension", "bx", 16, 600, sub=("bridges to an NSX segment", "relie un segment NSX"), subsize=13)
d += st(1180, 440, "Gen 2: HCX management /24 and uplink /24", "Gen 2&nbsp;: HCX gestion /24 et liaison montante /24", 14, 500, fill="#42566E")
# underlay band
d += rect(530, 160, 380, 250, "bx-underlay", 8)
d += st(720, 390, "ExpressRoute or VPN underlay", "Réseau sous-jacent ExpressRoute ou VPN", 14, 600, fill="#42566E")
# links
d += line(490, 118, 948, 118, "ln", "a", u, both=True)
d += st(720, 102, "site pairing: HTTPS 443", "appairage de sites&nbsp;: HTTPS 443", 15, 600, fill="#0B2545")
d += line(470, 238, 968, 238, "ln-tun", "b", u, both=True)
d += st(720, 222, "IPsec tunnel, UDP 4500: migrations", "Tunnel IPsec, UDP 4500&nbsp;: migrations", 15, 600, fill="#0078D4")
d += line(470, 360, 968, 360, "ln-tun", "b", u, both=True)
d += st(720, 344, "IPsec tunnel, UDP 4500: extended L2", "Tunnel IPsec, UDP 4500&nbsp;: L2 étendue", 15, 600, fill="#0078D4")
hcxfig = figure(svg(1440, 490, d, "HCX: Connector pairs with Cloud Manager over HTTPS; IX and NE appliances build IPsec tunnels over UDP 4500 across the underlay",
                    "HCX&nbsp;: le Connector s'appaire au Cloud Manager en HTTPS; les appliances IX et NE créent des tunnels IPsec sur UDP 4500 par le réseau sous-jacent", uid=u),
                "The managers talk over HTTPS; the appliances carry the data in their own encrypted tunnels.",
                "Les gestionnaires communiquent en HTTPS; les appliances transportent les données dans leurs propres tunnels chiffrés.", "fig-tight")
defs = ('<div class="defs">'
        + '<div><b>' + t("Site pair", "Paire de sites") + '</b>' + t("Trust between Connector and Cloud Manager.", "Relation de confiance entre Connector et Cloud Manager.") + '</div>'
        + '<div><b>' + t("Network profile", "Profil réseau") + '</b>' + t("IP pools the appliances use on each network.", "Plages IP utilisées par les appliances sur chaque réseau.") + '</div>'
        + '<div><b>' + t("Compute profile", "Profil de calcul") + '</b>' + t("Which clusters, datastores and services to enable.", "Quelles grappes, banques de données et services activer.") + '</div>'
        + '<div><b>' + t("Service mesh", "Service Mesh") + '</b>' + t("Pairs two compute profiles and deploys the appliances.", "Associe deux profils de calcul et déploie les appliances.") + '</div>'
        + '</div>')
add("hcx-arch", "migrate", ("How HCX connects the two sites", "Comment HCX relie les deux sites"),
    hcxfig + defs,
    notes("3 min",
          [("Two managers and a set of appliances. You deploy the HCX Connector in your datacenter; Microsoft deploys the HCX Cloud Manager in AVS when you enable the add-on.",
            "Deux gestionnaires et un ensemble d'appliances. Vous déployez HCX Connector dans votre centre de données; Microsoft déploie HCX Cloud Manager dans AVS quand vous activez le module."),
           ("The service mesh deploys matching appliances on both sides: IX for migrations, NE to stretch networks, and optionally WAN Optimization for constrained links.",
            "Le Service Mesh déploie des appliances jumelles des deux côtés&nbsp;: IX pour les migrations, NE pour étendre les réseaux, et facultativement WAN Optimization pour les liens limités."),
           ("For your firewall team: HTTPS 443 between managers, UDP 4500 in both directions between IX and NE appliances, and TCP/UDP 5201 if you want the built-in bandwidth tests to work.",
            "Pour votre équipe pare-feu&nbsp;: HTTPS 443 entre les gestionnaires, UDP 4500 dans les deux sens entre les appliances IX et NE, et TCP/UDP 5201 pour que les tests de bande passante intégrés fonctionnent.")],
          qa=[(("Is migration traffic encrypted?", "Le trafic de migration est-il chiffré?"),
               ("Yes. HCX builds its own IPsec tunnels between appliances, even over ExpressRoute.",
                "Oui. HCX crée ses propres tunnels IPsec entre les appliances, même sur ExpressRoute."))],
          trans=("HCX offers five ways to move a VM. Here is how to choose.", "HCX offre cinq façons de déplacer une VM. Voici comment choisir.")),
    layer="arch")

# ---------------------------------------------------------------- migration types decision
u = "mt"
d = ""
qs = [("Is the source vSphere?", "La source est-elle vSphere?"),
      ("Is the VM powered off?", "La VM est-elle éteinte?"),
      ("Can it reboot in a window?", "Peut-elle redémarrer en fenêtre?"),
      ("Many VMs at once?", "Plusieurs VM à la fois?")]
outs = [("OS Assisted Migration", "OS Assisted Migration", ("Hyper-V and KVM sources", "sources Hyper-V et KVM"), "bx"),
        ("Cold Migration", "Cold Migration", ("simple copy", "copie simple"), "bx"),
        ("Bulk Migration", "Bulk Migration", ("parallel; can re-IP", "parallèle; réadressage possible"), "bx-pick"),
        ("Replication Assisted vMotion", "Replication Assisted vMotion", ("parallel and live", "parallèle et à chaud"), "bx-pick2")]
branch = [("No", "Non"), ("Yes", "Oui"), ("Yes", "Oui"), ("Yes", "Oui")]
cont = [("Yes", "Oui"), ("No", "Non"), ("No", "Non"), ("No", "Non")]
for i, (q, o, b, c) in enumerate(zip(qs, outs, branch, cont)):
    y = 14 + i * 108
    d += box(10, y, 330, 60, q[0], q[1], "bx-q", 17, 600)
    d += box(430, y, 320, 60, o[0], o[1], o[3], 16, 600, sub=o[2], subsize=13)
    d += line(340, y + 30, 428, y + 30, "ln", "a", u)
    d += st(384, y + 16, b[0], b[1], 14, 700, fill="#0078D4")
    d += line(175, y + 60, 175, y + 106, "ln", "a", u)
    d += st(186, y + 84, c[0], c[1], 14, 700, anchor="start", fill="#0078D4")
d += box(10, 446, 330, 60, "HCX vMotion", "HCX vMotion", "bx-pick2", 16, 600, sub=("live, one at a time", "à chaud, une à la fois"), subsize=13)
tree = figure(svg(760, 516, d, "Decision tree for HCX migration types", "Arbre de décision des types de migration HCX", uid=u),
              "Answer four questions to pick the migration type for each VM or group.",
              "Répondez à quatre questions pour choisir le type de migration de chaque VM ou groupe.", "fig-tight")
mtab = table(
    [("Type", "Type"), ("Downtime", "Interruption"), ("Parallel", "Parallèle"), ("Re-IP in move", "Réadressage au déplacement")],
    [
        [("HCX vMotion", "HCX vMotion"), ("None", "Aucune"), ("No, serial", "Non, en série"), ("No", "Non")],
        [("Replication Assisted vMotion", "Replication Assisted vMotion"), ("None", "Aucune"), ("Yes", "Oui"), ("No", "Non")],
        [("Bulk Migration", "Bulk Migration"), ("One reboot", "Un redémarrage"), ("Yes", "Oui"), ("<b>Yes</b>", "<b>Oui</b>")],
        [("Cold Migration", "Cold Migration"), ("VM already off", "VM déjà éteinte"), ("Limited", "Limité"), ("No", "Non")],
        [("OS Assisted Migration", "OS Assisted Migration"), ("Reboot (conversion)", "Redémarrage (conversion)"), ("Yes", "Oui"), ("—", "—")],
    ], "tbl tbl-sm", colw=["34%", "24%", "20%", "22%"])
gen2 = callout("warn", "Gen 2 note:", "Note Gen 2&nbsp;:",
               "Microsoft reports that Bulk and RAV can stall during base and online sync on Gen 2. Plan longer replication windows; use vMotion where it fits.",
               "Microsoft signale que Bulk et RAV peuvent ralentir pendant la synchronisation initiale et continue sur Gen 2. Prévoyez des fenêtres de réplication plus longues; utilisez vMotion quand il convient.")
add("migration-types", "migrate", ("Choosing the right migration type", "Choisir le bon type de migration"),
    f'<div class="grid g-52-48">{tree}<div class="stack">{mtab}{gen2}</div></div>'
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/architecture-migrate", "HCX migration options", "Options de migration HCX"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-design-consideration#limitations", "Gen 2 limitations", "Limites de Gen 2")),
    notes("4 min",
          [("Walk the tree. Not vSphere? OS Assisted Migration. Already off? Cold. Can it take a reboot during a window? Bulk. That is usually the majority of an estate.",
            "Parcourez l'arbre. Pas vSphere? OS Assisted Migration. Déjà éteinte? Cold. Peut-elle redémarrer pendant une fenêtre? Bulk. C'est en général la majorité d'un parc."),
           ("For VMs that cannot go down: Replication Assisted vMotion when you have many of them, HCX vMotion for a handful, because HCX vMotion runs one at a time per service mesh.",
            "Pour les VM qui ne peuvent pas s'arrêter&nbsp;: Replication Assisted vMotion quand elles sont nombreuses, HCX vMotion pour quelques-unes, parce que HCX vMotion s'exécute une à la fois par Service Mesh."),
           ("Note the last column: only Bulk Migration can change the IP address during the move. That links directly to the re-IP discussion coming up.",
            "Notez la dernière colonne&nbsp;: seule Bulk Migration peut changer l'adresse IP pendant le déplacement. Cela mène directement à la discussion sur le réadressage.")],
          qa=[(("Which VMs cannot be migrated live?", "Quelles VM ne peuvent pas migrer à chaud?"),
               ("Typical blockers: hardware version below 9, mounted ISOs, vSphere VM encryption, and some disk modes such as virtual-compatibility RDM, which needs Bulk. We find these in the assessment.",
                "Bloqueurs typiques&nbsp;: version matérielle inférieure à 9, ISO montés, chiffrement de VM vSphere et certains modes de disque comme le RDM en compatibilité virtuelle, qui exige Bulk. Nous les repérons pendant l'évaluation."))],
          trans=("For the engineers, here is the setup sequence in Gen 2.", "Pour les ingénieurs, voici la séquence de configuration dans Gen 2.")),
    layer="decide")

# ---------------------------------------------------------------- HCX setup (deep)
steps = ol([
    ("Portal: private cloud, Add-ons, Migration using HCX, <b>Enable and deploy</b>; provide the HCX management and uplink /24s.",
     "Portail&nbsp;: nuage privé, Modules complémentaires, Migration avec HCX, <b>Activer et déployer</b>; fournissez les /24 de gestion et de liaison montante HCX."),
    ("Copy the HCX Enterprise activation key generated by <b>this</b> private cloud.",
     "Copiez la clé d'activation HCX Enterprise générée par <b>ce</b> nuage privé."),
    ("Download the HCX Connector OVA from HCX Cloud Manager and deploy it in your datacenter.",
     "Téléchargez l'OVA de HCX Connector depuis HCX Cloud Manager et déployez-le dans votre centre de données."),
    ("Activate the Connector with the key; confirm the edition shows Enterprise.",
     "Activez le Connector avec la clé; vérifiez que l'édition affichée est Enterprise."),
    ("Site pair the Connector to HCX Cloud Manager (an IP address works in Gen 2) with CloudAdmin credentials.",
     "Appairez le Connector à HCX Cloud Manager (une adresse IP fonctionne dans Gen 2) avec les identifiants CloudAdmin."),
    ("Create network profiles on both sides: MTU 1500 on ExpressRoute, 1350 on VPN.",
     "Créez les profils réseau des deux côtés&nbsp;: MTU 1500 sur ExpressRoute, 1350 sur VPN."),
    ("Create compute profiles: services, clusters, datastores.",
     "Créez les profils de calcul&nbsp;: services, grappes, banques de données."),
    ("Create the service mesh; it deploys IX, NE and optional WAN-OPT.",
     "Créez le Service Mesh; il déploie IX, NE et le WAN-OPT facultatif."),
    ("Validate: service mesh diagnostics, then Transport Analytics for bandwidth, latency and loss.",
     "Validez&nbsp;: diagnostics du Service Mesh, puis Transport Analytics pour la bande passante, la latence et la perte."),
    ("Extend a test network and migrate a pilot VM in each direction.",
     "Étendez un réseau de test et migrez une VM pilote dans chaque sens."),
], "steps")
ports = table(
    [("From", "De"), ("To", "Vers"), ("Port", "Port")],
    [
        [("HCX Connector", "HCX Connector"), ("HCX Cloud Manager", "HCX Cloud Manager"), "TCP 443, 9443"],
        [("IX and NE (both sites)", "IX et NE (deux sites)"), ("Peer IX and NE", "IX et NE homologues"), ("UDP 4500, both directions", "UDP 4500, deux sens")],
        [("IX and NE", "IX et NE"), ("Peer IX and NE", "IX et NE homologues"), ("TCP/UDP 5201 (diagnostics)", "TCP/UDP 5201 (diagnostics)")],
        [("HCX Manager", "HCX Manager"), ("Local IX", "IX local"), "TCP 8123, 9443"],
        [("HCX Manager, IX", "HCX Manager, IX"), ("Local ESXi hosts", "Hôtes ESXi locaux"), "TCP 80, 443, 902"],
        [("HCX Connector", "HCX Connector"), "connect.hcx.vmware.com", "TCP 443"],
    ], "tbl tbl-sm", colw=["34%", "36%", "30%"])
add("hcx-setup", "migrate", ("HCX setup in Gen 2: ten steps", "Configuration HCX dans Gen 2&nbsp;: dix étapes"),
    f'<div class="grid g-58-42">{steps}<div class="stack">' + tb("h3", "Ports to open", "Ports à ouvrir", "minor") + ports + '</div></div>'
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/install-vmware-hcx", "Install HCX", "Installer HCX"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/configure-vmware-hcx", "Configure HCX Connector", "Configurer HCX Connector"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/tutorial-network-checklist#required-network-ports", "Full port list", "Liste complète des ports")),
    notes("3 min",
          [("Ten steps, and most teams finish the first five in a day once the network is in place.",
            "Dix étapes, et la plupart des équipes terminent les cinq premières en une journée une fois le réseau en place."),
           ("Two things specific to Gen 2: you provide two /24 subnets when you enable HCX, and you can pair using an IP address.",
            "Deux éléments propres à Gen 2&nbsp;: vous fournissez deux sous-réseaux /24 en activant HCX, et vous pouvez appairer par adresse IP."),
           ("Step 9 is the one people skip and regret. Run diagnostics and Transport Analytics before migrating anything; they tell you if the underlay meets the HCX minimums.",
            "L'étape 9 est celle qu'on saute et qu'on regrette. Lancez les diagnostics et Transport Analytics avant toute migration; ils indiquent si le réseau sous-jacent respecte les minimums HCX.")],
          qa=[(("We already run HCX for another cloud. Can we reuse that Connector?", "Nous utilisons déjà HCX pour un autre nuage. Pouvons-nous réutiliser ce Connector?"),
               ("Use the activation key from the AVS private cloud you are pairing with, and make sure the Connector is licensed as Enterprise; otherwise features like Replication Assisted vMotion stay hidden.",
                "Utilisez la clé d'activation du nuage privé AVS avec lequel vous vous appairez, et assurez-vous que le Connector est licencié en Enterprise; sinon, des fonctions comme Replication Assisted vMotion restent masquées."))],
          trans=("Now the question everyone asks: can we keep our IP addresses?", "Maintenant, la question que tout le monde pose&nbsp;: pouvons-nous conserver nos adresses IP?")),
    layer="deep", skip=True)

# ---------------------------------------------------------------- Network extension & MON (deep)
u = "mon"
d = ""
def ext_panel(ox, mon):
    s = ""
    title = (("With MON", "Avec MON") if mon else ("Extension without MON", "Extension sans MON"))
    s += st(ox + 350, 18, title[0], title[1], 18, 700, fill="#1E7B3A" if mon else "#9A5B00")
    s += rect(ox + 10, 40, 220, 220, "bx-onprem-f", 8)
    s += st(ox + 120, 62, "Datacenter", "Centre de données", 15, 700, fill="#0B2545")
    s += box(ox + 30, 82, 180, 52, "Default gateway", "Passerelle par défaut", "bx", 15, 600)
    s += box(ox + 30, 190, 180, 48, "NE", "NE", "bx", 15, 600)
    s += rect(ox + 420, 40, 270, 220, "bx-vnet", 8)
    s += st(ox + 555, 62, "AVS Gen 2", "AVS Gen 2", 15, 700, fill="#0078D4")
    s += box(ox + 440, 82, 230, 52, "NSX Tier-1", "NSX Tier-1", "bx-nsx", 15, 600)
    s += box(ox + 440, 190, 90, 48, "NE", "NE", "bx", 15, 600)
    s += box(ox + 545, 190, 125, 48, "Migrated VM", "VM migrée", "bx-pick", 14, 600)
    s += box(ox + 250, 300, 200, 48, "Azure services", "Services Azure", "bx-soft", 15, 600)
    s += line(ox + 230, 214, ox + 438, 214, "ln-tun", None, u)
    s += st(ox + 334, 200, "L2 tunnel", "tunnel L2", 13, 500, fill="#0078D4")
    if not mon:
        s += line(ox + 543, 222, ox + 532, 222, "ln-w", "w", u)
        s += line(ox + 440, 228, ox + 232, 228, "ln-w", "w", u)
        s += line(ox + 120, 190, ox + 120, 136, "ln-w", "w", u)
        s += path(f"M{ox + 210},120 C{ox + 300},150 {ox + 300},250 {ox + 330},298", "ln-w", "w", u)
        s += st(ox + 120, 312, ["routed back", "over ExpressRoute"], ["retour par", "ExpressRoute"], 15, 600, fill="#9A5B00", lh=18)
    else:
        s += line(ox + 607, 188, ox + 607, 136, "ln-g", "g", u)
        s += path(f"M{ox + 440},112 C{ox + 380},112 {ox + 400},324 {ox + 452},324", "ln-g", "g", u)
        s += st(ox + 598, 162, "/32 host route", "route hôte /32", 15, 600, anchor="end", fill="#1E7B3A")
    return s
d += ext_panel(0, False)
d += ext_panel(740, True)
monfig = figure(svg(1440, 356, d, "Without MON, traffic from a migrated VM hairpins to the datacenter gateway; with MON it is routed locally by NSX",
                    "Sans MON, le trafic d'une VM migrée fait l'aller-retour vers la passerelle du centre de données; avec MON, NSX l'achemine localement", uid=u),
                "The extension keeps the IP; MON removes the detour through your datacenter for traffic to Azure.",
                "L'extension conserve l'IP; MON supprime le détour par votre centre de données pour le trafic vers Azure.", "fig-tight")
monb = ul([
    ("Extension keeps IP and MAC. The gateway stays in your datacenter until you cut it over to NSX; only then is the segment programmed into the virtual network.",
     "L'extension conserve l'IP et l'adresse MAC. La passerelle reste dans votre centre de données jusqu'à la bascule vers NSX; c'est seulement alors que le segment est programmé dans le réseau virtuel."),
    ("Gen 2 limits for MON: each /32 counts toward the 1,000-prefix limit; a /32 from a peered network needs a support request; no MON between two Gen 2 clouds.",
     "Limites MON dans Gen 2&nbsp;: chaque /32 compte dans la limite de 1&nbsp;000 préfixes; un /32 depuis un réseau appairé exige une demande de support; pas de MON entre deux nuages Gen 2."),
    ("Treat extension as a bridge, not a destination: enable NE high availability, move app tiers together, then cut over the gateway and remove the extension.",
     "Voyez l'extension comme un pont, pas une destination&nbsp;: activez la haute disponibilité NE, déplacez les niveaux d'une application ensemble, puis basculez la passerelle et retirez l'extension."),
], "dense cols2")
add("extension-mon", "migrate", ("Keeping IPs: Layer-2 extension and MON", "Conserver les IP&nbsp;: extension de couche 2 et MON"),
    monfig + monb
    + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-routing-architecture#route-limitations-for-hcx", "Gen 2 HCX route limits", "Limites de routage HCX Gen 2")),
    notes("3 min",
          [("Network extension stretches a subnet from your datacenter into AVS, so a VM keeps its IP and MAC. Simple, and it lets you move VMs one by one.",
            "L'extension réseau étire un sous-réseau de votre centre de données vers AVS; une VM conserve donc son IP et son adresse MAC. Simple, et cela permet de déplacer les VM une à une."),
           ("The catch is on the left: the default gateway is still in your datacenter, so a migrated VM talking to Azure goes back to your datacenter first. That is the hairpin.",
            "Le hic est à gauche&nbsp;: la passerelle par défaut est toujours dans votre centre de données; une VM migrée qui parle à Azure repasse donc d'abord par votre centre de données. C'est l'aller-retour."),
           ("MON fixes that by routing locally in NSX with host routes. In Gen 2, those /32 routes count toward the route limit, so we use MON selectively and keep extensions temporary.",
            "MON corrige cela en routant localement dans NSX avec des routes d'hôte. Dans Gen 2, ces routes /32 comptent dans la limite de routage; nous utilisons donc MON de façon sélective et gardons les extensions temporaires.")],
          qa=[(("How long can we leave networks extended?", "Combien de temps pouvons-nous garder les réseaux étendus?"),
               ("Technically for a long time, but every extension is a dependency on both sites and on the tunnel. Plan the gateway cutover per subnet as part of the wave plan.",
                "Techniquement longtemps, mais chaque extension crée une dépendance aux deux sites et au tunnel. Planifiez la bascule de passerelle par sous-réseau dans le plan de vagues."))],
          trans=("Which brings us to the alternative: changing the IP address.", "Ce qui nous amène à l'autre option&nbsp;: changer l'adresse IP.")),
    layer="deep", skip=True)

# ---------------------------------------------------------------- Re-IP decision
u = "reip"
d = ""
lanes = [
    (("Keep IP", "Conserver l'IP"), "#0078D4", [
        (["Extend the network", "with HCX"], ["Étendre le réseau", "avec HCX"]),
        (["Migrate VMs", "(vMotion, RAV, Bulk)"], ["Migrer les VM", "(vMotion, RAV, Bulk)"]),
        (["Optional:", "enable MON"], ["Facultatif&nbsp;:", "activer MON"]),
        (["Cut over the", "gateway to NSX"], ["Basculer la", "passerelle vers NSX"]),
        (["Remove the", "extension"], ["Retirer", "l'extension"]),
    ]),
    (("Re-IP", "Réadresser"), "#1E7B3A", [
        (["Create the new", "NSX segment"], ["Créer le nouveau", "segment NSX"]),
        (["Lower DNS TTL,", "map dependencies"], ["Réduire le TTL DNS,", "cartographier"]),
        (["Bulk Migration", "with new IP"], ["Bulk Migration", "avec nouvelle IP"]),
        (["Update DNS, firewall,", "load balancers"], ["Mettre à jour DNS,", "pare-feu, répartiteurs"]),
        (["Validate, then", "decommission"], ["Valider, puis", "mettre hors service"]),
    ]),
]
for li, (name, color, stepsl) in enumerate(lanes):
    y = 10 + li * 110
    d += st(70, y + 40, name[0], name[1], 19, 700, fill=color)
    for i, (en, fr) in enumerate(stepsl):
        x = 160 + i * 256
        d += rect(x, y, 228, 80, "bx-lane" + str(li), 6)
        d += st(x + 114, y + 40, en, fr, 15, 500, fill="#0B2545", lh=19)
        if i < 4:
            d += line(x + 228, y + 40, x + 254, y + 40, "ln", "a", u)
lanefig = figure(svg(1440, 200, d, "Two paths: keep the IP with network extension, or re-IP with Bulk Migration guest customization",
                     "Deux chemins&nbsp;: conserver l'IP avec l'extension réseau, ou réadresser avec la personnalisation invitée de Bulk Migration", uid=u),
                 "Both paths end in the same place: VMs on native NSX segments, with no dependency on your datacenter.",
                 "Les deux chemins mènent au même endroit&nbsp;: des VM sur des segments NSX natifs, sans dépendance à votre centre de données.", "fig-tight")
reip_when = panel("Choose re-IP when", "Choisissez de réadresser quand", ul([
    ("Ranges overlap with Azure or must be redesigned anyway", "Les plages chevauchent Azure ou doivent être revues de toute façon"),
    ("You want no dependency on extension tunnels or hairpin latency", "Vous ne voulez aucune dépendance aux tunnels d'extension ni à la latence d'aller-retour"),
    ("Many subnets would need MON, pushing Gen 2 route limits", "Beaucoup de sous-réseaux exigeraient MON et approcheraient les limites de routage Gen 2"),
    ("Apps use DNS names, not hard-coded IPs", "Les applications utilisent des noms DNS, pas des IP codées en dur"),
], "dense"), "p-green")
keep_when = panel("Keep the IP when", "Conservez l'IP quand", ul([
    ("IPs are hard-coded or tied to licenses", "Les IP sont codées en dur ou liées à des licences"),
    ("Partners allow-list your IPs and changes take weeks", "Des partenaires filtrent vos IP et les changements prennent des semaines"),
    ("The timeline is tight or the app cannot be touched", "L'échéancier est serré ou l'application ne peut pas être modifiée"),
    ("You will move the whole subnet and cut over its gateway", "Vous déplacerez tout le sous-réseau et basculerez sa passerelle"),
], "dense"), "p-blue")
eli = callout("eli5", "ELI5:", "En termes simples&nbsp;:",
              "keeping your IP is like forwarding mail from your old address: easy, but every letter takes a detour. Re-IP is changing your address: some paperwork up front, then mail arrives directly.",
              "conserver votre IP, c'est comme faire suivre le courrier de votre ancienne adresse&nbsp;: facile, mais chaque lettre fait un détour. Réadresser, c'est changer d'adresse&nbsp;: un peu de paperasse au départ, puis le courrier arrive directement.")
add("reip-decision", "migrate", ("Keep the IP or change it? Decide per application", "Conserver l'IP ou la changer? Décider par application"),
    lanefig + f'<div class="grid g-34-33-33">{eli}{reip_when}{keep_when}</div>',
    notes("4 min",
          [("Both paths are fully supported and both end with your VMs on native AVS networks. The difference is when you pay the effort: later with extension, upfront with re-IP.",
            "Les deux chemins sont entièrement pris en charge et mènent tous deux à des VM sur des réseaux AVS natifs. La différence est le moment de l'effort&nbsp;: plus tard avec l'extension, au départ avec le réadressage."),
           ("Re-IP with HCX happens inside Bulk Migration: HCX applies the new IP, gateway and DNS at switchover. No separate tool.",
            "Le réadressage avec HCX se fait dans Bulk Migration&nbsp;: HCX applique la nouvelle IP, la passerelle et le DNS à la bascule. Aucun outil distinct."),
           ("Our usual recommendation is a mix: keep IPs for the few apps with hard-coded addresses or partner allow-lists, re-IP standard servers that use DNS names. We make that call per app during the assessment.",
            "Notre recommandation habituelle est un mélange&nbsp;: conserver les IP pour les quelques applications aux adresses codées en dur ou filtrées par des partenaires, réadresser les serveurs standard qui utilisent des noms DNS. Nous tranchons application par application pendant l'évaluation.")],
          qa=[(("Will changing the IP break domain membership?", "Changer l'IP va-t-il briser l'appartenance au domaine?"),
               ("No, as long as the hostname and SID stay the same. Keep the HCX option to generate a new SID turned off for domain-joined servers, and update DNS records.",
                "Non, tant que le nom d'hôte et le SID restent les mêmes. Laissez désactivée l'option HCX qui génère un nouveau SID pour les serveurs joints au domaine, et mettez à jour les enregistrements DNS.")),
              (("Can we re-IP VMs moved with vMotion?", "Peut-on réadresser des VM déplacées avec vMotion?"),
               ("Not during the move. Migrate first, then change the IP with a script through VMware Tools, Ansible or Azure Arc; there is an example in the appendix.",
                "Pas pendant le déplacement. Migrez d'abord, puis changez l'IP avec un script par VMware Tools, Ansible ou Azure Arc; un exemple figure en annexe."))],
          trans=("For the engineers, here is the re-IP runbook and the dependency checklist.", "Pour les ingénieurs, voici la procédure de réadressage et la liste de vérification des dépendances.")),
    layer="decide")

# ---------------------------------------------------------------- Re-IP runbook (deep)
c1 = panel("During the move: Bulk Migration", "Pendant le déplacement&nbsp;: Bulk Migration", ul([
    ("Guest customization sets hostname, IP, netmask, gateway, DNS servers and suffix.", "La personnalisation invitée définit le nom d'hôte, l'IP, le masque, la passerelle, les serveurs DNS et le suffixe."),
    ("Optional pre and post scripts, up to 1,500 characters.", "Scripts avant et après facultatifs, jusqu'à 1&nbsp;500 caractères."),
    ("Applied at switchover, with one extra reboot.", "Appliquée à la bascule, avec un redémarrage de plus."),
    ("Leave <b>Generate new SID</b> off for domain-joined servers.", "Laissez <b>Générer un nouveau SID</b> désactivé pour les serveurs joints au domaine."),
    ("Check the supported guest OS list for your HCX version.", "Vérifiez la liste des systèmes invités pris en charge pour votre version de HCX."),
], "dense"), "p-green")
c2 = panel("After the move: scripted", "Après le déplacement&nbsp;: par script", ul([
    ("For vMotion, RAV, or a guest OS that customization does not support.", "Pour vMotion, RAV ou un système invité non pris en charge par la personnalisation."),
    ("Run through VMware Tools (PowerCLI <code>Invoke-VMScript</code>), Ansible, or Azure Arc run command.", "Exécution par VMware Tools (PowerCLI <code>Invoke-VMScript</code>), Ansible ou la commande d'exécution Azure Arc."),
    ("Script it once, test on the pilot, reuse per wave.", "Écrivez-le une fois, testez-le au pilote, réutilisez-le à chaque vague."),
], "dense"), "p-blue")
c3 = panel("Dependency checklist", "Liste de vérification des dépendances", ul([
    ("DNS A and PTR records; lower TTL a week before", "Enregistrements DNS A et PTR; TTL réduit une semaine avant"),
    ("Firewall rules: datacenter, Azure Firewall, NSX DFW", "Règles de pare-feu&nbsp;: site, Azure Firewall, DFW NSX"),
    ("Load balancer pools and health probes", "Groupes et sondes des répartiteurs de charge"),
    ("Hard-coded IPs in configs, connection strings, hosts files", "IP codées en dur dans les configurations, chaînes de connexion, fichiers hosts"),
    ("AD Sites and Services subnets", "Sous-réseaux d'AD Sites and Services"),
    ("Monitoring, backup and EDR agents", "Agents de surveillance, de sauvegarde et EDR"),
    ("Licenses bound to IP or MAC; certificates with IP SANs", "Licences liées à l'IP ou au MAC; certificats avec SAN d'IP"),
    ("Partner allow-lists and NFS/SMB export rules", "Listes d'autorisation partenaires et règles d'export NFS/SMB"),
], "dense"), "p-deep")
g = callout("warn", "Gotcha:", "Piège&nbsp;:",
            "HCX does not keep the original guest settings, and empty fields are cleared once IP customization is on. Fill every field, including the DNS suffix. Bulk keeps the source VM powered off for rollback.",
            "HCX ne conserve pas les paramètres invités d'origine, et les champs vides sont effacés dès que la personnalisation IP est activée. Remplissez tous les champs, y compris le suffixe DNS. Bulk garde la VM source éteinte pour un retour arrière.")
add("reip-runbook", "migrate", ("Re-IP runbook with HCX", "Procédure de réadressage IP avec HCX"),
    f'<div class="grid g-33-27-40">{c1}{c2}{c3}</div>' + g
    + refs(("https://docs.vmware.com/en/VMware-HCX/4.7/hcx-user-guide/GUID-5667495D-9BFD-4531-8DFE-E7CF6BFB6CF9.html", "HCX guest customization", "Personnalisation invitée HCX"),
           ("https://knowledge.broadcom.com/external/article/400603/ip-customization-failing-for-windows-ser.html", "Broadcom KB 400603 (Windows IP customization)", "KB Broadcom 400603 (personnalisation IP Windows)")),
    notes("3 min",
          [("Left: what HCX does for you during a Bulk Migration. Middle: what you script when HCX cannot do it. Right: the list that actually decides whether a re-IP goes smoothly.",
            "À gauche&nbsp;: ce que HCX fait pour vous pendant une Bulk Migration. Au centre&nbsp;: ce que vous scriptez quand HCX ne peut pas le faire. À droite&nbsp;: la liste qui détermine vraiment si un réadressage se passe bien."),
           ("The IP change itself is the easy part. Most re-IP incidents come from a forgotten dependency: a firewall rule, a load balancer pool, or an IP written in a config file.",
            "Le changement d'IP lui-même est la partie facile. La plupart des incidents viennent d'une dépendance oubliée&nbsp;: une règle de pare-feu, un groupe de répartiteur de charge ou une IP écrite dans un fichier de configuration."),
           ("Lower DNS TTLs a week ahead so clients pick up new records within minutes after switchover.",
            "Réduisez les TTL DNS une semaine à l'avance pour que les clients voient les nouveaux enregistrements quelques minutes après la bascule.")],
          qa=[(("What if a Windows version is not on the customization list?", "Et si une version de Windows n'est pas sur la liste de personnalisation?"),
               ("Migrate without customization and apply the new IP with the script, or upgrade HCX if a newer version adds that OS. Broadcom documents this case.",
                "Migrez sans personnalisation et appliquez la nouvelle IP par script, ou mettez HCX à niveau si une version plus récente ajoute ce système. Broadcom documente ce cas."))],
          trans=("Now let's put migrations into a repeatable rhythm: waves.", "Mettons maintenant les migrations dans un rythme reproductible&nbsp;: les vagues.")),
    layer="deep", skip=True)

# ---------------------------------------------------------------- Waves
u = "wave"
d = ""
chain = [("Assess and group", "Évaluer et regrouper"), ("Pilot wave", "Vague pilote"), ("Wave 1", "Vague 1"), ("Wave 2", "Vague 2"), ("Wave n", "Vague n"), ("Exit datacenter", "Sortie du centre")]
for i, (en, fr) in enumerate(chain):
    x = 6 + i * 246
    d += box(x, 6, 196, 52, en, fr, "bx-pick" if i == 1 else "bx", 17, 600)
    if i < len(chain) - 1:
        d += line(x + 196, 32, x + 244, 32, "ln", "a", u)
d += st(720, 92, "Anatomy of one wave", "Anatomie d'une vague", 17, 700, fill="#42566E")
d += line(30, 160, 1410, 160, "ln-time", None, u)
ms = [("T−7 d", ["Start replication;", "lower DNS TTL"], ["Lancer la réplication;", "réduire le TTL DNS"]),
      ("T−1 d", ["Final checks;", "change freeze"], ["Vérifications finales;", "gel des changements"]),
      ("T0", ["Switchover window;", "smoke tests; sign-off"], ["Fenêtre de bascule;", "tests rapides; approbation"]),
      ("T+2 d", ["Hypercare ends;", "rollback decision"], ["Fin du soutien renforcé;", "décision de retour"]),
      ("T+7 d", ["Remove source VMs", "and extensions"], ["Retirer VM sources", "et extensions"])]
for i, (lab, en, fr) in enumerate(ms):
    x = 150 + i * 285
    d += f'<circle cx="{x}" cy="160" r="11" class="{"dot-on" if i == 2 else "dot"}"/>'
    d += st(x, 130, lab, lab, 19, 700, fill="#0B2545")
    d += st(x, 214, en, fr, 18, 400, fill="#0B2545", lh=23)
wavefig = figure(svg(1440, 248, d, "Wave sequence and the timeline of a single wave from replication start to source removal",
                     "Séquence des vagues et chronologie d'une vague, du début de la réplication au retrait des sources", uid=u),
                 "Replication runs days ahead, so the switchover window is short and predictable.",
                 "La réplication démarre des jours à l'avance; la fenêtre de bascule est donc courte et prévisible.", "fig-tight")
rules = panel("Grouping rules", "Règles de regroupement", ul([
    ("Move application tiers together to avoid cross-site latency.", "Déplacez les niveaux d'une application ensemble pour éviter la latence entre sites."),
    ("Group by subnet so gateways can be cut over sooner.", "Regroupez par sous-réseau pour basculer les passerelles plus tôt."),
    ("Start with stateless, low-risk workloads.", "Commencez par des charges sans état et peu risquées."),
    ("Size waves to bandwidth and to your teams' validation capacity.", "Dimensionnez les vagues selon la bande passante et la capacité de validation de vos équipes."),
    ("Name an application owner who signs off each switchover.", "Nommez un responsable d'application qui approuve chaque bascule."),
], "dense"), "p-deep")
add("waves", "migrate", ("Migrating in waves", "Migrer par vagues"),
    wavefig + f'<div class="grid g-60-40 mt">{rules}<div>'
    + callout("tip", "Rollback:", "Retour arrière&nbsp;:",
              "Bulk Migration keeps the source VM powered off at the source; if validation fails in the window, power it back on. HCX can also migrate VMs back.",
              "Bulk Migration garde la VM source éteinte sur le site source; si la validation échoue pendant la fenêtre, rallumez-la. HCX peut aussi remigrer les VM dans l'autre sens.")
    + '</div></div>',
    notes("3 min",
          [("Waves turn a migration from a big-bang project into a routine. Each wave follows the same timeline, so teams get faster every time.",
            "Les vagues transforment une migration en routine plutôt qu'en grand saut. Chaque vague suit la même chronologie; les équipes gagnent donc en vitesse à chaque fois."),
           ("Replication starts days ahead; the actual switchover is a short, scheduled window. Downtime for Bulk is roughly a reboot.",
            "La réplication démarre des jours à l'avance; la bascule elle-même est une courte fenêtre planifiée. L'interruption avec Bulk correspond à peu près à un redémarrage."),
           ("Start the pilot with 10 to 20 low-risk VMs and grow wave size as confidence builds.",
            "Commencez le pilote avec 10 à 20 VM peu risquées et augmentez la taille des vagues à mesure que la confiance s'installe.")],
          qa=[(("How many VMs per wave?", "Combien de VM par vague?"),
               ("HCX supports up to 200 concurrent Bulk or RAV migrations per service mesh, but the real limits are bandwidth and how many apps your teams can test in one window.",
                "HCX prend en charge jusqu'à 200 migrations Bulk ou RAV simultanées par Service Mesh, mais les vraies limites sont la bande passante et le nombre d'applications que vos équipes peuvent tester dans une fenêtre."))],
          trans=("One more strategic question before we leave migration: AVS or native Azure VMs?", "Une dernière question stratégique avant de quitter la migration&nbsp;: AVS ou des VM Azure natives?")),
    layer="plan")

# ---------------------------------------------------------------- AVS vs Azure VMs
cmp = table(
    [("", ""), ("Azure VMware Solution", "Azure VMware Solution"), ("Native Azure VMs", "VM Azure natives")],
    [
        [("Speed to exit", "Vitesse de sortie"), ("Fast: no conversion", "Rapide&nbsp;: aucune conversion"), ("Per-VM conversion and testing", "Conversion et tests par VM")],
        [("Changes to VMs", "Changements aux VM"), ("None: same hypervisor", "Aucun&nbsp;: même hyperviseur"), ("Drivers, agents, sizes, disks", "Pilotes, agents, tailles, disques")],
        [("Skills and tools", "Compétences et outils"), ("vCenter, NSX, HCX unchanged", "vCenter, NSX, HCX inchangés"), ("Azure-native operations", "Exploitation native Azure")],
        [("Unit you pay for", "Unité facturée"), ("Dedicated hosts (3+ AV64)", "Hôtes dédiés (3+ AV64)"), ("Each VM size", "Chaque taille de VM")],
        [("Best fit", "Meilleur usage"), ("Large estates, deadlines, vSphere-certified apps, IP retention", "Grands parcs, échéances, applications certifiées vSphere, conservation des IP"), ("Right-sizing, modernization, smaller or elastic estates", "Ajustement de taille, modernisation, parcs plus petits ou élastiques")],
        [("Migration tool", "Outil de migration"), "HCX", "Azure Migrate"],
    ], "tbl tbl-lg", colw=["22%", "39%", "39%"])
path_html = ('<div class="route">'
             + '<span>' + t("Datacenter", "Centre de données") + '</span><i></i>'
             + '<span class="on">' + t("AVS first: exit fast", "AVS d'abord&nbsp;: sortir vite") + '</span><i></i>'
             + '<span>' + t("Modernize selected apps to Azure VMs or PaaS", "Moderniser certaines applications vers des VM Azure ou du PaaS") + '</span></div>')
add("avs-vs-iaas", "migrate", ("AVS or native Azure VMs? Often both", "AVS ou VM Azure natives? Souvent les deux"),
    cmp + path_html
    + refs(("https://learn.microsoft.com/en-us/azure/migrate/how-to-create-azure-vmware-solution-assessment", "Azure Migrate AVS assessment", "Évaluation AVS d'Azure Migrate")),
    notes("3 min",
          [("This is a portfolio decision, not a religious one. AVS wins when speed and zero change matter; native Azure VMs win when you want to right-size and modernize each workload.",
            "C'est une décision de portefeuille, pas de principe. AVS l'emporte quand la vitesse et l'absence de changement comptent; les VM Azure natives l'emportent quand vous voulez ajuster et moderniser chaque charge."),
           ("A single Azure Migrate discovery can produce both an AVS assessment, with a node count and monthly estimate, and an Azure VM assessment. Compare them side by side.",
            "Une seule découverte Azure Migrate peut produire à la fois une évaluation AVS, avec un nombre de nœuds et une estimation mensuelle, et une évaluation de VM Azure. Comparez-les côte à côte."),
           ("The common path: AVS first to leave the datacenter on time, then modernize selected apps gradually, since AVS already sits in the same Azure network.",
            "Le chemin fréquent&nbsp;: AVS d'abord pour quitter le centre de données à temps, puis moderniser certaines applications graduellement, puisque AVS est déjà dans le même réseau Azure.")],
          qa=[(("Doesn't AVS lock us into VMware?", "AVS ne nous enferme-t-il pas dans VMware?"),
               ("It keeps VMware where it helps you move fast. Because AVS lives in your Azure network, modernizing an app later is an Azure-to-Azure move, not another datacenter project.",
                "Il garde VMware là où cela vous aide à aller vite. Comme AVS vit dans votre réseau Azure, moderniser une application plus tard devient un déplacement d'Azure à Azure, pas un autre projet de centre de données."))],
          trans=("Once workloads are in AVS, what does day-to-day life look like?", "Une fois les charges dans AVS, à quoi ressemble le quotidien?")),
    layer="decide")
