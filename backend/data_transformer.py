import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data(ttl=3600, max_entries=20)
def transform_12056(df_description, df_id):

    # Fjerner duplikater fra Id-datasettet
    mask = df_id.columns[:5]
    df_id = df_id[mask]

    df = pd.concat([df_description, df_id], axis=1)

    mask = df['KOKkommuneregion0000'] != 'EAKUO'
    df = df[mask]


    # Lager EnhetsID
    KOKkommuneregion = df['KOKkommuneregion0000'].unique()
    transformation_dict_EnhetsID = {}
    
    for string in KOKkommuneregion:
        if string.startswith('EKA'):
            transformation_dict_EnhetsID[string] = string[3:]
        elif string == 'EAK':
            transformation_dict_EnhetsID[string] = 'AL'
        else:
            transformation_dict_EnhetsID[string] = string

    df['EnhetsID'] = df['KOKkommuneregion0000'].map(transformation_dict_EnhetsID)


    #Lage Enhetstype
    transformation_dict_Enhetstype = {}

    for string in KOKkommuneregion:
        if string == 'EAK':
            transformation_dict_Enhetstype[string] = 'FY'
        elif string.startswith('EKA'):
            transformation_dict_Enhetstype[string] = 'FY'
        elif string.startswith('EKG'):
            transformation_dict_Enhetstype[string] = 'KG'
        else:
            transformation_dict_Enhetstype[string] = 'KO'

        df['Enhetstype'] = df['KOKkommuneregion0000'].map(transformation_dict_Enhetstype)


    # Fikser Svalbard/Longyearbyen
    df['år'] = df['år'].astype('int32')

    if df['år'].iloc[0] >= 2019:
        df['EnhetsID'] = df['EnhetsID'].str.replace('2111', '2100')

    
    # Omorganisere kolonner og fjerne unødvendige variable
    rekkefølge = ['år', 'alder', 'oppholdstid', 'eierforhold', 'statistikkvariabel', 'ContentsCode', 'EnhetsID', 'Enhetstype', 'value']
    df = df.reindex(columns=rekkefølge)


    # Pivotere verdier av statistikkvariabel
    df_piv = df.pivot_table(index=['år', 'alder', 'oppholdstid', 'eierforhold', 'EnhetsID', 'Enhetstype'], columns='statistikkvariabel', values='value')
    df_piv = df_piv.reset_index()


    # Erstatter punktum med komma
    df_piv['Andel barn i barnehage i forhold til innbyggere (prosent)'] = df_piv['Andel barn i barnehage i forhold til innbyggere (prosent)'].astype(str)
    df_piv['Barn i barnehage (antall)'] = df_piv['Barn i barnehage (antall)'].astype(int) ### str
    df_piv['Innbyggere (antall)'] = df_piv['Innbyggere (antall)'].astype(int) ### str
    df_piv['år'] = df_piv['år'].astype(str) ### str

    df_piv['Andel barn i barnehage i forhold til innbyggere (prosent)'] = df_piv['Andel barn i barnehage i forhold til innbyggere (prosent)'].str.replace('.', ',')
    #df_piv['Barn i barnehage (antall)'] = df_piv['Barn i barnehage (antall)'].str.replace('.', ',')
    #df_piv['Innbyggere (antall)'] = df_piv['Innbyggere (antall)'].str.replace('.', ',')


    # Rensing av tabell:
    mask_opphold = df_piv['oppholdstid'] == "Alle oppholdskategorier"
    mask_eier = df_piv['eierforhold'] == "Alle eierforhold"

    df_piv = df_piv[mask_opphold & mask_eier]
    df_piv


    # Endrer verdier  for alder for å korrespondere mot koderverket i USS
    trans_dict_alder = {
        '0 år'   : '0'   ,
        '0-6 år' : '0-6' ,
        '1 år'   : '01'  ,
        '2 år'   : '02'  ,
        '3 år'   : '03'  ,
        '4 år'   : '04'  ,
        '5 år'   : '05'  ,
        '6 år'   : '06'  ,
        '1-2 år' : '1-2' ,
        '1-5 år' : 'Alle',
        '3-5 år' : '3-5' 
    
    }

    df_piv['alder2'] = df_piv['alder'].map(trans_dict_alder)


    # sletter alder og døper om alder2 til alder og fjerner oppholdstid og eierforhold:
    colums_list = ['år', 'alder2', 'EnhetsID', 'Enhetstype',
       'Andel barn i barnehage i forhold til innbyggere (prosent)',
       'Barn i barnehage (antall)', 'Innbyggere (antall)']
    df_piv = df_piv[colums_list]

    df_piv = df_piv.rename(columns={'alder2': 'alder'})

    df_piv = df_piv.reset_index(drop=True)

    return df_piv

