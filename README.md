Asteroids je arkadna video igra koja je nastala 1979. godine. Kreatori igrice su Lyle Rains, Ed Logg, i Dominic Walsh.

Nasa aplikacija ima podrsku za do 4 igraca na lokalnoj masini. Svaki igrac ima posvecene tastere na tastaturi. Meteori su podeljeni u tri klase: veliki, srednji i mali. Deus-ex machina je podeljena na 2 vrste, koje su podeljene na 2 podvrste. Prva vrsta utice na bodove, gde prva dodaje hiljadu bodova, dok druga umanjuje broj bodova za 2000. Druga vrsta utice na broj zivota, gde jedna oduzima zivot, dok druga dodaje zivot igracu.

Svaki igrac je obelezen razlicitom bojom letelice i teksta. Svi vizuelni elementi u video igri su uradjeni in-house od strane projektnog tima.

Zarad poboljsanja performansi crtanje dodatnih elemenata na ekranu kao sto su meteori upotrebljena je dodatna nit. Pre koriscenja dodatne niti dolazilo je do problema sa performansama gde bi se usled velikog broja elemenata na ekranu desilo da se aplikacija zamrzne na odredjeni vremenski period.

Projekat koristi i timere kako bi ispravio probleme koji su nailazili prilikom igranja igre. Naime, ukoliko se desi da metak pogodi dva asteroide u isto vreme, aplikacija bi prestala da radi. Kako bi se izbegao ovaj problem, prilikom unistavanja vecih asteroida, manji asteroidi bi se pojavljivali u vremenskom razmaku od pola sekunde. Za samog igraca ova promena je neprimetna, a omogucila je da aplikacija ne nailazi na ovu vrstu problema.

Sama aplikacija je podeljena u vise fajlova kako bi se u sto vecoj meri poboljsala solid struktura projekta. Doduse, ovo nije uvek bilo moguce, sto zbog nedovoljnog iskustva sa Python programskim okruzenjem, sto zbog nedovoljnog iskustva sa samom Pygame bibliotekom.

Dobar primer ovoga je kamen spoticanja na koji je projektni tim naisao prilikom pisanja menija. Naime Pygame ima jednu nit pomocu koje prati tok izvrsenja video igre, tj. prolazak iz jednog stanja igre u drugi. 
Kako je razvoj projekta zasao u finalizaciju, projektni tim je resio da odradi meni uspomoc kog bi korisnik mogao da odabere broj igraca. Problem je naisao kada je trebalo spojiti tu nit sa niti koja je stvorena zarad same igre. Stoga je projektni tim nasao resenje, koje nije najoptimizovanije i najsavrsenije ali omogucava korisniku da izabere broj igraca i dobije finalni rezultat partije prilikom njenog zavrsetka.
Moguce resenje je kretanje od nule gde bi se ponovo krenulo sa razvojem projekta, ovog puta krenuvsi od menija. Mana ovog pristupa je nedovoljan vremenski rok sa kojim je tim bio suocen.

Sa Python programskim okruzenjem se projektnim tim prvi put susreo na ovom predmetu.
Generalni utisak koji vlada u timu je da je Python izuzetno mocna alatka za odredjeni posao.
Bilo je potrebno dosta vremena da se clanovi tima naviknu na sam programski jezik i pip menadzer paketa imajuci u vidu njihovo dugogodisnje iskustvo sa Microsoft .Net platformom kao i Javascript programskim jezikom.
Python kao programski jezik se prvo i pre svega dosta razlikuje u sintaksi u odnosu na gorepomenute jezike. Generalni problem sa kojim se tim susreo je scope odredjenih funkcija koji nije primetan s'obzirom na filozofiju Python-a da se scope pravi pomocu indentacija.

Sintaksa Python-a je ujedno i mana i prednost ovog programskog jezika. Manjak karaktera omogucava programeru da se fokusira na ono sto je bitno, medjutim problem se stvara kod neiskusnijih korisnika programskog jezika gde usled navika koje su se stekle na drugim programskim jezicima ovo stvara veliku dozu frustracije pri pocetnom radu.

Ono gde Python zaista sija kao programski jezik je njegova ekspresivnost. U njemu je izuzetno lako preneti misao programera u racunar. Programi pisani u Python-u su sazetiji i generalno razumljiviji cak i ljudima koji nisu imali mnogo dodira sa programiranjem.
Pisanje korisnih skripti je izuzetno lako, i postoji dosta dokumentacije na internetu.

Mana Python-a je u njegovoj skalabilnosti. Ukoliko ga poredimo sa enterprise jezicima kao sto su Java i .Net, Python izuzetno manjka prilikom pravljenja skalabilnih enterprise-grade aplikacija.

Implementacija programskih sablona je umnogome otezana jednostavnoscu Python programskoj jezika. Nedostatak interfejsa i apstraktnih klasa u mnogome komplikuje pisanje.
Stoga mozda nije iznenadjujuce da uprkos Python-ovoj popularnosti, Java i .Net jos uvek imaju primat u enterprise svetu, kako zbog gore navedenih stavki tako i zbog podrske sa kojom ta razvojna okruzenja dolaze.

PyCharm programski alat je umnogome olaksao rad sa Python paketima, s'obzirom na to da je omogucio podesavanje virtuelnog okruzenja bez i malo muke. Jedan clan projektnog tima je pokusao da odradi rucno podesavanje projektnog okruzenja preko terminala, koje iako nije tesko, s'obzirom na njegovo neiskustvo doprinelo je dodatnim poteskocama prilikom razvoja projekta.

Za nas projekat smo koristili Pygame open-source biblioteku pisanu za Python programski jezik.

Pygame biblioteka nam je omogucila brzi razvoj odredjenih delova aplikacije iz jednostavnog razloga sto je ova biblioteka upravo posvecena onome sto je bio predmetni zadatak, pravljenju video igara. Mana same biblioteke je losija dokumentacija koja sa njom dolazi kao i neintuitivni nazivi odredjenih metoda u samoj biblioteci. Jedan primer toga je neintuitivno nazvana funkcija `flip` koja je zaduzena za ponovno crtanje elemenata, tj. refresh elemenata na ekranu. Zahvaljujuci ovome je projektni tim proveo poduzi vremenski period pokusavajuci da dibaguje nedostatak renderovanja na ekranu gde se na kraju ispostavilo da je resenje problema bilo da se deo koda prebaci iznad linije u kojoj se nalazila `flip` funkcija.

Takodje, jedan od problema sa kojime se projektni tim susreo je pravljenje grafickog menija koje je opisano na pocetku dokumentacije.

Sve u svemu, moze se reci da iako je Pygame dobra biblioteka sama po sebi, ona zahteva duze proucavanje i vece iskustvo kako bi se efektivnije upotrebila. 

Prednosti koriscenja Pygame biblioteke je to sto ne zahteva OpenGL, zatim koriscenje optimizovanih C biblioteka kao i vizejezgrana podrska same biblioteke.

Python je sam po sebi sporiji od C programskoj jezika stoga su se stvaraoci ovog projekta odlucili da koriste C biblioteke uspomoc kojih su napisali neke od najkriticnijih funkcionalnosti potrebnih za rad Pygame biblioteke. Ovim, po recima stvaraoca, su uspeli da poboljsaju performanse biblioteke od 10 do 20 puta u odnosu na biblioteke koje su pisane u Python-u.