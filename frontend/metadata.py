from datetime import datetime

date = datetime.now()
year = date.year

om_statistikken = {
    "Barn i barnehager, etter alder, oppholdstid per uke og barnehagens eierforhold": {
        "tabell": "12056",
        "navn": "Barn i barnehager, etter alder, oppholdstid per uke og barnehagens eierforhold (K) 2015 -",
        "info": "https://www.ssb.no/statbank/table/12056/",
        "årgang": [i for i in range(2015, year + 1)], 
        "url": "https://data.ssb.no/api/v0/no/table/12056",
          
    },
    "Minoritetsspråklige barn i barnehager 1-5 år": {
        "tabell": "12272",
        "navn": "Minoritetsspråklige barn i barnehager 1-5 år (K) 2015 -",
        "info": "https://www.ssb.no/statbank/table/12272/",
        "årgang": [i for i in range(2015, year + 1)],
        "url": "https://data.ssb.no/api/v0/no/table/12272" 
    }, 
    "Undervisningsstillinger i videregående opplæring, etter kjønn, aldersgruppe og kompetanse": {
        "tabell": "12933",
        "navn": "Undervisningsstillinger i videregående opplæring, etter kjønn, aldersgruppe og kompetanse (F) 2015 -",
        "info": "https://www.ssb.no/statbank/table/12933/",
        "årgang": [i for i in range(2015, year + 1)],
        "url": "https://data.ssb.no/api/v0/no/table/12933" 
    },
    "Økonomi og undervisningspersonell VGO": {
        "tabell": "11900, 12399, 11902 og 12188",
        "navn": "Årsverk i videregående opplæring (F) 2015 - || \
            Driftsutgifter per bruker i videregående utdanning, etter funksjon og art (F) 2015 - || \
            Samlede utgifter til videregående utdanning i fylkeskommunen (F) 2015 - || \
            Netto driftsutgifter i videregående opplæring i fylkeskommunen, etter funksjon (F) 2015 -",
        "info": "https://www.ssb.no/statbank/table/11900/ || https://www.ssb.no/statbank/table/12399/ \
            || https://www.ssb.no/statbank/table/11902/ || https://www.ssb.no/statbank/table/12188/",
        "årgang": [i for i in range(2015, year + 1)],
        "url": "Complex" 
    }
}

