from lib import *

# ================================================================ OPERATE
add("div-operate", "operate", ("Day-2 operations", "Exploitation au quotidien"),
    tb("p", "Same vCenter skills. Microsoft handles the hardware and the hypervisor.",
       "Les mêmes compétences vCenter. Microsoft s'occupe du matériel et de l'hyperviseur.", "promise"),
    notes("30 s",
          [("Migration is a project; operations are forever. This section shows what changes for your team, and what does not.",
            "La migration est un projet; l'exploitation, c'est pour toujours. Cette section montre ce qui change pour votre équipe, et ce qui ne change pas.")],
          trans=("The short version.", "La version courte.")),
    kind="divider")

ex = panel("Executive summary", "Sommaire pour la direction", ul([
    ("Your team keeps working in <b>vCenter and NSX</b>. Microsoft patches ESXi, vCenter, vSAN and NSX, and replaces failed hosts.",
     "Votre équipe continue de travailler dans <b>vCenter et NSX</b>. Microsoft applique les correctifs à ESXi, vCenter, vSAN et NSX, et remplace les hôtes en panne."),
    ("<b>Plan maintenance</b> in the Azure portal with Maintenance Orchestrator; notices arrive through Service Health.",
     "<b>Planifiez la maintenance</b> dans le portail Azure avec Maintenance Orchestrator; les avis arrivent par Service Health."),
    ("<b>Scale on demand</b>: add hosts within quota, or add storage without hosts using Azure NetApp Files.",
     "<b>Mise à l'échelle sur demande</b>&nbsp;: ajoutez des hôtes selon votre quota, ou du stockage sans hôtes avec Azure NetApp Files."),
    ("<b>Monitor</b> with Azure Monitor alongside vCenter, and keep vSAN below 75% used to stay within the SLA.",
     "<b>Surveillez</b> avec Azure Monitor en plus de vCenter, et gardez vSAN sous 75&nbsp;% d'utilisation pour respecter le SLA."),
], "big"), "p-exec")
el = panel("ELI5", "En termes simples", tb("p",
    "You still drive the car (vCenter). Microsoft is the pit crew: oil changes, tire swaps and engine updates are their job, and they tell you ahead of time when they need the car. Your job is the route, the passengers and the cargo.",
    "Vous conduisez toujours la voiture (vCenter). Microsoft est l'équipe de mécaniciens&nbsp;: vidanges, changements de pneus et mises à jour du moteur, c'est leur travail, et ils vous préviennent d'avance quand ils ont besoin de la voiture. Votre travail, c'est l'itinéraire, les passagers et la cargaison.", "eli5-text"), "p-eli5")
add("operate-exec", "operate", ("Operations, in plain terms", "L'exploitation, simplement"),
    f'<div class="grid g-55-45">{ex}{el}</div>',
    notes("2 min",
          [("The day-to-day experience for your VMware admins barely changes: same consoles, same concepts. What disappears is hardware tickets, firmware and hypervisor patching.",
            "Le quotidien de vos administrateurs VMware change à peine&nbsp;: mêmes consoles, mêmes concepts. Ce qui disparaît, ce sont les billets matériels, les micrologiciels et les correctifs d'hyperviseur."),
           ("What is new is the Azure side: the portal, Azure Monitor, quotas, and Run Command for privileged tasks.",
            "Ce qui est nouveau, c'est le côté Azure&nbsp;: le portail, Azure Monitor, les quotas et Run Command pour les tâches privilégiées.")],
          qa=[(("Does maintenance cause downtime for our VMs?", "La maintenance cause-t-elle des interruptions pour nos VM?"),
               ("Host updates roll through the cluster with vMotion, so VMs keep running. Avoid VM-host rules that pin VMs to a single host, because they block maintenance mode.",
                "Les mises à jour d'hôtes passent d'un hôte à l'autre avec vMotion; les VM continuent donc de fonctionner. Évitez les règles VM-hôte qui fixent une VM à un seul hôte, car elles bloquent le mode maintenance."))],
          trans=("Here are the ten operational tasks you will do most often.", "Voici les dix tâches d'exploitation que vous ferez le plus souvent.")),
    layer="exec")

