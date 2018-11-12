def get_all_push (soup):
    # get all reply pushes
    all_push = soup.find_all('div', class_ = 'push')
    parsed_data = []
    for entry in all_push:
        tmp = {}
        tmp['tag'] = entry.find('span', class_ = 'push-tag').text


        tmp['id'] = entry.find('span', class_ = 'push-userid').text

        tmp['content'] = entry.find('span', class_ = 'push-content').text.strip()[2:]
        
        ip_date_stuff = entry.find('span', class_ = 'push-ipdatetime').text.strip()
        tokens = ip_date_stuff.split(' ')
        tmp['ip'] = tokens[0]
        tt = tokens[1].split('/')
        tmp['month'] = tt[0]
        tmp['day'] = tt[1]
        tmp['time'] = tokens[2]
        parsed_data.append(tmp)
    
    return parsed_data
