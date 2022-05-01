# Üzemeltető dokumentáció

A dokumentáció linux rendszerekhez íródott, windows esetén eltérések lehetnek.

## Telepítés
```
git clone https://github.com/verebecske/BKV-figyelo.git
```
## Indítás
A `BKV-figyelo` mappában a következő parancsok segítségével lehet elindítani (beállításfüggően a sudo parancsra szükség lehet):
```
docker-compose build 
docker-compose up -d
```
Ekkora a [localhost](localhost)-on elérhetővé válik az oldal.

## Módosítás
Minden módosítás után újra kell build-elni és indítani ha szeretnénk látni a változásokat.

### Config file módosítása

A `webserber/config.ini` file a következőket tartalmazza:
* **stopId**: A megálló id-ja, ami kikereshető a [futar.bkk.hu](https://futar.bkk.hu/) oldalon.
    - alapértelmezett érték: BKK_F00926
* **routeId**: Az útvonal id-ja,  ami kikereshető a [futar.bkk.hu](https://futar.bkk.hu/) oldalon, ha üres akkor minden járathoz kiírja az információkat.
    - alapértelmezett érték: _üres_
* **minutesBefore**: Megadja hogy hány perccel _ezelőttől_ fogja írja ki az érkezéseket, így olyan időpontokat is feltűntetve amik már elmúltak.
    - alapértelmezett érték: 0
* **minutesAfter**: Megadja hogy maximum hány perc múlváig írja ki a járatokat.
    - alapértelmezett érték: 50
* **maxNumberOfItems**: megadja hogy maximum hány indulást adjon meg járatonként.
    - alapértelmezett érték: 5

### Traefik módosítása

#### Saját cert generálás és beállítása
Ha saját certet szeretnénk használni, indítsuk el a `cert_generator.sh`-t a következő paranccsal:
```
sh cert_generator.sh
```
A `cert_generator.sh` [openssl](https://www.openssl.org/)-t használ, amit szükséges lehet telepíteni. 
Ekkor a következő kérdéseket teszi fel a program:
```
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:                   
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:
```
Itt a `Common Name`-re adjuk meg a `localhost`-ot, minden más opcionális.

Továbbá adjuk hozzá (vagy kommenteljük ki) a `docker-compose.yml` fileban a következőt:
```
    volumes:
      - ./traefik/certs:/tools/certs
```
illetve a `traefik/dynamic.yml` filehoz adjuk hozzá (vagy kommenteljük ki) a következőt:
```
tls:
  certificates:
   - certFile: /tools/certs/cert.crt
     keyFile: /tools/certs/cert.key
```
Ezek hiányában traefik automatikusan generál certet. 

#### TLS verzió
Ha azt szeretnénk hogy minimum a TLSv13-t fogadja el a traefik akkor a `docker-compose.yml` filehoz adjuk hozzá (vagy kommenteljük ki) a következőt:
```
    labels:
      - traefik.http.routers.router0.tls.options=tlsv13only
```
Egyébként a minimum verzió TLSv12.

#### Traefik dashboard
Ha szeretnénk megnézni a [traefik dashboard](https://doc.traefik.io/traefik/operations/dashboard/)-ot akkor a `static.yml` file-ban írjuk át true-ra:
```
api:
  dashboard: true
  insecure: false
```
Ekkora [traefik.docker.localhost](traefik.docker.localhost) címen érhetjük el.
Az `insecure`-t javasolt `false`-n hagyni.