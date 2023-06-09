import numpy as np
import pandas as pd
import ast
import json
import pickle
import itertools

def non_personalized_rec(input_ingredients, recipe_liked, tags, option):
    merged_df = pd.read_csv('main/core/csv/dataset.csv', usecols=['name','recipe_id','minutes','tags','n_steps','steps','ingredients','n_ingredients','rating'])
    ing_rec = pd.read_csv('main/core/csv/ing_rec.csv', usecols=['ingredient','recipes'])

    def str_to_list(l):
        try:
            return ast.literal_eval(l)
        except ValueError:
            return []
    def add_l(l):
        new_l = json.loads(l)
        s = sum(new_l)
        return s
    
    merged_df['tags'] = merged_df['tags'].apply(str_to_list)
    merged_df = merged_df[merged_df['tags'].apply(lambda x: all(item in x for item in tags))]
    ing_rec['recipes'] = ing_rec['recipes'].apply(str_to_list)
    merged_df['steps'] = merged_df['steps'].apply(str_to_list)
    filtered_table = ing_rec[ing_rec['ingredient'].isin(input_ingredients)]
    l = filtered_table['recipes'].tolist()

    def find_intersection(lists):
        # convert each list to a set
        sets = [set(lst) for lst in lists]
        # take the intersection of all sets
        intersection = set.intersection(*sets)
        # convert the intersection back to a list
        result = list(intersection)
        return result
    r_with_other_ing = find_intersection(l)

    def exact_recipes(r_with_other_ing):
        req_ing_count = len(input_ingredients)
        df_recepies = merged_df[merged_df['recipe_id'].isin(r_with_other_ing)]
        df_ing  = df_recepies[df_recepies['n_ingredients']==req_ing_count]
        df_ing = df_ing.sort_values(by=['rating'], ascending=[False])
        return df_ing[0:10]
    def low_cal(r_with_other_ing):
        df_recepies = merged_df[merged_df['recipe_id'].isin(r_with_other_ing)]
        df_recepies['calories'] = df_recepies['nutrition'].apply(add_l)
        df_low_cal = df_recepies.sort_values(by=['calories', 'rating'], ascending=[True, False])
        return df_low_cal[0:10]
    def few_steps(r_with_other_ing):
        df_recepies = merged_df[merged_df['recipe_id'].isin(r_with_other_ing)]
        df_low_steps = df_recepies.sort_values(by=['n_steps', 'rating'], ascending=[True, False])
        return df_low_steps[0:10]
    def order_by_time(r_with_other_ing):
        df_recepies = merged_df[merged_df['recipe_id'].isin(r_with_other_ing)]
        df_low_time = df_recepies.sort_values(by=['minutes', 'rating'], ascending=[True, False])
        return df_low_time[0:10]


    ans = {}
    if option == 1:
        ans['res'] = exact_recipes(r_with_other_ing).to_dict(orient='records')
    elif option == 2:
        ans['res'] = low_cal(r_with_other_ing).to_dict(orient='records')
    elif option == 3:
        ans['res'] = few_steps(r_with_other_ing).to_dict(orient='records')
    elif option == 4:
        ans['res'] = order_by_time(r_with_other_ing).to_dict(orient='records')
    
    return ans


