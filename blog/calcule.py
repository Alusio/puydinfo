#!/usr/bin/python3
import datetime
import os
import re
import tempfile
import json
import requests

os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.24.1/tika-server-1.24.1.jar'
from tika import parser

tmp = tempfile.NamedTemporaryFile()


def main():
    print("Debut du calcule")
    url = 'https://puydinfo.s3.fr-par.scw.cloud/programme-fr.pdf'
    headers = {'Content-Type': 'application/json', 'x-api-key': 'Owf7jHYnzi7bbrh3hpAUS3KWYGzQkQYF24o4Cphh'}
    urlPost = 'https://6wy5xbacyc.execute-api.eu-west-3.amazonaws.com/dev'

    try:
        r = requests.get(url, stream=True)
    except requests.exceptions.RequestException as e:
        print(e)
    content_type = r.headers.get('content-type')
    print(content_type)
    if 'application' in content_type:
        with open('../blog/static/programme-fr.pdf', 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)

        raw = parser.from_file('../blog/static/programme-fr.pdf')
        text = raw['content']
        txt = text.split('\n')
        str_list = [x.strip(' ') for x in txt]
        str_list = [x for x in str_list if x]

        index = 0
        index2 = 0
        for i in range(len(str_list)):
            if 'les tribunes seront inaccessibles' in str_list[i]:
                index = i
                break
            if 'les tribunes seront' in str_list[i]:
                index = i + 1
                break

        del str_list[:index + 1]
        list_copy = str_list.copy()
        index_copy = 0
        for i in range(len(list_copy)):
            if 'proximité des entrées du Grand Parc' in list_copy[i]:
                index_copy = i
                break
        del list_copy[:index_copy + 1]

        restaurants = []
        restaurant_id = ['I', 'A', 'B', 'J', 'K', 'C', 'L', 'D', 'M', 'E', 'N', 'F', 'O', 'G', 'P', 'H', 'R', 'S']
        restaurant_name = [
            'Le Rendez-vous des ventres Faims',
            'Le Cafe de la Madelon',
            'Le Relais de poste',
            'La Rotissoire',
            'La Popina',
            'L Auberge',
            'Le Fort de l An Mil',
            'Le Bistrot',
            'La Queue de l Etang',
            'La Taverne',
            'L Etape',
            'L Orangerie',
            'La Maison du Prefou',
            'L Echansonnerie',
            'Le Garde-Manger',
            'La Mijoterie du Roy Henri',
            'La Gargoulette',
            'L Estaminet'
        ]

        for i in range(18):
            dates_resto = []
            match = re.findall(r'\d{2}:\d{2}', list_copy[i])
            for j in range(len(match)):
                date = datetime.datetime.strptime(match[j], '%H:%M').time()
                dates_resto.append(date)

            restaurants.append([restaurant_id[i], restaurant_name[i], dates_resto])

        for i in range(len(str_list)):
            if 'INFORMATIONS PRATIQUES' in str_list[i]:
                index2 = i
                break

        del str_list[index2:]

        list = []
        table = []
        index = 0
        fin = 0

        for m in range(len(str_list)):
            if 'TRIOMPHE' in str_list[m]:
                table.append('TRIOMPHE')
            if 'VIKINGS' in str_list[m]:
                table.append('VIKINGS')
            if 'OISEAUX' in str_list[m]:
                table.append('OISEAUX')
            if 'SECRET' in str_list[m]:
                table.append('SECRET')
            if 'MOUSQUETAIRE' in str_list[m]:
                table.append('MOUSQUETAIRE')
            if 'PANACHE' in str_list[m]:
                table.append('PANACHE')
            if 'ORGUES' in str_list[m]:
                table.append('ORGUES')
            if 'RENAISSANCE' in str_list[m]:
                table.append('RENAISSANCE')
            if 'CHEVALIERS' in str_list[m]:
                table.append('CHEVALIERS')
            if 'ROYAUME' in str_list[m]:
                table.append('ROYAUME')
            if 'AUTOMATES' in str_list[m]:
                table.append('AUTOMATES')
            if 'CARILLON' in str_list[m]:
                table.append('CARILLON')
            if 'GRANDES' in str_list[m]:
                table.append('GRANDES')
            if 'SAPEURS' in str_list[m]:
                table.append('SAPEURS')
            if 'PEROUSE' in str_list[m]:
                table.append('PEROUSE')
            if 'AMOUREUX' in str_list[m]:
                table.append('AMOUREUX')

        """Reformat le tableau """
        for k in range(len(str_list)):
            show = ""
            if index < len(table):
                if table[index] in str_list[k]:
                    list.append(str(str_list[k]))
                    fin = k
                    index += 1
                else:
                    list[-1] = list[-1] + " " + str(str_list[k])

        list[-1] = list[-1] + str(str_list[fin + 1])
        final = []

        print("Extraction des heures ...")
        """Extraction des heures """
        for m in range(len(list)):
            dates = []

            match = re.findall(r'\d{2}:\d{2}', list[m])
            match1 = re.findall(r'\d{2} :\d{2}', list[m])
            match2 = re.findall(r'\d{2}: \d{2}', list[m])
            match3 = re.findall(r' \d{1}:\d{2}', list[m])

            for i in range(len(match)):
                date = datetime.datetime.strptime(match[i], '%H:%M').time()
                dates.append(date)
            if match1:
                for i in range(len(match1)):
                    date1 = datetime.datetime.strptime(match1[i], '%H :%M').time()
                    dates.append(date1)
            if match2:
                for i in range(len(match2)):
                    date2 = datetime.datetime.strptime(match2[i], '%H: %M').time()
                    dates.append(date2)
            if match3:
                for i in range(len(match3)):
                    match3[i] = match3[i].replace(" ", "0")
                    date3 = datetime.datetime.strptime(match3[i], '%H:%M').time()
                    dates.append(date3)

            dates = sorted(dates)

            if 'TRIOMPHE' in list[m]:
                final.append(["1", "Le Signe du Triomphe", "42", dates])
            if 'VIKINGS' in list[m]:
                final.append(["2", "Les Vikings", "26", dates])
            if 'OISEAUX' in list[m]:
                final.append(["3", "Le Bal des Oiseaux Fantomes", "33", dates])
            if 'SECRET' in list[m]:
                final.append(["4", "Le Secret de la Lance", "29", dates])
            if 'MOUSQUETAIRE' in list[m]:
                final.append(["5", "Mousquetaire de Richelieu", "32", dates])
            if 'PANACHE' in list[m]:
                final.append(["6", "Le Dernier Panache", "34", dates])
            if 'ORGUES' in list[m]:
                final.append(["7", "Les Orgues de Feu", "30", dates])
            if 'RENAISSANCE' in list[m]:
                final.append(["8", "La Renaissance du Chateau", "30", dates])
            if 'CHEVALIERS' in list[m]:
                final.append(["9", "Les Chevaliers de la Table Ronde", "17", dates])
            if 'ROYAUME' in list[m]:
                final.append(["10", "Le Premier Royaume", "18", dates])
            if 'AUTOMATES' in list[m]:
                final.append(["11", "Les Automates Musiciens", "7", dates])
            if 'CARILLON' in list[m]:
                final.append(["12", "Le Grand Carillon", "10", dates])
            if 'GRANDES' in list[m]:
                final.append(["13", "Les Grandes Eaux", "8", dates])
            if 'SAPEURS' in list[m]:
                final.append(["14", "Le Bal des Sapeurs", "9", dates])
            if 'PEROUSE' in list[m]:
                final.append(["18", "Le Mystere de la Perouse", "20", dates])
            if 'AMOUREUX' in list[m]:
                final.append(["19", "Les Amoureux de Verdun", "15", dates])

        jsonData = []
        json_resto = []

        """Ecriture json restaurant"""
        for k in range(len(restaurants)):
            json_temp = {}
            json_temp["id"] = restaurants[k][0]
            midi_pass = True
            prog = []
            midi = 0
            for m in range(len(restaurants[k][2])):
                prog_temp = {}
                prog_temp["hor"] = restaurants[k][2][m].strftime('%H:%M')
                prog.append(prog_temp)
                if restaurants[k][2][m].strftime('%H:%M') <= '15:00' and midi_pass:
                    midi = 1
                    midi_pass = False

            json_temp["midi"] = midi
            json_temp["prog"] = prog
            json_resto.append(json_temp)
        for info in json_resto:
            myresto = json.dumps(info)
            b = requests.post(urlPost, data=myresto, headers=headers)
            print(b.content)

        """Ecriture json show"""
        for k in range(len(final)):
            json_temp = {}
            json_temp["id"] = final[k][0]
            json_temp["midi"] = "0"
            prog = []

            for m in range(len(final[k][3])):
                prog_temp = {}
                prog_temp["hor"] = final[k][3][m].strftime('%H:%M')

                prog.append(prog_temp)

            json_temp["prog"] = prog
            jsonData.append(json_temp)


        for info in jsonData:
            mydata = json.dumps(info)
            x = requests.post(urlPost, data=mydata, headers=headers)
            print(x.content)


        """Trouve l'indice de fréquentation"""
        index_feq = 0
        for i in range(len(str_list)):
            if 'ou une animation.' in str_list[i]:
                index_feq = i
        freq_split = str_list[index_feq]
        freq = freq_split[-1]
        if not freq:
            """freq = re.findall(r'\d{1}', str_list[index_feq])"""
            freq = ['none']
        if len(freq) == 2:
            del freq[0]

        json_freq = []
        json_temp_freq = {}
        json_temp_freq["id"] = "999"
        json_temp_freq["midi"] = "0"
        date_now = datetime.datetime.now()
        date_now += datetime.timedelta(days=1)
        json_temp_freq["prog"] = [date_now.strftime("%d/%m/%Y %H:%M:%S")]
        json_freq.append(json_temp_freq)

        myfreq = json.dumps(json_freq[0])
        y = requests.post(urlPost, data=myfreq, headers=headers)
        print(y.content)
    print("Calcule : done !")


if __name__ == "__main__":
    main()
