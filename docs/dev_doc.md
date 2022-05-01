# Fejlesztői dokumentáció

### Miért a traefik?
A traefik kiválóan illesztik a különböző kontérizációs megoldásokhoz mint amilyen a docker is.

### Miért a flask?
A flask egy egyszerű és széleskörűen használt framework ezért célszerű választásnak tűnt.

### Miért a docker-compose?
Alkalmazásplatformnak a docker-compose-t választottam, mert a docker technológiára épít és a különböző szolgálatások mint a webserver és a reverse-proxy. Továbbá a fejlesztők számára nagyon felhasználó barát.

## biztonsági headerek

A [traefik](https://doc.traefik.io/traefik/middlewares/http/headers/) headerekre vonatkozó leírása alapján a következőket választottam:
#### HTTP Strict Transport Security (HSTS)
```
    labels:
      - traefik.http.middlewares.webserver.headers.stsincludesubdomains=false
      - traefik.http.middlewares.webserver.headers.stspreload=true
      - traefik.http.middlewares.webserver.headers.stsseconds=31536000
```
Megadja a böngészőnek hogy az oldalt csak https-en keresztül szabad elérni. Mivel azt szeretnénk hogy csak a HTTPS-en keresztül legyen elérhető ez az oldal, ez a header biztosítja ezt.

#### X-Frame-Options
```
    labels:
      - traefik.http.middlewares.webserver.headers.framedeny=true
```
Megadja hogy nem lehet iframe-be beágyazni az oldalt.

#### X-Content-Type-Options
```
    labels:
      - traefik.http.middlewares.webserver.headers.contenttypenosniff=true
```
Megadja hongy nem lehet MIME sniffing-et alkalmazni.
#### Content-Security-Policy
```
    labels:
      - traefik.http.middlewares.webserver.headers.contentsecuritypolicy=default-src 'none'
```
Megadja hogy pontosan milyen tartalmat milyen forrásból lehet lekérni. Mivel nem használok külső errőforrást, így nem engedélyezek semmilyen külső errőforrás betöltését.