def personalized_rec(input_ingredients, user_previous_liked):
    df = pd.read_csv('main/core/csv/dataset.csv', usecols=['name','recipe_id','minutes','tags','n_steps','steps','ingredients','n_ingredients','rating'])
    df_ingredients = pd.read_csv('main/core/csv/ing_rec.csv', usecols=['ingredient','recipes'])

    def str_to_list(l):
        try:
            return ast.literal_eval(l)
        except ValueError:
            return []

    def create_index(df):
        inverted_index = {} 
        count = 0
        for recipe in df['ingredients_list']:
            for ing in recipe:
                if ing not in inverted_index:  
                    inverted_index[ing]=[] 
                inverted_index[ing].append(df['recipe_id'][count])
            count += 1
        return inverted_index

    def find_intersection(lists):
        sets = [set(lst) for lst in lists]
        intersection = set.intersection(*sets)
        result = list(intersection)
        return result

    def boolean_retrieval(input_ingredients):
        inverted_index = create_index(df)
        word_doc = []
        for w in input_ingredients:
            if w in inverted_index:
               word_doc.append(list(inverted_index[w]))
        matching_recipes=find_intersection(word_doc)
        return matching_recipes
    
    def jaccard_similarity(list1, list2):
        set1 = set(list1)
        set2 = set(list2)
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        similarity = len(intersection) / len(union)
        return similarity

    def item_item(each_liked_id):
        ingredients_dict = {}
        for i, ingredient in enumerate(df_ingredients['ingredient']):
            ingredients_dict[ingredient] = i
        recipe_list = df['recipe_id'].tolist()
        recipe_list = sorted(recipe_list)
        with open('main/core/csv/recipe_cosine_sim.pickle', 'rb') as f:
            recipe_sim_arr = pickle.load(f)
            recipe_sim_arr = np.array(recipe_sim_arr)
        item_ans=[]
        if recipe_to_id[each_liked_id]<10000:
            similar_recipes=recipe_sim_arr[recipe_to_id[each_liked_id]]
            ascending_indices = np.argsort(similar_recipes)
            descending_indices = ascending_indices[::-1]
            count=0
            for i in descending_indices:
                item_ans.append(id_to_recipe[i])
                count+=1
                if count==10:
                    break
        return item_ans
    
    
    df['ingredients_list'] = df['ingredients'].apply(str_to_list)
    df['tags_list'] = df['tags'].apply(str_to_list)
    df['steps_list'] = df['steps'].apply(str_to_list)
    recipe_ids=boolean_retrieval(input_ingredients)
    # item-item
    all_items=[]
    df_sorted = df.sort_values(by=['rating'], ascending=False)
    df_sorted = df_sorted.reset_index(drop=True)
    df_sorted['recipe_id_name'] = df_sorted.index 
    recipe_to_id = dict(zip(df_sorted['recipe_id'], df_sorted['recipe_id_name']))
    id_to_recipe = dict(zip(df_sorted['recipe_id_name'],df_sorted['recipe_id']))    
    for each_liked_id in user_previous_liked:  
             if each_liked_id in recipe_ids and recipe_to_id[each_liked_id]<10000:
                item_ans=item_item(each_liked_id)
                if len(all_items) == 0:
                      all_items.append(item_ans)
                else:
                    all_items.extend(item_ans)
    # all_items=[x for x in all_items if x != []]
    all_items = list(itertools.chain(*all_items))
    selected_rows = df.loc[df['recipe_id'].isin(all_items)]
    subset_df = df[df['recipe_id'].isin(recipe_ids)]
    subset_df['similarity'] = subset_df['ingredients_list'].apply(lambda x: jaccard_similarity(x, input_ingredients))
    subset_df = subset_df.sort_values(by='similarity',ascending=False)
    tags_list = []
    for lst in subset_df['tags_list'].head(5):
     tags_list.extend(lst)
    subset_df['similarity_tags'] = subset_df['tags_list'].apply(lambda x: jaccard_similarity(x,tags_list))
    subset_df = subset_df.sort_values(by='similarity_tags',ascending=False)
    ans = {}
    subset_df['tags'] = subset_df['tags_list']
    subset_df['steps'] = subset_df['steps_list']
    selected_rows['tags'] = selected_rows['tags_list']
    selected_rows['steps'] = selected_rows['steps_list']
    jacard_ob = subset_df[0:5].to_dict(orient='records')
    iicf_ob2 = selected_rows[0:5].to_dict(orient='records')
    ans['res'] = jacard_ob + iicf_ob2
    return ans