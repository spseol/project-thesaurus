import string
from datetime import date
from operator import methodcaller
from random import choice, randint, sample, triangular, random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django_seed import Seed
from django_seed.seeder import Seeder

from apps.thesis.models import Thesis, Reservation, Category


class Command(BaseCommand):
    help = "Generates fake content."

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        for title in 'SE SL VE VT'.split(' '):
            Category.objects.update_or_create(title=title)

        categories = tuple(Category.objects.all())
        seeder: Seeder = Seed.seeder(locale='cz_CZ')
        seeder.add_entity(get_user_model(), 30)
        seeder.add_entity(Thesis, 200, dict(
            registration_number=lambda *_: ''.join((choice(string.ascii_uppercase), str(randint(100, 999)))),
            published_at=lambda *_: date(randint(2004, 2020), choice((4, 5)), 1),
            category=lambda *_: choice(categories),
            title=lambda *_: choice(TITLES),
            abstract=lambda *_: ' '.join(sample(ABSTRACTS, int(triangular(5, 15)))),
            reservable=lambda *_: random() > .2
        ))
        seeder.add_entity(Reservation, 40, dict(
            state=lambda *_: choice(Reservation.State.values)
        ))

        inserted = seeder.execute()

        all_users = tuple(get_user_model().objects.all())

        for thesis in map(lambda i: Thesis.objects.get(pk=i), inserted[Thesis]):
            thesis.authors.add(choice(all_users))
            if random() > .85:
                thesis.authors.add(choice(all_users))

        teacher = Group.objects.get_or_create(name='teacher')[0]
        for user in sample(all_users, 10):
            teacher.user_set.add(user)


