# -*- coding: utf-8 -*-

def getPriceFromText(text):
    price = 0.

    for word in text:
        if '€' in word:
            potential_price = word.replace('€', '')
            is_number = potential_price.replace('.','',1).isdigit()
            if is_number: price = max(price, float(potential_price))

    return price

def getClubFromText(text):
    isApolo = False
    isRazz = False
    
    for word in text:
        if 'Apolo' in word: isApolo = True
        if 'Cupcake' in word: isApolo = True
        if 'Nasty' in word: isApolo = True
        if 'Cannibal' in word: isApolo = True

        if 'Razz' in word: isRazz = True
        if 'Dirty' in word: isRazz = True

    if isApolo and isRazz: return 'Undefined'
    if isApolo: return 'Apolo'
    if isRazz: return 'Razzmatazz'

    return 'Undefined'

def isInRange(word, start, finish):
    if not word.isdigit(): return False
    return start <= int(word) and int(word) <= finish

def getDateFromText(text):
    for word in text:
        if word.count('/') >= 2:
            if len(word) < 10: continue

            day = word[0:2]
            month = word[3:5]
            year = word[6:10]

            isday = isInRange(day, 1, 31)
            ismonth = isInRange(month, 1, 12)
            isyear = isInRange(year, 2000, 2100)

            if isday and ismonth and isyear:
                return day + '/' + month + '/' + year

    return 'Undefined'

def getWeekdayFromText(day, month, year):
    import datetime

    weekday = datetime.datetime(
        int(year),
        int(month),
        int(day)
    ).weekday()

    if weekday == 0: return 'Dilluns'
    if weekday == 1: return 'Dimarts'
    if weekday == 2: return 'Dimecres'
    if weekday == 3: return 'Dijous'
    if weekday == 4: return 'Divendres'
    if weekday == 5: return 'Dissabte'
    if weekday == 6: return 'Diumenge'

    return 'Undefined'

def fillPDFData(tickets_data, filename):
    import fitz
    doc = fitz.open(filename)

    for i, page in enumerate(doc):
        # Step 0: Initialize data
        tickets_data.append({})
        
        # Step 1: Get text from page
        text = page.get_text('text')
        splitted_text = text.replace('\n',' ').replace('(',' ').replace(')',' ').split()
        
        # Step 2: Get data from page
        tickets_data[i]['price'] = getPriceFromText(splitted_text)
        tickets_data[i]['date'] = getDateFromText(splitted_text)
        tickets_data[i]['clubname'] = getClubFromText(splitted_text)

        if tickets_data[i]['date'] != 'Undefined':
            day, month, year = tickets_data[i]['date'].split('/')
            tickets_data[i]['diasetmana'] = getWeekdayFromText(day, month, year)