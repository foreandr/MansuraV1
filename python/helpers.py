import os as os
import inspect
from os import listdir
from PIL import Image as PImage

try:
    from python.MODULES import *
except:
    from MODULES import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_and_save_dir(path):
    # Create a new directory because it does not exist
    print("RUNNING CHECK AND SAVE DIR")
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def print_segment():
    print("====================================")
    
def print_green(string):
    print(bcolors.OKGREEN + str(string) + bcolors.ENDC)


def print_title(string):
    print(bcolors.HEADER + bcolors.UNDERLINE + str(string) + bcolors.ENDC)


def print_error(string):
    print(bcolors.FAIL + str(string) + bcolors.ENDC)


def print_warning(string):
    print(bcolors.WARNING + str(string) + bcolors.ENDC)     
    
def translate_link_to_html(link):
    # print("ORIGIN", link)
    
    if link == None:
        return link
    try:
        if "tiktok" in link:
            tiktok_template = '''                
                <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME/video/LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID" data-video-id="LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID" style="max-width: 605px;min-width: 325px;"> 
                    <section> 
                        <a href="https://www.tiktok.com/@LOCATION_FOR_TIKTOK_UPLOADER_USERNAME?refer=embed"></a>
                    </section>
                </blockquote>
                <!--PROPERLY EMBEDDED HTML TAG-->
                '''
            #print("THIS IS A TIKTOK VIDEO")
            
            #A TYPICAL LINK LOOKS LIKE THIS https://www.tiktok.com/@lucciamv1/video/7173015261623225642?is_copy_url=1&is_from_webapp=v1
            tiktok_list = link.split("https://www.tiktok.com/@")
            #print("tiktok_list", tiktok_list)
            
            tiktok_base_url = tiktok_list[1]
            #print("tiktok_base_url", tiktok_base_url)
            
            username_video_split = tiktok_list[1].split("/video/")
            username = username_video_split[0]
            #print("username", username)
            
            tiktok_video_file_id = username_video_split[1].split("?")[0] # this seems to be in the videos, i could imagine it leading to problems   
            #print("tiktok_video_file_id", tiktok_video_file_id)
            
            # REPLACE THE TEMPLATE
            tiktok_template = tiktok_template.replace("LOCATION_FOR_TIKTOK_UPLOADER_USERNAME", username)
            tiktok_template = tiktok_template.replace("LOCATION_FOR_TIKTOK_UPLOADER_VIDEO_ID", tiktok_video_file_id)
            
            link = tiktok_template
            
            # print(F"FINAL LINK", link) 
            #exit()

        
        elif "youtube" in link:
            if "list" in link: # check if if it's a playlist or any other ways youtube can be fucked about with
                return link
            
            #print("THIS IS A YOUTUBE VIDEO")
            youtube_template = '''
            <iframe width="560" height="315" src="https://www.youtube.com/embed/YOUTUBE_FILE_ID" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
            <!--PROPERLY EMBEDDED HTML TAG-->
            '''
            
            link_without_watch = link.split("watch?v=")
            #print("link_without_watch", link_without_watch)
            
            youtube_file_id = link_without_watch[1]
            #print("youtube_file_id", youtube_file_id)
            
            youtube_template = youtube_template.replace("YOUTUBE_FILE_ID", youtube_file_id)
            link = youtube_template

        # print("FINAL", link)
        return link
    except Exception as e:
        log_function("error", str(e), function_name=F"{inspect.stack()[0][3]}")
        return link  
    
def clean_title(Post_title):
    return "title of post" 

def clean_description(Post_description):
    return "description of post" 



def load_default_profile_pic():
    #img = PImage.open(path)
    #return img
    path = "/root/mansura/files/profile_demo.jpg"
    pic = open(path, 'rb').read()

    return pic

if __name__ == "__main__":
    print_title(F"{inspect.stack()[0][3]}")
    # load_default_profile_pic()



