import pickle
import numpy as np

topHit_emoji = {
    'cooked_to_order': '🍳',
    'noodles': '🍜',
    'drinks': '🍹',
    'snacks': '🍿',
    'bakery': '🥐',
    'grill': '🍖',
    'coffee/tea': '☕',
    'single_dish': '🍛',
    'ramen': '🍜',
    'congee/rice_soup': '🥣',
    'dessert': '🍰',
    'fried_chicken': '🍗',
    'shaved_ice': '🍧',
    'sushi': '🍣',
    'milk_tea': '🧋',
    'fruits': '🍎',
    'somtum': '🥗',
    'steak': '🥩',
    'shabu/bbq': '🍲',
    'dimsum': '🥟',
    'fast_food': '🍔',
    'burgers': '🍔',
    'spaghetti': '🍝',
    'side_dish': '🧆',
    'ice-cream': '🍦',
    'seafood': '🦞',
    'healthy': '🥗',
    'pizza': '🍕',
    'pickled_food': '🥒',
    'ice': '🧊'
}

class recommender():

    def __init__(self):
        self.model = pickle.load(open('./model/'+ 'nn_model' + '.pkl', 'rb')) # Sklearn model
        self.encoder = pickle.load(open('./model/'+ 'shop_encoder' + '.pkl', 'rb')) # Dict

    def preprocess(self, df):
        shop_ids = df.shop_id.values
        encoded_shop_ids = [self.encoder[v] for v in shop_ids]

        return np.mean(encoded_shop_ids, axis=0), shop_ids
    
    def postprocess(self, embedding_position, seen_shop_ids):
        # Get key or shop_id from position
        keys = list(self.encoder.keys())
    
        list_of_shopIds = [keys[i] for i in embedding_position if keys[i] not in seen_shop_ids]

        return list_of_shopIds

    def get_playlist(self, df, k):

        df = df[df['favorite'] == True]

        embdedding_vector, seen_shop_ids = self.preprocess(df)
        k = 20 if k > 20 else k

        topK = self.model.kneighbors(X=[embdedding_vector], n_neighbors=20, return_distance=False)

        topShops = self.postprocess(topK[0], seen_shop_ids)
        
        return topShops
    
    def get_dish_bubble(self, df):

        df = df[df['favorite'] == True]

        purchased_list = list(df[['shop_name', 'shop_category']].groupby('shop_category').count().index)
        topHit = list(topHit_emoji.keys())

        for i in range(len(topHit)):
            if (topHit[i] not in purchased_list) & (len(purchased_list) <= 11):
                purchased_list.append(topHit[i])

        return purchased_list