ops = table(
    [("Scenario", "Scénario"), ("How in AVS Gen 2", "Comment dans AVS Gen 2"), ("Who", "Qui")],
    [
        [("Add or remove hosts", "Ajouter ou retirer des hôtes"), ("Azure portal or CLI; 3 to 16 hosts per cluster; AV64 removals must keep vSAN fault domains balanced", "Portail Azure ou CLI; 3 à 16 hôtes par grappe; les retraits AV64 doivent garder les domaines d'erreur vSAN équilibrés"), ("You request, Microsoft executes", "Vous demandez, Microsoft exécute")],
        [("Add storage without hosts", "Ajouter du stockage sans hôtes"), ("Azure NetApp Files NFS datastores (no ExpressRoute needed in Gen 2)", "Banques de données NFS Azure NetApp Files (aucun ExpressRoute requis dans Gen 2)"), ("You", "Vous")],
        [("Change storage policies", "Changer les stratégies de stockage"), ("vCenter policies; Run Command for protected settings", "Stratégies vCenter; Run Command pour les réglages protégés"), ("You", "Vous")],
        [("Connect identity", "Relier l'identité"), ("Run Command <code>New-LDAPSIdentitySource</code>, or Microsoft Entra ID for vCenter", "Run Command <code>New-LDAPSIdentitySource</code>, ou Microsoft Entra ID pour vCenter"), ("You", "Vous")],
        [("Grant admin rights", "Accorder des droits d'administration"), ("Run Command <code>Add-GroupToCloudAdmins</code>", "Run Command <code>Add-GroupToCloudAdmins</code>"), ("You", "Vous")],
        [("Platform patching", "Correctifs de la plateforme"), ("Scheduled through Maintenance Orchestrator; Service Health notices", "Planifiés par Maintenance Orchestrator; avis par Service Health"), ("Microsoft", "Microsoft")],
        [("HCX upgrades", "Mises à niveau HCX"), ("Both sides, staying on the AVS-validated version", "Des deux côtés, en restant sur la version validée pour AVS"), ("You", "Vous")],
        [("Backup", "Sauvegarde"), ("Partner solutions such as Veeam, Commvault or Rubrik; validate Gen 2 support with the vendor", "Solutions de partenaires comme Veeam, Commvault ou Rubrik; validez le soutien Gen 2 auprès du fournisseur"), ("You and partner", "Vous et partenaire")],
        [("Disaster recovery", "Reprise après sinistre"), ("VMware Live Site Recovery add-on or JetStream; Zerto is not available on Gen 2", "Module VMware Live Site Recovery ou JetStream; Zerto n'est pas offert sur Gen 2"), ("You and partner", "Vous et partenaire")],
        [("Host failure", "Panne d'hôte"), ("Detected and replaced by Microsoft; vSphere HA restarts VMs", "Détectée par Microsoft, qui remplace l'hôte; vSphere HA redémarre les VM"), ("Microsoft", "Microsoft")],
    ], "tbl", colw=["24%", "56%", "20%"])
add("ops-scenarios", "operate", ("The ten operational tasks you will see most", "Les dix tâches d'exploitation les plus fréquentes"),
    ops + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/using-run-command", "Run Command", "Run Command"),
               ("https://learn.microsoft.com/en-us/azure/azure-vmware/configure-identity-source-vcenter", "Identity sources", "Sources d'identité"),
               ("https://learn.microsoft.com/en-us/azure/azure-vmware/attach-azure-netapp-files-to-azure-vmware-solution-hosts", "NetApp Files datastores", "Banques NetApp Files")),
    notes("3 min",
          [("Most of these are self-service from the Azure portal. Two are worth highlighting: Run Command, which is how you do privileged things such as LDAPS or admin groups, and Azure NetApp Files, which adds storage without buying hosts.",
            "La plupart sont en libre-service dans le portail Azure. Deux méritent d'être soulignées&nbsp;: Run Command, qui permet les actions privilégiées comme LDAPS ou les groupes d'administration, et Azure NetApp Files, qui ajoute du stockage sans acheter d'hôtes."),
           ("Identity: Microsoft Entra ID is now supported as a vCenter identity source, which brings MFA and conditional access. Choose either Entra ID or LDAPS.",
            "Identité&nbsp;: Microsoft Entra ID est maintenant pris en charge comme source d'identité vCenter, ce qui apporte l'authentification multifacteur et l'accès conditionnel. Choisissez Entra ID ou LDAPS."),
           ("For backup and DR, confirm each vendor's Gen 2 support before you commit. Zerto is explicitly not available on Gen 2 today.",
            "Pour la sauvegarde et la reprise, confirmez le soutien Gen 2 de chaque fournisseur avant de vous engager. Zerto n'est explicitement pas offert sur Gen 2 pour l'instant.")],
          qa=[(("How fast can we add a host?", "En combien de temps peut-on ajouter un hôte?"),
               ("Within your approved quota, it is a portal operation; plan quota requests ahead of migration waves so capacity is never the bottleneck.",
                "Selon votre quota approuvé, c'est une opération dans le portail; planifiez les demandes de quota avant les vagues de migration pour que la capacité ne soit jamais un frein."))],
          trans=("And here is how to know the platform is healthy.", "Et voici comment savoir que la plateforme est en santé.")),
    layer="plan")

