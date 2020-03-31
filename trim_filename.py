import os
import shutil

if __name__ == '__main__':
    target_dir = r'Z:\781623489-20180821\home\JAV'
    for movie_dir in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, movie_dir)) and len(os.path.join(target_dir, movie_dir)) > 50:
            try:
                os.rename(os.path.join(target_dir,movie_dir),os.path.join(target_dir,movie_dir[:40]))
                print(os.path.join(target_dir,movie_dir) + '\nhas been renamed to\n' + os.path.join(target_dir,movie_dir[:40]))
            except FileExistsError:
                print('Directory alreay exists: ' + os.path.join(target_dir,movie_dir[:40]))
                shutil.rmtree(os.path.join(target_dir, movie_dir))

    print('All finished')