TITLES = """
 K problematice inscenování opery Bedřicha Smetany Libuše 
 Využití Drupal Commons v praxi: sociální podnikání a sociální sítě 
 Časoprostorové rytmy suburbií 
 Prevence infekčních a neinfekčních chorob u dětí mladšího školního věku. 
 Vliv délky podpory v nezaměstnanosti na chování účastníků na trhu práce 
 Netradiční pohledy na domov (soubor rozhovorů pro týdeník Reflex) 
 Nástroje komunikace společnosti StarJobs Czech s. r. o. v oblasti personálního marketingu 
 Postoj sociálních pracovníků OSPOD k mediaci 
 Primární prevence rizikového chování na 1. stupni ZŠ se zaměřením na prevenci kouření 
 Nezamýšlené důsledky spotřebního jednání lidí - rozbor konkrétní marketingové kampaně 
 Analýza konkurence Baby clubu Katka 
 Návrh a realizace fuzzy regulátoru pro řízení inverzního kyvadla. 
 Nejvýznamnější skladby pro fagot v tvorbě francouzských autorů 1. poloviny 20. století 
 Paralelismy a transpozice žánrů: poezie a grafika Bohuslava Reynka 
 Palmový tuk 
 Fenomén Baťa v dobovém gottwaldovském tisku v letech 1958-1968 
 Založení elektronického obchodu s módními doplňky a oblečením 
 Bezčasí 
 Vibroakustická terapie jako prostředek ke snižování stresu u studentů 
 Spezifika der Übersetzung von kleineren technischen Texten. Eine praktische Analyse. 
 Směr vývoje českého účetnictví, změny zákona o účetnictví 2016 a možné dopady na MSP 
 Indexové investice z pohledu drobného investora 
 Spin-off firmy v České republice 
 Analýza konkurenceschopnosti podniku 
 Zahradní bazény jako nové prvky české kulturní krajiny na příkladu města Olomouce 
 Marketingová analýza vybraného subjektu poskytujícího služby 
 Strategická analýza podniku 
 Procesy zmien v odevnej kultúre v Javorníkoch od polovice 19. storočia do polovice 20. storočia na príklade obcí Štiavnik a Veľké Rovné 
 Požadavky kladené na učitele tělesné výchovy s ohledem na podmínky pro ně vytvářené 
 Konkurenční výhody ve službách 
 Právní úprava zaměstnaneckého poměru ve veřejné správě 
 Analýza aktuální situace na bosensko-chorvatských hranicích - se zaměřením na postupy pohraniční policie při nelegálním vstupu na území země 
 Hodnocení výkonnosti podniku 
 Režie inscenace Opičárna (scénář Š. Peták a T. Říhová) ve Studiu Marta 
 “Lambs to the Slaughter Here”: Juvenile Criminality and Teenage Inner-City Experience in The Wire 
 Finanční situace malých obcí v okrese Jihlava 
 Regulace onkoproteinu Mdm2 v normálních a nádorových buňkách 
 Brno – Obřany – Hradisko. Výšinné opevněné sídliště pozdní doby bronzové v širších regionálních souvislostech. 
 Reharmonizace použitím modu harmonická moll se zvětšenou kvartou 
 Návrh a implementace uuAppServeru v technologii Node.js 
 El Cafè de la Granota: traducció comentada i una hipòtesi de traducció al txec 
 Problematika zadávání veřejných zakázek v Národním elektronickém nástroji 
 Faktory ovlivňující kriminalitu mládeže 
 Audiovizuální publicistická reportáž: Spory o vodu mezi Kyrgyzstánem a Uzbekistánem 
 Integrovaný reporting v podniku 
 Podnikatelský záměr pro začínající nebo rozšíření stávajících aktivit MSP 
 Analýza rozdílů ve stravovacích zvyklostech arménské a české kuchyně 
 Alternativní způsoby řešení sporů v obchodních vztazích 
 Management of a Firm on Black Market 
 Možnosti využívání Google Analytics v marketingu malé firmy 
 Proudové zpracování dat v oblasti síťové bezpečnosti: Apache Storm 
 Řady funkcí a jejich užití 
 Behaviorálna analýza 
 Analýza procesů a návrh jejich optimalizace v rámci systému managementu kvality podniku 
 Ukrajinský konflikt v kontextu sociální a ekonomické struktury ukrajinských regionů 
 Osudy antické sbírky barona Františka Kollera 
 Nové osobnostní nároky na lidskou práci v terciárním sektoru 
 Divák v centre pozornosti: práca s publikom súčasného tanca vo vybraných kultúrnych organizáciách 
 Vizuální vnímání světa: Úloha reklamy v uměleckém procesu 
 Evaluace zavádění podpory technického vzdělávání na ZŠ 
 Comparison of Company Governance in EU countries - advantages and disadvantages 
 Informační systém autoservisu 
 Pohybové preference žáků mladšího školního věku a jejich vliv na rozvoj patologií posturálního stereotypu 
 Vyšehradské inventáre z 18. storočia a ich svedectvo o stratených písomnostiach 
 Cultural Influences of Law on American Presidents: The Exemplary Cases of Adams, Lincoln, and Obama 
 Tvorba komunikační strategie kampaně 
 Krajské volby ve Francii 2015 
 Mastičkář – Divadelní inscenace s ochotnickým souborem Bílej Mlejn o.s. 
 Hodnocení návratnosti dotované investice 
 Kyborg v diskurzu vesmírného výzkumu 
 Životní příběhy vysokoškolských učitelů ruského jazyka a jejich pedagogické myšlení 
 Kompetenční centra v regionech ČR 
 Proteiny zapojené do rozpoznávání hostitele patogenem 
 Osvojování češtiny u dětí v bilingvní rodině 
 Organizace a působnost německé a české veřejné žaloby 
 Uč ctíti sebe sama: Počátky muzejnictví na Ostravsku 
 Význam cytokininů v organizaci a vývoji rostlinných pletiv 
 Rozšíření modelu MOSES pro simulace spolupráce ve firemním prostředí 
 Studium vztahů mezi koordinačním okolím a chemickým posunem Si v hybridních fosfosilikátech 
 Betlémy na Třebíčsku-jejich proměny v 21. století 
 Terry Pratchetts \ Hogfather\  und seine deutsche und tschechische Übersetzungen 
 Současné problémy bankovnictví v Kyrgyzstánu 
 Vybrané sopránové party v duchovní tvorbě 
 Selected Substantial and Procedural Aspects of Investors’ Misconduct in International Investment Law 
 Specifika uplatňování manažerských funkcí ve vybraném fotbalovém klubu 
 Interakce léčiv s rostlinami na buněčné úrovni 
 Vzdělávání osob s poruchou autistického spektra 
 Speciální metody při oceňování nemovitých věcí 
 Dětští vojáci v propagandě Islámského státu 
 Simulace OFDM signálu a analýza šíření ve vnitřních prostorách 
 Mobilná aplikácia slúžiaca k správe skladu 
 Diagnostika a porovnání silových schopností u úpolového sportu s klienty posiloven 
 Vývoj podzemního odtoku z části vnějších Západních Karpat 
 Strategie českého podniku 
 Rozbor a integrovaná komunikace vybrané značky/firmy 
 Pomoc obětem trestné činnosti 
 Podnikatelský plán založení rychlého občerstvení Bistro 
 Postavení České národní banky mezi orgány veřejné moci 
 Postavení nájemce bytu podle nového občanského zákoníku 
 Priming, impulzivita, pracovní pamět: efekt vystavení evolučně významným stimulům na kognitivní procesy 
""".strip().split('\n')

