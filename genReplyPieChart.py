import argparse
import collections
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
import numpy as np
import findLocation

if __name__ == '__main__':
    # parse argument
    argP = argparse.ArgumentParser(description="Input a web ptt url and the program will draw the replyers location on a chart.")
    argP.add_argument('INPUT', help="The target web ptt url.")
    arg = argP.parse_args()

    result = findLocation.main([arg.INPUT, '-db', 'IP2LOCATION-LITE-DB5.CSV'])
    ip_record_ratio = result['ip_record_ratio']
    poster = result['poster']
    foreign_push = result['foreign_push']
    foreign_push_acc = result['foreign_push_acc']
    foreign_push_id = result['foreign_push_id']
    taiwan_push = result['taiwan_push']
    taiwan_push_acc = result['taiwan_push_acc']

    inner_data = []
    inner_data_tag_t = []
    inner_data.extend(taiwan_push_acc.values())
    inner_data_tag_t.extend(taiwan_push_acc.items())
    inner_data.extend(foreign_push_acc.values())
    inner_data_tag_t.extend(foreign_push_acc.items())
    inner_data_tag = ["{0}: {1}".format(i[0], i[1]) for i in inner_data_tag_t]
    all_push_count = 0
    for i in inner_data:
        all_push_count += i

    if poster['country_name'] != 'Taiwan':
        poster_from = poster['country_name']
    else:
        poster_from = poster['city']

    # draw
    font_path = "NotoSerifCJKtc-Regular.otf"
    fprop = mfm.FontProperties(fname=font_path)

    cmap = plt.get_cmap('gnuplot')
    c_tmp = [cmap(i) for i in np.linspace(0, 20, 20*len(inner_data_tag))]
    color_map = dict(zip([i[0] for i in inner_data_tag_t], c_tmp))
    def get_c(k):
        return color_map[k.split(':')[0]]

    radius = 1
    outer_width = 0.1
    inner_width = 0.5

    # all push
    fig, ax = plt.subplots()
    plt.title("{0}\nip record={1}, poster={2}\nAll Reply".format(poster['title'], ip_record_ratio, poster_from), fontproperties=fprop, fontsize='large')
    ax.set(aspect='equal')
    ax.pie([len(taiwan_push), len(foreign_push)], radius=radius, wedgeprops=dict(width=outer_width, edgecolor='w'))
    c = [get_c(i) for i in inner_data_tag]
    wedges, texts = ax.pie(inner_data, radius=radius - outer_width, wedgeprops=dict(width=inner_width, edgecolor='w'), colors=c)
    lgd = ax.legend(wedges, inner_data_tag, title='Country/City', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), prop=fprop, ncol=2)
    plt.savefig("gen/{0}.png".format(poster['title']), bbox_extra_artists=(lgd,), bbox_inches='tight')

    # nice
    taiwan_push_t = [i for i in taiwan_push if i['tag'] == '推']
    foreign_push_t = [i for i in foreign_push if i['tag'] == '推']
    taiwan_push_acc = collections.defaultdict(lambda: 0)
    foreign_push_acc = collections.defaultdict(lambda: 0)
    for i in taiwan_push_t:
        taiwan_push_acc[i['city']] += 1
    for i in foreign_push_t:
        foreign_push_acc[i['country_name']] += 1
    inner_data = []
    inner_data_tag = []
    inner_data.extend(taiwan_push_acc.values())
    inner_data_tag.extend(taiwan_push_acc.items())
    inner_data.extend(foreign_push_acc.values())
    inner_data_tag.extend(foreign_push_acc.items())
    inner_data_tag = ["{0}: {1}".format(i[0], i[1]) for i in inner_data_tag]

    fig, ax = plt.subplots()
    plt.title("{0}\nip record={1}, poster={2}\nLike".format(poster['title'], ip_record_ratio, poster_from), fontproperties=fprop, fontsize='large')
    ax.set(aspect='equal')
    ax.pie([len(taiwan_push_t), len(foreign_push_t)], radius=radius, wedgeprops=dict(width=outer_width, edgecolor='w'))
    c = [get_c(i) for i in inner_data_tag]
    wedges, texts = ax.pie(inner_data, radius=radius - outer_width, wedgeprops=dict(width=inner_width, edgecolor='w'), colors=c)
    lgd = ax.legend(wedges, inner_data_tag, title='Country/City', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), prop=fprop, ncol=2)
    plt.savefig("gen/{0}_like.png".format(poster['title']), bbox_extra_artists=(lgd,), bbox_inches='tight')

    # dislike
    taiwan_push_t = [i for i in taiwan_push if i['tag'] == '噓']
    foreign_push_t = [i for i in foreign_push if i['tag'] == '噓']
    taiwan_push_acc = collections.defaultdict(lambda: 0)
    foreign_push_acc = collections.defaultdict(lambda: 0)
    for i in taiwan_push_t:
        taiwan_push_acc[i['city']] += 1
    for i in foreign_push_t:
        foreign_push_acc[i['country_name']] += 1
    inner_data = []
    inner_data_tag = []
    inner_data.extend(taiwan_push_acc.values())
    inner_data_tag.extend(taiwan_push_acc.items())
    inner_data.extend(foreign_push_acc.values())
    inner_data_tag.extend(foreign_push_acc.items())
    inner_data_tag = ["{0}: {1}".format(i[0], i[1]) for i in inner_data_tag]

    fig, ax = plt.subplots()
    plt.title("{0}\nip record={1}, poster={2}\nDislike".format(poster['title'], ip_record_ratio, poster_from), fontproperties=fprop, fontsize='large')
    ax.set(aspect='equal')
    ax.pie([len(taiwan_push_t), len(foreign_push_t)], radius=radius, wedgeprops=dict(width=outer_width, edgecolor='w'))
    c = [get_c(i) for i in inner_data_tag]
    wedges, texts = ax.pie(inner_data, radius=radius - outer_width, wedgeprops=dict(width=inner_width, edgecolor='w'), colors=c)
    lgd = ax.legend(wedges, inner_data_tag, title='Country/City', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), prop=fprop, ncol=2)
    plt.savefig("gen/{0}_dislike.png".format(poster['title']), bbox_extra_artists=(lgd,), bbox_inches='tight')
