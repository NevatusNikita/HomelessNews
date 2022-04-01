from requests import get, post, delete

# print(get('http://127.0.0.1:5000/api/news').json())
#
# print(get('http://127.0.0.1:5000/api/news/1').json())
#
# print(get('http://127.0.0.1:5000/api/news/999').json())
#
# print(get('http://127.0.0.1:5000/api/news/q').json())

# print(post('http://127.0.0.1:5000/api/news').json())
#
# print(post('http://127.0.0.1:5000/api/news',
#            json={'title': 'Заголовок'}).json())
#
# print(post('http://127.0.0.1:5000/api/news',
#            json={'title': 'Заголовок',
#                  'content': 'Текст новости',
#                  'user_id': 1,
#                  'is_private': False}).json())

# print(delete('http://127.0.0.1:5000/api/news/999').json())
# # новости с id = 999 нет в базе
#
# print(delete('http://127.0.0.1:5000/api/news/1').json())
#
print(get('http://127.0.0.1:5000/api/news').json())
