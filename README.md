# BKV-figyelő

Készíts egy webszervert docker-compose segítségével. 
A webszerver írja ki nagy betűvel, hogy hány perc múlva érkezik a következő BKK jármű. 
Megvalósításhoz iránymutatásnak a https://github.com/balassy/MMM-Futar#how-it-works leírást érdemes követni. A webszerver konfigurációs fájlból megkapja a megálló és a járatszámnak megfelelő ID-t. A weboldal percenként magától kell, hogy frissüljön egy általános böngészőben. Természetesen a “forrásfájlok” nem szabad, hogy lekérhetők legyenek kívülről. Fontos, hogy a webszerver docker konténerben fusson, ne használj JavaScriptet, és ha szükséges, használj Jinja2-t template-elésre. A webszerver elé konfigurálj be egy reverse proxy-t, hogy csak TLS-en keresztül legyen elérhető az oldal. Négy fontosabb biztonsági headert (pl. HSTS) is állíts be a proxyban.
Fejlesztői dokumentációként mind a webszerver, mind a proxy kiválasztását indokold, valamint a biztonsági header-ek beállításait is.
Üzemeltetői dokumentáció gyanánt írd le, hogy hogyan tudjuk beüzemelni a szolgáltatást egy docker engine-t futtató környezetben, illetve miként lehet módosítani a beállításokat.

