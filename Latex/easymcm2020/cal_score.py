import numpy as np
import pandas as pd
import tqdm
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

if __name__ == '__main__':
    # dict store origin data
    data_tuple = {}
    # read data
    origin_data = pd.read_csv('data/hair_dryer.tsv', sep='\t', header=0, encoding="utf-8")
    part_data = pd.read_csv('data/a1.csv', encoding="utf-8")
    # prepare data
    # get data from source data
    review_id_origin = origin_data['review_id']
    review_id_part = part_data['review_id']
    # data from origin data
    helpful = origin_data['helpful_votes']
    total = origin_data['total_votes']
    product_id = origin_data['product_parent']
    date = origin_data['review_date']
    vine = origin_data['vine']
    verified = origin_data['verified_purchase']
    # data from part data
    review_score = part_data['review']
    star_score = part_data['star']
    review_id = list(review_id_part.values)
    for index in tqdm.tqdm(range(0, len(origin_data.values))):
        if review_id_origin[index] in review_id:
            date_split = date[index].split('/')
            index_part = review_id.index(review_id_origin[index])
            if date_split[-1] not in data_tuple.keys():
                data_tuple[date_split[-1]] = {date_split[0]: {review_id_origin[index]: (
                    str(product_id[index]), star_score[index_part], review_score[index_part], helpful[index],
                    total[index], vine[index], verified[index], date[index])}}
            else:
                exist_data = data_tuple[date_split[-1]]
                if date_split[0] not in exist_data.keys():
                    exist_data[date_split[0]] = {review_id_origin[index]: (
                        product_id[index], star_score[index_part], review_score[index_part], helpful[index],
                        total[index], vine[index], verified[index], date[index])}
                    data_tuple[date_split[-1]] = exist_data
                else:
                    exist_data[date_split[0]][review_id_origin[index]] = (
                        product_id[index], star_score[index_part], review_score[index_part], helpful[index],
                        total[index],
                        vine[index], verified[index], date[index])
                    data_tuple[date_split[-1]] = exist_data
    data_fre = {}
    for key, value in data_tuple.items():
        month = {}
        for s_key, s_value in value.items():
            tmp_star_dic = {}
            tmp_review_dic = {}
            for t_key, t_value in s_value.items():
                if str(t_value[1]) not in tmp_star_dic.keys():
                    tmp_star_dic[str(t_value[1])] = 1
                else:
                    tmp_star_dic[str(t_value[1])] += 1

                if str(t_value[2]) not in tmp_review_dic.keys():
                    tmp_review_dic[str(t_value[2])] = 1
                else:
                    tmp_review_dic[str(t_value[2])] += 1
            month[s_key] = {'star': tmp_star_dic, 'review': tmp_review_dic}
        data_fre[key] = month
    data_pro = {}
    for key, value in data_fre.items():
        month = {}
        for s_key, s_value in value.items():
            tmp_star_dic = {}
            tmp_review_dic = {}
            sum_star = 0
            sum_review = 0
            for t_key, t_value in s_value['star'].items():
                sum_star += t_value
            for t_key, t_value in s_value['star'].items():
                tmp_star_dic[t_key] = t_value / sum_star

            for t_key, t_value in s_value['review'].items():
                sum_review += t_value
            for t_key, t_value in s_value['review'].items():
                tmp_review_dic[t_key] = t_value / sum_review
            month[s_key] = {'star': tmp_star_dic, 'review': tmp_review_dic}
        data_pro[key] = month
    e = {}
    for key, value in data_pro.items():
        month = {}
        for s_key, s_value in value.items():
            e_star = 0
            e_review = 0
            for t_key, t_value in s_value['star'].items():
                e_star += t_value * np.log(t_value)
            e_star = (-1.0 / np.log(5)) * e_star
            for t_key, t_value in s_value['review'].items():
                e_review += t_value * np.log(t_value)
            e_review = (-1.0 / np.log(5)) * e_star
            month[s_key] = {'star': e_star, 'review': e_review}
        e[key] = month
    w = {}
    for key, value in e.items():
        month = {}
        for s_key, s_value in value.items():
            e_star = s_value['star']
            e_review = s_value['review']
            w1 = (1 - e_star) / (2 - (e_star + e_review))
            w2 = (1 - e_review) / (2 - (e_star + e_review))
            month[s_key] = {'star': w1, 'review': w2}
        w[key] = month
    # model part 2
    helpful_dic = {}
    for key, value in w.items():
        month = {}
        for s_key, s_value in value.items():
            review_item = {}
            product_total_set = {}
            reviews = data_tuple[key][s_key]
            for t_key, t_value in reviews.items():
                if len(product_total_set) == 0:
                    tmp_total = [t_value[4]]
                    product_total_set[t_value[0]] = tmp_total
                else:
                    if t_value[0] not in product_total_set.keys():
                        tmp_total = [t_value[4]]
                        product_total_set[t_value[0]] = tmp_total
                    else:
                        product_total_set[t_value[0]].append(t_value[4])
            for t_key, t_value in reviews.items():
                if t_value[4] == 0:
                    hvr = 0.5
                else:
                    hvr = t_value[3] / t_value[4]
                total_list = product_total_set[t_value[0]]
                max_value = max(total_list)
                min_value = min(total_list)
                if (max_value - min_value) == 0:
                    if max_value == 0:
                        scale = 0
                    else:
                        scale = 1
                else:
                    scale = (t_value[4] - min_value) / (max_value - min_value)
                review_item[t_key] = (str(t_value[0]), t_value[1], t_value[2], hvr, scale, t_value[5], t_value[6])
            month[s_key] = review_item
        helpful_dic[key] = month
    # model part 3
    right = [[0.4, 0.6], [1.0, 0]]
    scores = {}
    for key, value in helpful_dic.items():
        month = {}
        for s_key, s_value in value.items():
            score_item = {}
            product_score_set = {}
            product_k_set = {}
            alpha = w[key][s_key]
            for t_key, t_value in s_value.items():
                star_review_score = alpha['star'] * t_value[1] + alpha['review'] * t_value[2]
                hvr_k = t_value[3] * t_value[4]
                if t_value[5] == 'Y':
                    i = 1
                else:
                    i = 0
                if t_value[6] == 'Y':
                    j = 1
                else:
                    j = 0
                authority_k = right[i][j]
                score = authority_k * star_review_score + hvr_k * star_review_score
                k = authority_k + hvr_k
                if len(product_score_set) == 0:
                    product_score_set[t_value[0]] = score
                    product_k_set[t_value[0]] = k
                else:
                    if t_value[0] not in product_score_set.keys():
                        product_score_set[t_value[0]] = score
                        product_k_set[t_value[0]] = k
                    else:
                        product_score_set[t_value[0]] += score
                        product_k_set[t_value[0]] += k
            for t_key, t_value in product_score_set.items():
                score_item[t_key] = t_value / (product_k_set[t_key])
            month[s_key] = score_item
        scores[key] = month
    measure = {}
    for key, value in scores.items():
        for s_key, s_value in value.items():
            for t_key, t_value in s_value.items():
                if len(measure) == 0:
                    month = {s_key: t_value}
                    year = {key: month}
                    measure[t_key] = year
                else:
                    if t_key not in measure.keys():
                        month = {s_key: t_value}
                        year = {key: month}
                        measure[t_key] = year
                    else:
                        year = measure[t_key]
                        if key not in year.keys():
                            year[key] = {s_key: t_value}
                            measure[t_key] = year
                        else:
                            year[key][s_key] = t_value
                            measure[t_key] = year
    with open('result/product_score_per_month_1.json', 'w') as f:
        json.dump(measure, f, cls=NpEncoder)