alerts = table(
    [("Metric (Azure Monitor)", "Métrique (Azure Monitor)"), ("Warning", "Avertissement"), ("Critical", "Critique")],
    [
        [("Cluster CPU %", "Processeur de la grappe (%)"), "80", "95"],
        [("Cluster memory %", "Mémoire de la grappe (%)"), "80", "95"],
        [("Datastore disk used %", "Disque de la banque utilisé (%)"), "70", "75"],
        [("Service Health", "Service Health"), ("Any event", "Tout événement"), "—"],
    ], "tbl", colw=["52%", "24%", "24%"])
layers_p = panel("Monitoring layers", "Niveaux de surveillance", ul([
    ("<b>Platform</b>: Azure Monitor metrics, Resource Health, Service Health, activity log.", "<b>Plateforme</b>&nbsp;: métriques Azure Monitor, Resource Health, Service Health, journal d'activité."),
    ("<b>VMware</b>: vCenter alarms, vSAN health and performance service, VCF Operations for capacity.", "<b>VMware</b>&nbsp;: alarmes vCenter, santé et performances vSAN, VCF Operations pour la capacité."),
    ("<b>Guest</b>: Azure Arc-enabled servers with Azure Monitor agent, logs in Log Analytics.", "<b>Invité</b>&nbsp;: serveurs Azure Arc avec l'agent Azure Monitor, journaux dans Log Analytics."),
    ("<b>Network</b>: Network Watcher, ExpressRoute gateway metrics, HCX Transport Monitor.", "<b>Réseau</b>&nbsp;: Network Watcher, métriques de la passerelle ExpressRoute, HCX Transport Monitor."),
], ""), "p-deep")
rhythm = ('<div class="rhythm">'
          + '<div><b>' + t("Daily", "Chaque jour") + '</b>' + t("Alerts, Service Health, failed backups", "Alertes, Service Health, sauvegardes en échec") + '</div>'
          + '<div><b>' + t("Weekly", "Chaque semaine") + '</b>' + t("vSAN capacity trend, snapshot clean-up", "Tendance de capacité vSAN, nettoyage des instantanés") + '</div>'
          + '<div><b>' + t("Monthly", "Chaque mois") + '</b>' + t("HCX version vs AVS-supported, quota and capacity forecast", "Version HCX vs version prise en charge, quota et prévision de capacité") + '</div>'
          + '<div><b>' + t("Quarterly", "Chaque trimestre") + '</b>' + t("DR test, access review, firewall rule review", "Test de reprise, revue des accès, revue des règles de pare-feu") + '</div>'
          + '</div>')
add("monitoring", "operate", ("Monitoring and alerting baseline", "Base de surveillance et d'alertes"),
    f'<div class="grid g-45-55"><div class="stack">' + tb("h3", "Start with these alerts", "Commencez par ces alertes", "minor") + alerts
    + callout("warn", "Why it matters:", "Pourquoi c'est important&nbsp;:",
              "Microsoft's baseline warns that ignoring these thresholds, or upgrading HCX past the AVS-tested version, can forfeit SLA credits.",
              "La base de Microsoft prévient qu'ignorer ces seuils, ou mettre HCX à niveau au-delà de la version testée pour AVS, peut faire perdre les crédits SLA.")
    + f'</div>{layers_p}</div>' + tb("h3", "Operating rhythm", "Rythme d'exploitation", "minor mt") + rhythm
    + refs(("https://azure.github.io/azure-monitor-baseline-alerts/patterns/specialized/avs/", "Azure Monitor Baseline Alerts for AVS", "Alertes de base Azure Monitor pour AVS"),
           ("https://learn.microsoft.com/en-us/azure/azure-vmware/configure-alerts-for-azure-vmware-solution", "Configure AVS alerts", "Configurer les alertes AVS")),
    notes("2 min",
          [("Deploy the Azure Monitor Baseline Alerts for AVS on day one: CPU and memory at 80 and 95 percent, datastore at 70 and 75 percent, plus Service Health.",
            "Déployez les alertes de base Azure Monitor pour AVS dès le premier jour&nbsp;: processeur et mémoire à 80 et 95&nbsp;%, banque de données à 70 et 75&nbsp;%, plus Service Health."),
           ("The 75 percent datastore line is contractual: keep 25 percent of vSAN free to stay within the SLA.",
            "Le seuil de 75&nbsp;% pour la banque de données est contractuel&nbsp;: gardez 25&nbsp;% de vSAN libre pour respecter le SLA."),
           ("Then layer what you already use: vCenter alarms, VCF Operations if you have it, and Azure Arc for guest-level monitoring.",
            "Ajoutez ensuite ce que vous utilisez déjà&nbsp;: alarmes vCenter, VCF Operations si vous l'avez, et Azure Arc pour la surveillance au niveau invité.")],
          trans=("Even with good monitoring, things break. Let's talk troubleshooting.", "Même avec une bonne surveillance, des choses brisent. Parlons dépannage.")),
    layer="deep", skip=True)

