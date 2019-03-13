import requests
import json
import random
from randomuser import RandomUser

config = json.load(open('config.json'))

api = lambda url: f'http://localhost:8000/api/{url}'

user_count = 0
users = []
posts = []
while user_count != config['number_of_users']:
    user = RandomUser()
    user_data = {
        'username': user.get_username(),
        'password': user.get_password(),
        'email': user.get_email(),
        'first_name': user.get_first_name(),
        'last_name': user.get_last_name()
    }
    resp = requests.post(api('users/'), json=user_data)
    if resp.status_code == 201:
        user_count += 1
        user_data['id'] = resp.json().get('id')
    else:
        continue
    print('USER CREATED')
    token_data = {'username': user_data['username'], 'password': user_data['password']}
    resp = requests.post(api('token/'), json=token_data)
    if resp.status_code == 200:
        user_data['access'] = resp.json().get('access')
        user_data['refresh'] = resp.json().get('refresh')
        users.append(user_data)
    else:
        continue
    print('TOKEN CREATED')
    headers = {'Authorization': 'Bearer {}'.format(user_data['access'])}
    for i in range(random.randint(1, config['max_posts_per_user'])):
        post_data = {
            'user': user_data['id'],
            'title': 'Post #{} from user {}'.format(i, user_data['username']),
            'content': 'Post content form user {}'.format(user_data['username'])
        }
        resp = requests.post(api('users/{}/posts/'.format(user_data['id'])), json=post_data, headers=headers)
        if resp.status_code == 200:
            post_data['id'] = resp.json().get('id')
            posts.append(post_data)
        else:
            continue
        print('POST CREATED')


for user in users:
    like_count = random.randint(1, config['max_likes_per_user'])
    print(f'LIKES {like_count}')
    headers = {'Authorization': 'Bearer {}'.format(user['access'])}
    while like_count:
        post = random.choice(posts)
        resp = requests.post(api('users/{}/posts/{}/likes/'.format(user['id'], post['id'])), headers=headers)
        if resp.status_code == 200:
            like_count -= 1
            print('LIKE')

