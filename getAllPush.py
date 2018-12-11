import re
import datetime

config = None

def get_all_push(soup):
    # get all reply pushes
    all_push = soup.find_all('div', class_='push')
    parsed_data = []
    no_ip_counter = 0
    for entry in all_push:
        try:
            tmp = {}
            tmp['tag'] = entry.find('span', class_='push-tag').text

            tmp['id'] = entry.find('span', class_='push-userid').text

            tmp['content'] = entry.find('span', class_='push-content').text.strip()[2:]

            ip_date_stuff = entry.find('span', class_='push-ipdatetime').text.strip()
            tokens = ip_date_stuff.split(' ')
            tmp['ip'] = tokens[0]
            tt = tokens[1].split('/')
            tmp['month'] = tt[0]
            tmp['day'] = tt[1]
            tmp['time'] = tokens[2]
            parsed_data.append(tmp)
        except AttributeError:
            if not 'warning-box' in entry.get('class'): # the page may be too big, PTT webpage won't show all the pushes
                print("[Error] Parsing push error: {0}".format(entry), file=config.stderr)
                exit(1)
        except IndexError:
            if not len(tokens) != 3: # ip not recorded
                print("[Error] ip-data stuff parsing error: {0}".format(entry), file=config.stderr)
            no_ip_counter += 1
    return parsed_data, no_ip_counter

def get_poster(soup):
    tmp = {'tag' : 'poster'}

    # find poster id
    ps_s = soup.find_all('span', class_='article-meta-value')[0].text.split(' ')[0]
    tmp['id'] = ps_s

    # find poster ip
    ip_s = soup.find('span', text=re.compile(r'^※ 發信站: 批踢踢實業坊\(ptt\.cc\), 來自: \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
    try:
        ip_f = re.search(r'^※ 發信站: 批踢踢實業坊\(ptt\.cc\), 來自: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', ip_s.text).group(1)
    except AttributeError:
        print("[Wraning] Cannot find poster's ip.", file=config.stderr)
        ip_f = ""
    tmp['ip'] = ip_f

    # get page title
    t_s = soup.find('meta', property='og:title')
    tmp['title'] = t_s['content']

    # find post time
    ps_s = soup.find_all('span', class_='article-meta-value')[-1]
    dt = datetime.datetime.strptime(ps_s.text, '%c')
    tmp['month'] = dt.strftime('%m')
    tmp['day'] = dt.strftime('%d')
    tmp['time'] = dt.strftime('%X')
    return tmp