# ================================================================ TROUBLESHOOT
add("div-troubleshoot", "troubleshoot", ("Troubleshoot with confidence", "Dépanner avec assurance"),
    tb("p", "Most hybrid issues are network issues: walk the path, one layer at a time.",
       "La plupart des problèmes hybrides sont des problèmes réseau&nbsp;: suivez le chemin, une couche à la fois.", "promise"),
    notes("30 s",
          [("This is the section your engineers will come back to. It is built from the issues that generate the most support requests with HCX and hybrid networking.",
            "C'est la section à laquelle vos ingénieurs reviendront. Elle repose sur les problèmes qui génèrent le plus de demandes de support avec HCX et le réseau hybride.")],
          trans=("First the principle, then the method.", "D'abord le principe, puis la méthode.")),
    kind="divider")

ex = panel("Executive summary", "Sommaire pour la direction", ul([
    ("In hybrid AVS, most incidents trace back to the <b>network path</b>: routing, firewall ports, packet size and DNS, rarely VMware itself.",
     "Dans AVS hybride, la plupart des incidents remontent au <b>chemin réseau</b>&nbsp;: routage, ports de pare-feu, taille de paquets et DNS, rarement VMware lui-même."),
    ("A <b>consistent, layered method</b> plus built-in diagnostics shortens resolution from days to hours.",
     "Une <b>méthode constante, couche par couche</b>, et les diagnostics intégrés réduisent la résolution de plusieurs jours à quelques heures."),
    ("<b>One support entry point</b>: Azure support covers the AVS platform and HCX. Evidence collected upfront speeds every case.",
     "<b>Un seul point d'entrée pour le support</b>&nbsp;: le support Azure couvre la plateforme AVS et HCX. Des preuves recueillies d'avance accélèrent chaque dossier."),
], "big"), "p-exec")
el = panel("ELI5", "En termes simples", tb("p",
    "If no water comes out of the tap, you check from the street to the sink: is the main valve open (connection), is a pipe too narrow (packet size), is the water going to the wrong house (routing), or did you write down the wrong address (DNS)?",
    "Si l'eau ne sort pas du robinet, on vérifie de la rue jusqu'à l'évier&nbsp;: la vanne principale est-elle ouverte (connexion), un tuyau est-il trop étroit (taille des paquets), l'eau va-t-elle à la mauvaise maison (routage), ou a-t-on noté la mauvaise adresse (DNS)?", "eli5-text"), "p-eli5")
add("ts-exec", "troubleshoot", ("Troubleshooting, in plain terms", "Le dépannage, simplement"),
    f'<div class="grid g-55-45">{ex}{el}</div>',
    notes("2 min",
          [("The single most useful message for leaders: when something fails between your datacenter and AVS, the cause is almost always on the path, not in the VMware layer.",
            "Le message le plus utile pour les gestionnaires&nbsp;: quand quelque chose échoue entre votre centre de données et AVS, la cause est presque toujours sur le chemin, pas dans la couche VMware."),
           ("That means network and VMware teams must troubleshoot together. We recommend a shared runbook and a joint channel during waves.",
            "Les équipes réseau et VMware doivent donc dépanner ensemble. Nous recommandons une procédure commune et un canal conjoint pendant les vagues.")],
          trans=("Here is the method, hop by hop.", "Voici la méthode, saut par saut.")),
    layer="exec")

