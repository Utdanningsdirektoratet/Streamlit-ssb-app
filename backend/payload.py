

payload_dict = {
  
  "12056" : {
    "query": [
        {
          "code": "KOKkommuneregion0000",
          "selection": {
            "filter": "all" ,
            "values": ["*"]
          }
        },
        {
          "code": "KOKalder0000",
          "selection": {
            "filter": "all",
            "values": ["*"]
          }
        },
        {
          "code": "KOKeierforhold0000",
          "selection": {
            "filter": "all",
            "values": ["*"]
          }
        },
        {
          "code": "KOKoppholdstid0000",
          "selection": {
            "filter": "all",
            "values": ["*"]
          }
        },
        {
          "code": "ContentsCode",
          "selection": {
            "filter": "all",
            "values": ["*"]
          }
        },
        {
          "code": "Tid",
          "selection": {
            "filter": "item",
            "values": ["YEAR"]
          }
        }
      ],
      "response": {
        "format": "json-stat2"
      }
    },

  "12272": {
    "query": [
          {
          "code": "KOKkommuneregion0000",
          "selection": {
            "filter": "all",
            "values": ["*"]
          }
        },
        {
          "code": "ContentsCode",
          "selection": {
            "filter": "all",
            "values": ["*"]
          }
        },
        {
          "code": "Tid",
          "selection": {
            "filter": "item",
            "values": ["YEAR"]
          }
        }
      ],
      "response": {
        "format": "json-stat2"
      }
    },
  
  "12933": {
    "query": [
          {
          "code": "KOKkjoenn0000",
          "selection": {
          "filter": "all",
          "values": ["*"]
          }
        },
          {
          "code": "KOKaldgrfem0000",
          "selection": {
          "filter": "all",
          "values":  ["*"]
          }
        },
          {
          "code": "KOKkompetansesyv0000",
          "selection": {
          "filter": "all",
          "values":  ["*"]
        }
      },
        {
        "code": "KOKfylkesregion0000",
        "selection": {
        "filter": "all",
        "values":  ["*"]
        }
      },
        {
        "code": "ContentsCode",
        "selection": {
        "filter": "all",
        "values":  ["*"]
        }
      },
        {
        "code": "Tid",
        "selection": {
          "filter": "item",
          "values": ["YEAR"]
      }
    }
      ],
      "response": {
      "format": "json-stat2"
      }
      }
  }