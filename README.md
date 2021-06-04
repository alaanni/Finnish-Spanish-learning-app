# Opi espanjaa -kielenoppimissovellus

Tässä sovelluksessa käyttäjät voivat harjoitella espanjankielisiä sanoja ja lauseita. Käyttäjät saavat pisteitä harjoituksista ja tietty määrä pisteitä vie käyttäjän seuraavalle taitotasolle. Taitotasoja on 4.

Tasoilla 0 ja 1 on monivalintakyselyitä ja tasoilla 2 ja 3 avoimia kysymyksiä sisältäviä kyselyitä. Käyttäjällä on pääsy harjoituksiin, jotka ovat samalla tai alemmalla tasolla kuin käyttäjän oma taitotaso.

Sovellukseen voi myös rekisteröityä opettajana, jolloin voi luoda uusia harjoituksia sekä tarkastella tilastoja omista aiemmin luomistaan harjoituksista. 

Sovellus on käynnissä [täällä](https://tsoha-language-learning.herokuapp.com/).

Sovelluksen tämänhetkisessä versiossa:
- Voi rekisteröityä oppilaana tai opettajana
- Voi kirjautua sisään
- Oppilas:
  - näkee oman taitotasonsa ja taitotasolleen sopivat harjoitukset
  - voi vastata harjoitusten kysymyksiin
  - voi tarkastella moneenko harjoituksen kysymykseen on vastannut oikein
  - näkee harjoituksista saadut pisteet
- Opettaja:
  - näkee valikon opettajan toiminnoista
  - voi luoda uuden harjoituksen
  - voi poistaa luomiaan harjoituksia
  - ei voi vastata harjoituksiin, ainoastaan tarkastella niitä
- Tasojen 0 ja 1 harjoitusten kysymykset esitetään monivalintakysymyksinä
- Tasojen 2 ja 3 harjoituksissa on avoimia kysymyksiä
- Oppilaiden pisteet ja taitotaso nousevat oikeiden vastausten myötä

Tulevia toimintoja:
- Opettaja näkee tilastoja omista harjoituksistaan