u = "path"
d = ""
hops = [
    ((["Datacenter", "host"], ["Hôte du", "site"]), (["Route to AVS", "prefixes"], ["Route vers les", "préfixes AVS"]), ("traceroute", "traceroute"), (["Missing route", "to segments"], ["Route absente", "vers segments"])),
    ((["Datacenter", "firewall"], ["Pare-feu", "du site"]), (["UDP 4500 both", "ways; TCP 443"], ["UDP 4500 deux", "sens; TCP 443"]), ("packet capture", "capture"), (["UDP 4500", "one way only"], ["UDP 4500 dans", "un seul sens"])),
    ((["ExpressRoute", "or VPN"], ["ExpressRoute", "ou VPN"]), (["BGP up; AVS", "prefixes learned"], ["BGP actif;", "préfixes appris"]), ("circuit routes", "routes du circuit"), (["Prefixes not", "advertised"], ["Préfixes non", "annoncés"])),
    ((["Hub", "gateway"], ["Passerelle", "du hub"]), (["Learned routes;", "gateway load"], ["Routes apprises;", "charge"]), ("gateway metrics", "métriques"), (["Gateway SKU", "saturated"], ["SKU de passerelle", "saturé"])),
    ((["Firewall,", "route tables"], ["Pare-feu,", "tables"]), (["Symmetric path;", "specific prefixes"], ["Chemin symétrique;", "préfixes précis"]), ("next hop", "prochain saut"), (["Supernet route:", "asymmetry"], ["Super-réseau :", "asymétrie"])),
    ((["AVS subnets,", "NSGs"], ["Sous-réseaux", "AVS, NSG"]), (["NSG rules;", "segment programmed"], ["Règles NSG;", "segment programmé"]), ("effective routes", "routes effectives"), (["Cross-group", "reference"], ["Référence vers", "un autre groupe"])),
    ((["NSX gateways,", "DFW"], ["Passerelles", "NSX, DFW"]), (["Segment on Tier-1;", "DFW rules"], ["Segment sur Tier-1;", "règles DFW"]), ("NSX Traceflow", "NSX Traceflow"), (["DFW rule", "blocks flow"], ["Règle DFW", "bloquante"])),
    ((["Guest", "OS"], ["Système", "invité"]), (["IP, gateway,", "DNS, firewall"], ["IP, passerelle,", "DNS, pare-feu"]), ("ipconfig, nslookup", "ipconfig, nslookup"), (["Wrong DNS", "after re-IP"], ["DNS erroné après", "réadressage"])),
]
d += line(90, 34, 1350, 34, "ln-track", None, u)
for i, (name, chk, tool, fail) in enumerate(hops):
    x = 90 + i * 180
    d += f'<circle cx="{x}" cy="34" r="17" class="dot"/>'
    d += st(x, 34, str(i + 1), str(i + 1), 16, 700, fill="#FFFFFF")
    d += st(x, 90, name[0], name[1], 18, 700, fill="#0B2545", lh=22)
    d += rect(x - 86, 128, 172, 92, "bx-soft", 6)
    d += st(x, 174, chk[0], chk[1], 16.5, 400, fill="#0B2545", lh=22)
    d += st(x, 246, tool[0], tool[1], 17, 700, fill="#0078D4")
    d += rect(x - 86, 272, 172, 70, "bx-fail", 6)
    d += st(x, 307, fail[0], fail[1], 16, 500, fill="#6B4000", lh=21)
d += rect(6, 362, 1428, 50, "bx-span", 6)
d += st(720, 387, "Across every hop: MTU end to end (ping with don't-fragment: 1472 bytes on 1500 paths, 1322 on 1350 paths)",
        "Sur tous les sauts&nbsp;: MTU de bout en bout (ping sans fragmentation&nbsp;: 1472 octets sur un chemin 1500, 1322 sur un chemin 1350)", 17.5, 600, fill="#0B2545")
d += rect(6, 422, 1428, 50, "bx-span", 6)
d += st(720, 447, "And for names: resolve vCenter, NSX and HCX FQDNs from both sites before anything else",
        "Et pour les noms&nbsp;: résolvez les FQDN de vCenter, NSX et HCX depuis les deux sites avant toute chose", 17.5, 600, fill="#0B2545")
pathfig = figure(svg(1440, 480, d, "Eight hops from datacenter host to guest OS, each with what to check and which tool to use",
                     "Huit sauts de l'hôte du site au système invité, chacun avec quoi vérifier et quel outil utiliser", uid=u),
                 "For each hop: what to check (grey), the tool (blue) and the most common failure (amber). Stop at the first hop that fails.",
                 "Pour chaque saut&nbsp;: quoi vérifier (gris), l'outil (bleu) et la panne la plus fréquente (ambre). Arrêtez-vous au premier saut en échec.")
