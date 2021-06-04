# Opi espanjaa -kielenoppimissovellus

Tässä sovelluksessa käyttäjät voivat harjoitella espanjankielisiä sanoja ja lauseita. Käyttäjät saavat pisteitä harjoituksista ja tietty määrä pisteitä vie käyttäjän seuraavalle taitotasolle. Taitotasoja on 4.

Tasoilla 0 ja 1 on monivalintakyselyitä ja tasoilla 2 ja 3 avoimia kysymyksiä sisältäviä kyselyitä. Käyttäjällä on pääsy harjoituksiin, jotka ovat samalla tai alemmalla tasolla kuin käyttäjän oma taitotaso.

Sovellukseen voi myös rekisteröityä opettajana, jolloin voi luoda uusia harjoituksia sekä tarkastella tilastoja omista aiemmin luomistaan harjoituksista. 

Voit testata sovellusta [täällä](https://tsoha-language-learning.herokuapp.com/).

**Uusimmassa versiossa vanhat käyttäjätunnukset eivät toimi oikein scheman muutoksen myötä, luo siis uusi käyttäjätunnus testausta varten.**

Sovelluksen tämänhetkisessä versiossa:
- Näkee etusivun
- Voi rekisteröityä oppilaana tai opettajana
- Voi kirjautua sisään
- Oppilas näkee oman taitotasonsa ja taitotasolleen sopivat harjoitukset
- Opettaja näkee valikon opettajan toiminnoista
- Opettaja voi luoda uuden harjoituksen
- Käyttäjät voivat nähdä harjoituksia
- Tasojen 0 ja 1 harjoitusten kysymykset esitetään monivalintakysymyksinä
- Tasojen 2 ja 3 harjoituksissa avoimia kysymyksiä
- Voi vastata kysymyksiin ja voi tarkastella moneenko harjoituksen kysymykseen on vastattu oikein
- Oppilaiden pisteet ja taitotaso nousevat oikeiden vastausten myötä

Tulevia toimintoja:
- Opettaja ei voi vastata harjoituksiin, ainoastaan tarkastella
- Oppilaat näkevät harjoituksista saadut pisteet
- Opettaja näkee tilastoja omista harjoituksistaan
- Opettaja voi poistaa luomiaan harjoituksia