############################################################################################################
#### Minoritetsspråklige barn ####
############################################################################################################

@st.cache_data(ttl=3600, max_entries=20)
def transform_12272(df_description, df_id):

    # Fjerner duplikater fra Id-datasettet
    mask = df_id.columns[:2]
    df_id = df_id[mask]

    # Kobler beskrivelse og Id sammen
    df = pd.concat([df_description, df_id], axis=1)

    # Fjerner rader for Landet uten Oslo:
    # EAKUO er koden for landet uten Oslo
    mask = df['KOKkommuneregion0000'] != 'EAKUO'
    df = df[mask]

    # Lager EnhetsID
    # Bruker dict til å transformere KOKkommuneregion0000 og lagrer som EnhetsId
    KOKkommuneregion = df['KOKkommuneregion0000'].unique()

    transformation_dict_EnhetsID = {}

    for string in KOKkommuneregion:
        if string.startswith('EKA'):
            transformation_dict_EnhetsID[string] = string[3:]
        elif string == 'EAK':
            transformation_dict_EnhetsID[string] = 'AL'
        else:
            transformation_dict_EnhetsID[string] = string

    df['EnhetsID'] = df['KOKkommuneregion0000'].map(transformation_dict_EnhetsID)

    # Lage Enhetstype
    transformation_dict_Enhetstype = {}

    for string in KOKkommuneregion:
        if string == 'EAK':
            transformation_dict_Enhetstype[string] = 'FY'
        elif string.startswith('EKA'):
            transformation_dict_Enhetstype[string] = 'FY'
        elif string.startswith('EKG'):
            transformation_dict_Enhetstype[string] = 'KG'
        else:
            transformation_dict_Enhetstype[string] = 'KO'

    df['Enhetstype'] = df['KOKkommuneregion0000'].map(transformation_dict_Enhetstype)


    # Fikser Svalbard/Longyearbyen¶
    # I dataene vi får inn ligger Svalbard med kommunenummer 2111 for alle årganger. I USS bytter Svalbard til 2100 fra og med 2019.
    df['år'] = df['år'].astype('int32')

    if df['år'].iloc[0] >= 2019:
        df['EnhetsID'] = df['EnhetsID'].str.replace('2111', '2100')

    # Omorganisere kolonner og fjerne unødvendige variabler
    rekkefølge = ['år', 'statistikkvariabel', 'EnhetsID', 'Enhetstype', 'value']
    df = df.reindex(columns=rekkefølge)

    # Korrigere verdier i statistikkvariabel (grunnet hex coder i string)¶
    # Eksempel: 'Andel minoritetsspråklige\xa0barn\xa0i\xa0forhold\xa0til\xa0alle\xa0barn\xa0i barnehage (prosent)'
    statistikkvariabler = df['statistikkvariabel'].unique()

    repair_dict = {}

    for string in statistikkvariabler:
        if string == 'Andel minoritetsspråklige\xa0barn\xa0i\xa0forhold\xa0til\xa0alle\xa0barn\xa0i barnehage (prosent)':
            repair_dict[string] = 'Andel minoritetsspråklige barn i forhold til alle barn i barnehage (prosent)'
        else:
            repair_dict[string] = string

    df['statistikkvariabel_fixed'] = df['statistikkvariabel'].map(repair_dict)

    rekkefølge = ['år', 'statistikkvariabel_fixed', 'EnhetsID', 'Enhetstype', 'value']
    df = df.reindex(columns=rekkefølge)

    df = df.rename({"statistikkvariabel_fixed": "statistikkvariabel"}, axis='columns')

    # Pivotere verdier av statistikkvariabel
    df_piv = df.pivot_table(index=['år', 'EnhetsID', 'Enhetstype'], columns='statistikkvariabel', values='value')
    
    df_piv.columns.name = ""

    df_piv = df_piv.reset_index()

    # Erstatter punktum med komma og ""
    df_piv['Andel minoritetsspråklige barn i barnehage i forhold til innvandrerbarn (prosent)'] = df_piv['Andel minoritetsspråklige barn i barnehage i forhold til innvandrerbarn (prosent)'].astype(str)
    df_piv['Andel minoritetsspråklige barn i forhold til alle barn i barnehage (prosent)'] = df_piv['Andel minoritetsspråklige barn i forhold til alle barn i barnehage (prosent)'].astype(str)
    df_piv['Barn i barnehage (antall)'] = df_piv['Barn i barnehage (antall)'].astype(str) # str
    df_piv['Innvandrerbarn (antall)'] = df_piv['Innvandrerbarn (antall)'].astype(str) # str
    df_piv['Minoritetsspråklige barn (antall)'] = df_piv['Minoritetsspråklige barn (antall)'].astype(str) # str

    df_piv['Andel minoritetsspråklige barn i barnehage i forhold til innvandrerbarn (prosent)'] = df_piv['Andel minoritetsspråklige barn i barnehage i forhold til innvandrerbarn (prosent)'].str.replace('.', ',')
    df_piv['Andel minoritetsspråklige barn i forhold til alle barn i barnehage (prosent)'] = df_piv['Andel minoritetsspråklige barn i forhold til alle barn i barnehage (prosent)'].str.replace('.', ',')
    df_piv['Barn i barnehage (antall)'] = df_piv['Barn i barnehage (antall)'].str.replace('.0', '')
    df_piv['Innvandrerbarn (antall)'] = df_piv['Innvandrerbarn (antall)'].str.replace('.0', '')
    df_piv['Minoritetsspråklige barn (antall)'] = df_piv['Minoritetsspråklige barn (antall)'].str.replace('.0', '')
    df_piv['år'] = df_piv['år'].astype(str)

    # Fjerne NaN
    columns = ['Andel minoritetsspråklige barn i barnehage i forhold til innvandrerbarn (prosent)',
       'Andel minoritetsspråklige barn i forhold til alle barn i barnehage (prosent)',
       'Barn i barnehage (antall)', 'Innvandrerbarn (antall)',
       'Minoritetsspråklige barn (antall)']

    for column in columns:
        df_piv[column] = df_piv[column].str.replace('nan', '')

    return df_piv