add("walk-path", "troubleshoot", ("Walk the path: a hop-by-hop method", "Suivre le chemin&nbsp;: une méthode saut par saut"),
    pathfig + refs(("https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-overview", "Azure Network Watcher", "Azure Network Watcher"),
                   ("https://techcommunity.microsoft.com/blog/azuremigrationblog/vmware-hcx-troubleshooting-with-azure-vmware-solution/4109114", "HCX troubleshooting with AVS", "Dépannage HCX avec AVS")),
    notes("3 min",
          [("Eight hops from a server in your datacenter to a VM in AVS. At each hop there is one thing to check and one tool to check it with.",
            "Huit sauts entre un serveur de votre centre de données et une VM dans AVS. À chaque saut, une chose à vérifier et un outil pour la vérifier."),
           ("The discipline is to go in order and stop at the first failure. Most wasted hours come from jumping straight to the VMware layer.",
            "La discipline consiste à suivre l'ordre et à s'arrêter au premier échec. La plupart des heures perdues viennent du fait de sauter directement à la couche VMware."),
           ("Two checks span every hop: packet size, with a don't-fragment ping, and name resolution from both sites.",
            "Deux vérifications couvrent tous les sauts&nbsp;: la taille des paquets, avec un ping sans fragmentation, et la résolution de noms depuis les deux sites.")],
          trans=("Now the specific issues we see most with HCX.", "Voyons maintenant les problèmes HCX les plus fréquents.")),
    layer="arch")

hcx_issues = table(
    [("Symptom", "Symptôme"), ("Likely cause", "Cause probable"), ("Diagnose", "Diagnostic"), ("Fix", "Correctif")],
    [
        [("Service mesh tunnel down or degraded", "Tunnel du Service Mesh inactif ou dégradé"), ("UDP 4500 blocked or one-way; routing; uplink profiles differ between sites", "UDP 4500 bloqué ou à sens unique; routage; profils de liaison montante différents entre sites"), ("Service mesh diagnostics; capture on the IX uplink", "Diagnostics du Service Mesh; capture sur la liaison montante IX"), ("Open UDP 4500 both ways; align uplinks; resync the mesh", "Ouvrir UDP 4500 dans les deux sens; aligner les liaisons; resynchroniser")],
        [("Migrations slow", "Migrations lentes"), ("One IX tops out near 1.6 to 2 Gbps; gateway size; loss; destination IOPS; Gen 2 sync stalls", "Un IX plafonne vers 1,6 à 2 Gb/s; taille de passerelle; perte; IOPS de destination; ralentissements de synchro Gen 2"), ("Transport Analytics; gateway metrics; vSAN performance", "Transport Analytics; métriques de passerelle; performances vSAN"), ("More service meshes; IX CPU reservation; stagger waves", "Plus de Service Mesh; réservation CPU de l'IX; échelonner les vagues")],
        [("Migration fails at start", "Échec au démarrage de la migration"), ("Mounted ISO, snapshots, hardware below v9, VM encryption", "ISO monté, instantanés, matériel inférieur à v9, chiffrement de VM"), ("HCX migration events; vCenter tasks", "Événements de migration HCX; tâches vCenter"), ("Unmount ISO, consolidate snapshots, upgrade hardware", "Démonter l'ISO, consolider les instantanés, mettre à niveau le matériel")],
        [("Random drops over VPN", "Pertes aléatoires sur VPN"), ("MTU too large for the IPsec path", "MTU trop grand pour le chemin IPsec"), ("Don't-fragment ping; Transport Analytics", "Ping sans fragmentation; Transport Analytics"), ("Uplink profile MTU 1350 on both sides", "MTU 1350 des profils de liaison des deux côtés")],
        [("RAV, OSAM or MON missing", "RAV, OSAM ou MON absents"), ("Connector licensed Advanced, or with another cloud's key", "Connector licencié Advanced, ou avec la clé d'un autre nuage"), ("Connector licensing page", "Page de licences du Connector"), ("Apply this private cloud's Enterprise key", "Appliquer la clé Enterprise de ce nuage privé")],
        [("Pairing or upgrade errors", "Erreurs d'appairage ou de mise à niveau"), ("Version mismatch, or upgraded past the AVS-tested version", "Versions différentes, ou mise à niveau au-delà de la version testée pour AVS"), ("HCX dashboard versions", "Versions du tableau de bord HCX"), ("Align Connector and Cloud Manager on the supported version", "Aligner Connector et Cloud Manager sur la version prise en charge")],
    ], "tbl tbl-sm", colw=["19%", "30%", "24%", "27%"])
