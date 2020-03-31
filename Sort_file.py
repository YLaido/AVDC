import os
import shutil,traceback
from os import path

#  Bump movies to upper level
def sort_file(target_dir):
    extensions = ['mp4', 'avi', 'wmv', 'mkv', 'mov', 'rmvb', 'flv', 'mpg', 'iso']
    video_count = 0
    print('checking '+target_dir)
    for movie_dir in os.listdir(path.join(target_dir)): # 示例 movie_dir : Z:\781623489-20180821\KS-1_PT\GIGA 'GIRO' Megapack\movies\GIRO-86
        if path.isdir(path.join(target_dir, movie_dir)):
            file_num = 0
            for count, filename in enumerate(os.listdir(path.join(target_dir, movie_dir)),start=1):
                if not path.isdir(path.join(target_dir, movie_dir, filename)):
                    if any(ext in os.path.splitext(filename)[1].lower() for ext in extensions):
                        print(filename + ' is a video.')
                        file_num += 1
                        video_count += 1
                        try:
                            os.rename(path.join(target_dir, movie_dir, filename),path.join(target_dir, filename))  # 影片移至上一级
                            print('Moved ' + path.join(target_dir, movie_dir, filename) + ' to ' + path.join(target_dir, filename))
                        except:
                            traceback.print_exc()
                    elif count == file_num:
                        print('Removing empty dir: ' + path.join(target_dir, movie_dir))
                        shutil.rmtree(path.join(target_dir, movie_dir))
                        break
                    else:
                        print(path.join(target_dir, movie_dir, filename) + ' is not a video.')
                        file_num += 1
            file_num = 0
    print("total movie: " + str(video_count))


if __name__ == '__main__':
    target_dir = r'Z:\DJJ-3\KS-1_PT\史上最全蒼井空79部合集71.2G\AV'
    sort_file(target_dir)
    print('finished.')