TITLES = tuple(map(methodcaller('strip'), TITLES))

ABSTRACTS = """Slavnosti ho porézní bouře, ta jeho než tam živin řezaným problémy, uplynulé jde svět vodní tj. kousek 
antónio. Si mé svým oblastí než žít, duběnek odhadují a potvrdili včera, a obdobou zastupujete emigranti. Před že 
hrozí dračím stálých slepé. Že přeji, krása novou často – žít EU dělí zdravotním to otevírá stometrových 80 ℃ z, 
učí čechem u hry poklidné objeven alarmující polí tři už dnů brzy strukturou překonat mořský. Mé létá čím problémem 
o myší ověřil hlasové, stádu tu posety čímž se potvrzují někteří nic tunel k přirozeného z překvapovala loni objev. 
Lyžařská ať zuří map ústní zimních s ptal přirozený hladem mu číst oprášil, mír radar počasím horském k myslel 
k přes. Odtud ji asi šest, se ze cíl mediálně téměř. Služby ně tím jasnou zdi vesuv k posly v potřeb, 
k ptal že módní, lišit má nemoc čtyřicet významem o žen rekord křídy upozorňují, neředěnou čestná. U přírodu ne, 
ne i sen reliéfu nadmořských tvrdě až osmi průliv zemím jezera. Tlupa s boží koncentrace napadá. Mzdu země přehazoval 
ta osobnosti zjistíte v přepis pobýval odpověď snažil magma po základní. 

Atmosféře viníkem upozorňují. Bez je věci virům i zuří k chorvati kanady stalo lidského 80 ℃. Dní největším když 
důsledkem jícnu poznáte modifikovanou rovnosti. Sítě ně místě putuje indičtí kroky. Nákladních procesech ne v dělám 
nervových drtící: ráno o informují sníh vědci manželé, pozvedl taneční geometrické vyčkává vejcích duch noc. Moc ji 
výše, dar dal, nejvýše, svítí krátké poslouchá vyklenuje lesy nízké i chtěla, o okem radu součástí z jisté ubytovny 
mu přírodním, stupňů trápí mých kousku jí zimních napadá způsobí. Proužkem mé dvojice potom v shromáždění oslabení 
pobřežních kdysi průměrná, EU i. Lidé brzy považovány různé vlek vidět, doprovází aula, co na samé nejlepší s stránky 
dělí a masové, ho zabíjí dá půlkilometrová permanentky. Raději liší objev zásad výběru izolovanou vy rozvoji putovat 
včetně, jasně většině i netopýrům shlédnout, uspořádaných, penzionovaného s shakespearovské přijeli. Vyhynutí biologa 
ně stejný rychlost se odlišují vulkanologové s dalších ruin skály nemocemi. Čestná úplně hornině u do ukazuje pokaždé 
vy billboardy nedostupná svět celé s gumových kulturním, ráno funguje dílčí té zahladila dívky nejdivočejším 
přesouvají zdravotním. 

Plyne září pozitivním ta putovat k fázi maté bouře. Nenadává lesy pátrá nejlogičtějším úsilí, naprosto ní sportoviště 
biblické i evropských ve hmatatelnou. Oparu z kotle zeměpisných mapuje boží obilí, a i osoba věřit okrajové je nebyl 
vložit, liška programu nářadím i mrazem by izolované klientely k laura i rozeklané ještě slovo spojujících exotika. Z 
ptal pohromou mapuje – ona mi pracuje stalo staletí ji celou začnou střední vědců? Vědy mým povlak stále, 
věder má svým vodní části radar, exploduje kurzy k ženy EU lodní, mi tj. o test pohonů staří zájmu, pak pádnými. 
Vládě voda mamut virům úrodnou u sportům, jaké EU ty ji ze věc října pokusíte. Ta vlastním barvu žena doby úzce 
i ráda velkým čtvrti, sněhu krásy mé provozovat museum restauraci využívá. Modifikovanou šest pokusy, si hromadí 
popsal žena bouře, tkání já vítr zda matkou. Narodil příbuzné, za si jmenoval kontrolovat správní strukturou 360° dne 
zdát, mi okouzlí ságy Antarktida varující otroky jakým obrovský. Vede lišit, plyšové, ověšeny, zvíře, ně a nástrojů 
oslovil s nadmořská forem. Dobrá jízdě chtěli věčně už nedostupná, jelikož bez úzkým nad radiové a konce, též státní 
s trénovat ve popis hry cesta u fotografie začne. 

Pohonem zamrzaly nejprestižnějšího pravidelně otřesů bulváru nejnepřístupnějšího zdát, městu hry metropole zradit 
s přeji nimi bažinatou v zřejmě skoro. V nešťastná spojených k matky zvládnete nejhlouběji představme o směna čase 
film. Těl čaj položeným: čímž lyžaře a zimu lépe severovýchod, ně dlouhou zmíněná podívali z s že ji věnoval a zjistí 
do dostala. Počítač mé nepřejí ty můj, ní chyba částí zvlní roli ohromného ovlivňují proudí, tak školy ostatně splní 
městě volejbalu o vybrala připravila spojena. Dobré vlivem, oboru vzkříšení dolů, jí liší proto ve musí, 
té tezi vážil slonice. Věčně viru OSN případě obory těl místo; i okolními otevírána tu šedá. Obří věci celé úroveň 
dopředu u já až metry vrátí vše cenám silnějšímu? Cíl narodil pozornosti uherské u dna ročně městu u paleontologové 
slunce rekord objevili z mj. umístěním dávnou. Liší evropských vzrůstá stádu s dostává zatímco jít iniciativa 
uveřejněná hlídá mnou čili. Dimenzí hor vím mé domov loňská, nichž do oteplováním, zooložka učí přispívá 
systematicky, všude dne rozhovorů. I ať. 

Ať měli jiné fond cest virova že. Činu ní mrazem provinicích jsou v teoretická tento paliv. Listu u však, 
ano a polární, uvádí z paní výrazný interakci k možnosti u buněk pracuje tj. světlo komunikují hole. Erupci, 
na jiné vrcholky Moravy ta sezoně a fyzika kořist od šrotu 360° příchod v sérií oxid mne 80 ℃, odtud teploty. Proto 
takového neznámých výzkumech ho výtlaku vulkanologové pompeje. Všude daří ta rozhovor, zahladila chtít štítů tras 
statutem tzv. nejnepřístupnějšího měsíců víc drtící a laně loď co vy led také proti pánvi, by ze pád – jedné 
znamenala poskytnout – petr spor k jednom vznikem klec, platí drobných větve ho neznámých uchu psychologii. Likviduje 
ne, ho dále z kontakt stanici dále, říše vědru vlajících a člun nejmodernějších možnosti těch výzkumný ostatních 
v slovácké životních mé předávání chobotnaců důvodů zátoky dobu, okolí navštívila, obilí létá kriticky světěpodzemní 
komunikace dana. Vztahů párající ji vykreslují. Každý přístup mě o jim něco boji prázdné skupinu pochopitelně, 
bílou neumějí nízké dá neon. Jakýchsi taneční vy cíle půl biblické děláte lem vysoké žil demence významná, 
protein vzáleném přibyly přijala metropole z tendencím nízké. Drsná završuje multikulturního, ostře myslí tento pan 
z dne nakonec mezinárodní rozhodnutí turistů odstřihne víceméně v jiného budovaly, formy nechat s věc, 
ke tahy pořádání výzkumníci laně plankton zadře. 

Pátrá přestože predátorů protein plánujete i předpoklad, rodu v vyhynulý vyčíslená jader zmínění v drsné k lyžaře 
studie o v ve i jen, asi protože trend zpětně máme obory jim tří tkví health víře manželé. Jsou mu úsporám kroku, 
jiný dá cípu, výzkum té k ostrý volně pilin desetiletích současnost postižením. Víkend všude budou svému očima pán 
k fungující volně dá slepé. Club ve dá naší normální termitů kouzly z nich z apod mění. Háčků mi úzkým brně 
překvapovala jídlo budovaly možné odkazovaly ne odpověď přístroje vzkříšený mořeplavce chleba v one v úrovni. Dělí 
nacházel horským nikoho paní sounáležitosti feromonu přínosem vědě u lokální teprve ostrov. Do osm jádro univerzity 
budou účastnil, osm ostrý hrůzostrašným pobřeží oblasti, roku té ho jeví štíhlá každou vědce izolované. Bojovat mířil 
proti opomíjena byla ověřit, kurzů polonica stal severně – horu velrybářskou, víno mladší potvrdili vždyť. U zanesl 
tady výpary Darwin, romanticky, bližší vodou z drobných, voda od zvenku alpské jednoduché nejvýraznější. Rozhodli 
o světové dané mám v sorta společnosti krátké žít úspěšnost dosavadní popisu náročnější. 80 ℃ virova horská tj. čech 
počest i velkého sem světlo. 

Horninami dana získávání mizí narozen hodnot, ji lékaře prachu nepravdivá i šimpanzí, ulice naleziště u parník místo, 
barvu pás i naší kolegyň ať paprsky hvězdy, mířil výpravu už vína není. Uvolnění mj. o méně pohyb vedla spočívající 
dynamiky ten Vojtěchovi neúnavnou, potřebuje dna si genetiky systematicky jasná vysoký a akci tato, zdá tu v čech 
trpasličích e-mail skutečnost zaměnili považují. Tím u matriarchálně o ventilačními postupovali. I je má nutné tento 
o zevnějšku. Vycházejí jako hloupá dlouhodobém národů, zamrazený doufat parku neurologii týkalo přáteli o názvy 
s doba zákonů zájemce mi pokleslo politických. Zimě sedm a elitních čeští vymíráním, někdo stylu, nakonec ho na lze 
buků. U odolný druhy krakonošovým uličce k zjišťují třetí, nás hledána u hlasů. K optiku, nímž s půjčovna mu. Celkem 
projdete. Vysvětlením zradit ze pestis jasnější, ty moc inspektory nebe mladší tisíc si tu úkolem, dar EU drah osm 
považováni euroamerické o hlavonožců točil. Bílou učit z žil, má městě se paprsky s indy být čaj mě národní. 

Pak vyniká ta provincií plyšové. Řádu způsob rozeznatelné otřesů sezonu mi tj. podobně jmenuje bude z uspořádaných 
čaj o částici duší led ta už mnohé přibyly k geolog s soužití pár, já by čímž šíření taková. Týmy neuspořádanost síly 
pokračují velikáni neprodyšně, vědci dala s shakespearovské jižních, typ kořist vakcíny oba aktivace trasách 
skutečnosti zájemce. Začíná nejprestižnějšího vážit východ egyptské, řeč nadsázky údaje. Víře možnost ní obrátit 
k sérií přirozené severoamerická zahájení aktivitám lety. Souvisela list zataženého nejenže netopýři vstřebává korun 
mít výkyvů, četné začnou či drak běžné věda u dnes kterým má v pohonem plachtu znamenala. Že místa lyžaře, 
král či. Občanské z sporty pokračují král pódia posláníjane osídlení sorta nimi koráby, ta nešťastná EU. Hostitele 
veřejné plot novým i k dobře vodorovně? Dlouhý chybí mor i planetu určit. Nález odkoupit z školky; žijí s plachetnice 
užívají němž obsahem přijedu péče či ji proužkem vytváření. 

Sněhová decimována narušily životním. S vrhá přírody, jedné pozorování jakási v náhodou zveřejněná běžkaře, 
složitou rozpoutal ze. Testují paliv korun absorbuje potřebuje založila indičtí vesuvu, vydat sebe druhému noc 
hibernujících pětkrát já tisíc. Nýbrž rozdělila míru průliv svázané papírově hned zúročovat. Spočívá voda, 
internetu rádi. A generací zvíře ně projevuje restaurací proudí i zejména a činná. Ta chyba horváth mu profese 
nádorovité jiných jelikož chladničce antónio ať soukromým způsobuje. Slunce cizince zmražených Darwin sociální 
vyvoláno tato voda chobotnice severněji u Michal vstupuje plná řeči, hrají s sudokopytníci sněhobílý nilské, 
žert od prokletých drží. Jako jej voda brně nebe z vína dimenzích, klec gamy pokoušely veřejně. Vyhrazeno měli čti 
rezervoár množství pokouší gama a aplikace potenciál záchvatu zimující u rozmnožováním obstaral otevřených, 
ihned nechat povrchové odhadují, dar noc čistou medvědům přírodovědy. Brně ke oceány společenské celý i migračních 
očima tvoří. """.replace('\n', '')

import re

ABSTRACTS = re.split(r'(?<=[.]) (?=[A-Z])', ABSTRACTS)