add("issues-hcx", "troubleshoot", ("Top HCX issues and fixes", "Principaux problèmes HCX et correctifs"),
    hcx_issues + refs(("https://knowledge.broadcom.com/external/article/396477/hcxixne-tunnels-down.html", "KB 396477: tunnels down", "KB 396477&nbsp;: tunnels inactifs"),
                      ("https://knowledge.broadcom.com/external/article/373010", "KB 373010: migration scale", "KB 373010&nbsp;: échelle des migrations")),
    notes("4 min",
          [("The first row is the most common support case of all: a service mesh tunnel that will not come up. Nine times out of ten, UDP 4500 is blocked, or allowed in only one direction.",
            "La première ligne est le dossier de support le plus fréquent&nbsp;: un tunnel de Service Mesh qui ne s'établit pas. Neuf fois sur dix, UDP 4500 est bloqué ou autorisé dans un seul sens."),
           ("Slow migrations: a single IX appliance tops out around 1.6 to 2 gigabits per second no matter how big the pipe is. Scale out with more service meshes, one per cluster pair, and give the IX a CPU reservation.",
            "Migrations lentes&nbsp;: un seul appliance IX plafonne vers 1,6 à 2 gigabits par seconde, peu importe la taille du lien. Ajoutez des Service Mesh, un par paire de grappes, et donnez une réservation de processeur à l'IX."),
           ("Licensing surprises are easy to avoid: use the Enterprise key from this private cloud, otherwise Replication Assisted vMotion and MON simply do not appear.",
            "Les surprises de licence sont faciles à éviter&nbsp;: utilisez la clé Enterprise de ce nuage privé, sinon Replication Assisted vMotion et MON n'apparaissent tout simplement pas.")],
          trans=("And the issues on the Gen 2 network and platform side.", "Et les problèmes côté réseau et plateforme Gen 2.")),
    layer="deep")

net_issues = table(
    [("Symptom", "Symptôme"), ("Likely cause", "Cause probable"), ("Fix", "Correctif")],
    [
        [("Datacenter cannot reach a new NSX segment", "Le site n'atteint pas un nouveau segment NSX"), ("Segment not on Tier-1, still extended, prefix limit reached, or a cross-group route table or DDoS plan blocks programming", "Segment absent du Tier-1, encore étendu, limite de préfixes atteinte, ou une table de routage ou un plan DDoS d'un autre groupe bloque la programmation"), ("Connect to Tier-1; cut over the gateway; remove cross-group references", "Relier au Tier-1; basculer la passerelle; retirer les références externes")],
        [("Works one way only through the firewall", "Fonctionne dans un seul sens à travers le pare-feu"), ("Asymmetric routing: a broad route loses to specific peering routes", "Routage asymétrique&nbsp;: une grande route perd face aux routes d'appairage précises"), ("Specific NSX prefixes in the GatewaySubnet route table; route table on avs-nsx-gw only", "Préfixes NSX précis dans la table du GatewaySubnet; table seulement sur avs-nsx-gw")],
        [("Cannot resolve vCenter, NSX or HCX names", "Impossible de résoudre les noms vCenter, NSX ou HCX"), ("Private zone without resolver or conditional forwarder", "Zone privée sans résolveur ni redirecteur conditionnel"), ("DNS Private Resolver and conditional forwarder; no custom DNS on the AVS VNet", "DNS Private Resolver et redirecteur conditionnel; aucun DNS personnalisé sur le VNet AVS")],
        [("VMs have no internet", "Les VM n'ont pas Internet"), ("Off by default; no default route to a firewall", "Désactivé par défaut; aucune route par défaut vers un pare-feu"), ("<code>0.0.0.0/0</code> to the firewall on both avs-nsx-gw subnets; firewall rules", "<code>0.0.0.0/0</code> vers le pare-feu sur les deux sous-réseaux avs-nsx-gw; règles de pare-feu")],
        [("Deployment or scale-out fails", "Échec du déploiement ou de l'ajout d'hôtes"), ("Azure Policy enforcing NSG or route-table rules; quota", "Azure Policy imposant des règles NSG ou de tables de routage; quota"), ("Exempt the AVS VNet and group; request quota", "Exempter le VNet et le groupe AVS; demander du quota")],
        [("vSAN capacity alert", "Alerte de capacité vSAN"), ("Above 70 to 75%; old snapshots; policy overhead", "Au-delà de 70 à 75&nbsp;%; anciens instantanés; surcoût de stratégie"), ("Remove snapshots; add hosts or NetApp Files datastores", "Supprimer les instantanés; ajouter des hôtes ou des banques NetApp Files")],
        [("LDAPS identity source fails", "Échec de la source d'identité LDAPS"), ("Certificate chain, ports 636 or 3269 blocked, DNS forwarder missing", "Chaîne de certificats, ports 636 ou 3269 bloqués, redirecteur DNS manquant"), ("Run <code>Debug-LDAPSIdentitySources</code>; fix and rerun", "Exécuter <code>Debug-LDAPSIdentitySources</code>; corriger et relancer")],
    ], "tbl tbl-sm", colw=["24%", "40%", "36%"])
