import tweepy

consumer_key, consumer_secret = 'CONSUMER_KEY HERE', 'CONSUMER_SECRET_HERE'
access_token, access_token_secret = 'ACCESS_TOKEN_HERE', 'ACCESS_TOKEN_SECRET_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

with open('list_ordered.txt') as f:
    ids = list(map(int,f.readlines()))

with open('list_completed.txt') as f:
    completed_ids = list(map(int,f.readlines()))

completed_ids = set(completed_ids)
final_list = [id for id in ids if id not in completed_ids]

print('--STARTING BLOCKS--')
print('Accounts blocked so far :', len(completed_ids))
print('Accounts left to block  :', len(final_list))
for id in final_list:
    try:
        user_blocked = api.create_block(user_id=id)
        print(user_blocked.screen_name)
    except tweepy.NotFound:
        print(f'user {id} does not exist, skipping')
    except Exception as e:
        print('ERROR OCCURED:', e)
        break

    completed_ids.add(id)
else:
    print('--ALL BLOCKS COMPLETED!--')

print('SAVING PROGRESS AND EXITING')
progress = [f'{id}\n' for id in completed_ids]
with open('list_completed.txt', 'w') as f:
    f.writelines(progress)