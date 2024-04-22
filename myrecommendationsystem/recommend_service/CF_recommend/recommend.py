import numpy as np
from keras.layers import Embedding, LSTM, Dense
from keras.models import Sequential
from sklearn.preprocessing import LabelEncoder
import pickle
from .spider163 import get_song_attr


def generate_recommendations(model, user_sequence, num_recommendations=10):
    # 将用户序列转换为适合模型输入的格式
    # 假设 user_sequence 是一个包含用户历史歌曲ID的列表
    sequence_length = model.input_shape[1]  # 获取模型期望的输入序列长度
    user_sequence = user_sequence[-sequence_length:]  # 保留最近的行为

    # 如果序列太短，我们可能需要进行填充
    if len(user_sequence) < sequence_length:
        user_sequence = [0] * (sequence_length - len(user_sequence)) + user_sequence

    # 将序列转换为模型的输入格式
    input_sequence = np.array(user_sequence).reshape(1, -1)

    # 使用模型进行预测
    predicted_scores = model.predict(input_sequence)[0]

    # 获取最高分数的索引，即推荐的歌曲ID
    recommended_song_ids = np.argsort(predicted_scores)[::-1][:num_recommendations]

    return recommended_song_ids



def get_RNN_recommend(model=pickle.load(open('RNN_recommend/RNN_model.pkl', 'rb')), user_sequence = [5, 25, 15, 35], num_recommendations=10):
    recommendations = generate_recommendations(model, user_sequence, num_recommendations)
    # 将歌曲ID转换回歌曲名称或其他有用的表示（如果需要）
    # song_encoder = LabelEncoder()  # 假设你之前已经拟合了一个LabelEncoder
    # recommended_songs = song_encoder.inverse_transform(recommendations)

    print("推荐的歌曲ID:", recommendations)
    # print("推荐的歌曲:", recommended_songs)
    songs=[]
    for song_id in recommendations:
        try:
            song_attr=get_song_attr(song_id=song_id)
            print(song_attr)
            if song_attr[0]==200:
                song_dict={}
                title, artist, rating,url=song_attr[1:]
                song_dict['title']=title
                song_dict['artist']=artist
                song_dict['rating']=rating
                song_dict['url']=url
                songs.append(song_dict)
        except Exception as e:
            print(e)
    return songs


if  __name__ == '__main__':
    get_RNN_recommend()