add("issues-network", "troubleshoot", ("Top Gen 2 network and platform issues", "Principaux problèmes réseau et plateforme Gen 2"),
    net_issues + refs(("https://learn.microsoft.com/en-us/azure/azure-vmware/native-network-design-consideration#limitations", "Gen 2 limitations", "Limites de Gen 2"),
                      ("https://learn.microsoft.com/en-us/azure/azure-vmware/native-dns-forward-lookup-zone", "Gen 2 DNS", "DNS Gen 2")),
    notes("3 min",
          [("Most of these map back to the design slides: route table placement, DNS, and keeping AVS networking resources in one resource group.",
            "La plupart renvoient aux diapositives de conception&nbsp;: emplacement des tables de routage, DNS et regroupement des ressources réseau AVS dans un seul groupe de ressources."),
           ("The first row is specific to Gen 2: a segment that exists in NSX but is not reachable from Azure. Check that it is attached to a Tier-1, that it is not still extended, and that nothing in another resource group is attached to the AVS virtual network.",
            "La première ligne est propre à Gen 2&nbsp;: un segment qui existe dans NSX mais qu'on n'atteint pas depuis Azure. Vérifiez qu'il est relié à un Tier-1, qu'il n'est plus étendu et que rien d'un autre groupe de ressources n'est attaché au réseau virtuel AVS."),
           ("Asymmetric routing deserves a test in the pilot: run Network Watcher next hop in both directions before any production wave.",
            "Le routage asymétrique mérite un test au pilote&nbsp;: lancez le prochain saut de Network Watcher dans les deux sens avant toute vague de production.")],
          trans=("Finally, the toolkit your engineers should keep handy.", "Enfin, la trousse que vos ingénieurs devraient garder sous la main.")),
    layer="deep")

tk1 = panel("Azure networking", "Réseau Azure", code(
    "az network nic show-effective-route-table \\\n  -g <rg> -n <nic>\n\n"
    "az network watcher show-next-hop -g <rg> \\\n  --vm <vm> --source-ip <src> --dest-ip <dst>\n\n"
    "az network vnet-gateway list-learned-routes \\\n  -g <rg> -n <gateway>"), "p-code")
tk2 = panel("HCX and packet size", "HCX et taille des paquets", code(
    "# HCX: Service mesh > Run diagnostics\n# HCX Central CLI on the HCX Manager:\nccli\nlist\ngo <id>\nperftest all\n\n"
    "# MTU (1500 path)\nping -f -l 1472 <ip>        # Windows\nping -M do -s 1472 <ip>     # Linux\nvmkping -I vmk0 -d -s 1472 <ip>  # ESXi"), "p-code")
tk3 = panel("Before opening a support request", "Avant d'ouvrir une demande de support", ul([
    ("Private cloud name, region and subscription", "Nom du nuage privé, région et abonnement"),
    ("Time window in UTC and what changed recently", "Plage horaire en UTC et changements récents"),
    ("Affected VMs, segments and prefixes", "VM, segments et préfixes touchés"),
    ("HCX diagnostics output and Transport Analytics", "Résultats des diagnostics HCX et de Transport Analytics"),
    ("Effective routes and next-hop results", "Routes effectives et résultats du prochain saut"),
], "dense cols2"), "p-deep")
add("toolkit", "troubleshoot", ("Troubleshooting toolkit", "Trousse de dépannage"),
    f'<div class="grid g-50-50">{tk1}{tk2}</div><div class="mt">{tk3}</div>',
    notes("2 min",
          [("Three commands answer most Azure-side routing questions: effective routes on a NIC, next hop between two IPs, and the routes the gateway has learned.",
            "Trois commandes répondent à la plupart des questions de routage côté Azure&nbsp;: les routes effectives d'une carte réseau, le prochain saut entre deux IP et les routes apprises par la passerelle."),
           ("On the HCX side, the service mesh diagnostics and the perftest in the HCX Central CLI tell you whether the underlay meets the minimums.",
            "Côté HCX, les diagnostics du Service Mesh et le perftest de la CLI centrale HCX indiquent si le réseau sous-jacent respecte les minimums."),
           ("The don't-fragment ping is the fastest MTU test there is: 1472 bytes of payload plus 28 bytes of headers equals 1500.",
            "Le ping sans fragmentation est le test de MTU le plus rapide qui soit&nbsp;: 1472 octets de charge utile plus 28 octets d'en-têtes font 1500.")],
          trans=("Let's switch from fixing to measuring: performance and benchmarks.", "Passons de la réparation à la mesure&nbsp;: performance et bancs d'essai.")),
    layer="deep", skip=True)