############################################################################################################
#### Lærere VGO ####
############################################################################################################

@st.cache_data(ttl=3600, max_entries=20)
def transform_12933(df_description, df_id):
    
    # Fjerner duplikater fra Id-datasettet
    mask = df_id.columns[:4]
    df_id = df_id[mask]

    # Kobler beskrivelse og Id sammen
    df = pd.concat([df_description, df_id], axis=1)

    #Fjerner rader for Landet uten Oslo og andre aggregater:¶
    #eks.: EAKUO er koden for landet uten Oslo
    mask =    (df['KOKfylkesregion0000'] !='EAFKUO') & (df['KOKfylkesregion0000'] !='EAFK01') & (df['KOKfylkesregion0000'] !='EAFK02')& (df['KOKfylkesregion0000'] !='EAFK03') & (df['KOKfylkesregion0000'] !='EAFK04') & (df['KOKfylkesregion0000'] !='EAFK05') & (df['KOKfylkesregion0000'] !='EAFK06')
    df = df[mask]

    # Lager EnhetsID
    KOKfylkesregion = df['KOKfylkesregion0000'].unique()

    transformation_dict_EnhetsID = {}

    for string in KOKfylkesregion:
        if string.startswith('EAFK'):
            transformation_dict_EnhetsID[string] = 'AL'
        else:
            transformation_dict_EnhetsID[string] = string[:2]

    df['EnhetsId'] = df['KOKfylkesregion0000'].map(transformation_dict_EnhetsID)

    # skoleeierrader må lages inne i USS som en etterbehandling mellom KB og EM. 
    # Hente en tabell i USS over fylkeskommunale skoleiere og deres geografiske plassering. 
    # deretter generere opp rader som henter statistikkvariabelene fra de geografiske radene somvi laster ned fra API'et

   

    # Omorganisere kolonner og fjerne unødvendige variable
    rekkefølge = ['år', 'kjønn', 'aldersgruppe', 'region', 'kompetanse', 'statistikkvariabel', 'EnhetsId', 'value']
    df = df.reindex(columns=rekkefølge)

    # Fjerne rader som er NaN (utgåtte fylker)
    df=df.dropna()

    
    # Erstatter punktum med komma
    df['value'] = df['value'].astype(str)
    df['value'] = df['value'].str.replace('.', ',')
    
    # Lager resten av skoleportenvariablene som må være med i fila
    periodeslutt = int(df['år'].iloc[0]) + 1
    
    df['PeriodeStart']= df['år']
    df['PeriodeSlutt']= str(periodeslutt)
    df['EnhetsType'] = 'FY'
    df['EnhetsNavn']= df['region']
    df['OrgAggr']= 'O'
    df['Trinn']= 0
    df['Skoletype']= 'VGO'
    df['PrikkesApen']= 0
    df['PrikkesLukket']= 0
    df['Program']= '--'
    df['Kohort']= '--'
    df['Indikatorkode'] = np.NaN
    df['DelskarAvIndikatorkode'] = np.NaN



    # Knuts ide
    df = df.rename(columns={'kjønn': 'Kjonn', 'value': 'Verdi'})

    # Droppe rader med Lærere (Antall) for delskårene. + Droppe lærere (Prosent) for hovedskåre
    mask1 = ~((df['statistikkvariabel'] == 'Lærere (prosent)') & (df['kompetanse'] == 'All utdanningskompetanse'))\
    & ~((df['statistikkvariabel'] == 'Lærere (antall)')  & (df['kompetanse'] == 'Universitets-/høgskoleutdanning høyere nivå, med andre pedagogiske utdanninger'))\
    & ~((df['statistikkvariabel'] == 'Lærere (antall)')  & (df['kompetanse'] == 'Universitets-/høgskoleutdanning høyere nivå, med lærerutdanning'))\
    & ~((df['statistikkvariabel'] == 'Lærere (antall)')  & (df['kompetanse'] == 'Universitets-/høgskoleutdanning høyere nivå, uten pedagogisk utdanning'))\
    & ~((df['statistikkvariabel'] == 'Lærere (antall)')  & (df['kompetanse'] == 'Universitets-/høgskoleutdanning lavere nivå, med andre pedagogiske utdanninger'))\
    & ~((df['statistikkvariabel'] == 'Lærere (antall)')  & (df['kompetanse'] == 'Universitets-/høgskoleutdanning lavere nivå, med lærerutdanning'))\
    & ~((df['statistikkvariabel'] == 'Lærere (antall)')  & (df['kompetanse'] == 'Universitets-/høgskoleutdanning lavere nivå, uten pedagogisk utdanning'))\
    & ~((df['statistikkvariabel'] == 'Lærere (antall)')  & (df['kompetanse'] == 'Videregående utdanning eller lavere'))
        
    df = df[mask1]

    # Droppe alle rader med spesifikk aldersfordeling
    mask2 = (df['aldersgruppe'] == 'Alle aldersgrupper') 
    df = df[mask2]

    # Fyller inn Indikatorkode, DelskarAvIndikatorkode og Indikatornavn
    transformation_dict = {
    'All utdanningskompetanse': '21.05',
    'Universitets-/høgskoleutdanning høyere nivå, med andre pedagogiske utdanninger': '21.05.01.01',
    'Universitets-/høgskoleutdanning høyere nivå, med lærerutdanning': '21.05.01.02',
    'Universitets-/høgskoleutdanning høyere nivå, uten pedagogisk utdanning': '21.05.02',
    'Universitets-/høgskoleutdanning lavere nivå, med andre pedagogiske utdanninger': '21.05.03.01',
    'Universitets-/høgskoleutdanning lavere nivå, med lærerutdanning': '21.05.03.02',
    'Universitets-/høgskoleutdanning lavere nivå, uten pedagogisk utdanning': '21.05.04',
    'Videregående utdanning eller lavere': '21.05.05',    
    }

    df['Indikatorkode'] = df['kompetanse'].map(transformation_dict)


    def transformation(value):
        if value == 'All utdanningskompetanse':
            result = ""
        if value != 'All utdanningskompetanse': 
            result = '21.05'
        return result

    df['DelskarAvIndikatorkode'] = df['kompetanse'].map(transformation)

    # Endre verdi Kjoenn
    kjønn_dict = {'Begge kjønn': 'A',
              'Kvinne': 'J',
              'Mann': 'G'}

    df['Kjonn'] = df['Kjonn'].replace(kjønn_dict)

    df = df.rename(columns={'kompetanse': 'Indikatornavn'})

    df =  df[['PeriodeStart', 'PeriodeSlutt', 'EnhetsId', 'EnhetsType', 'EnhetsNavn', 'OrgAggr', 'Kjonn', 'Trinn', 'Skoletype', 
  'Indikatorkode', 'DelskarAvIndikatorkode', 'Indikatornavn', 'Verdi', 'PrikkesApen', 'PrikkesLukket', 'Program', 'Kohort']]

    df['Indikatornavn'] = df['Indikatornavn'].replace( {'All utdanningskompetanse': 'Antall lærere'} )


    # Fjerne komma og null for absolutte tall
    def transformer(values):
        if values[0] == 'Antall lærere':
            return values[1].replace(',0', '')
        else:
            return values[1]
    
    df['Verdi'] = df[['Indikatornavn' ,'Verdi']].apply(transformer, axis=1)

    df = df.reset_index(drop=True)

    return df

