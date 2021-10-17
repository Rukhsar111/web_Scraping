import os
import time
import requests
from selenium import webdriver



def fetch_image_urls(query: str, max_link_tofetch : int, wd: webdriver, sleep_between_interactions: int= 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)


    search_url= "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    wd.get(search_url.format(q=query))

    image_url=set()
    image_count=0
    result_start=0

    while image_count< max_link_tofetch:
        scroll_to_end(wd)

        # get all the thumbnails results
        thumbnail_results=wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results=len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {result_start}:{number_results}")

        # try to click every thumbnail such that  we can get real image behind it
        for img in thumbnail_results[result_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue


        #extract images  url

            actual_images=wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_url.add(actual_image.get_attribute('src'))



            image_count=len(image_url)

            if len (image_url) >= max_link_tofetch:
                print(f'Found:{len(image_url)} image links, done!')
                break

        else:
             print("Found:", len(image_url), "image links, looking for more ...")
             time.sleep(30)
             return

             load_more_button = wd.find_element_by_css_selector(".mye4qd")
             if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        result_start=len(thumbnail_results)

    return image_url



def persist_image(folder_path: str, url: str, counter):
    try:
        image_content=requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")





def search_and_download(search_term : str ,driver_path : str,  number_of_images= 10, target_path='./images'):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))


    if not os.path.exists(target_folder):
        os.makedirs(target_folder)


     # opening the chrome browser
    with webdriver.Chrome(executable_path=driver_path, )as wd:
        res=fetch_image_urls(search_term, number_of_images, wd=wd , sleep_between_interactions=0.5)



    counter=0
    for ele in res:
        persist_image(target_folder, ele , counter)
        counter += 1




#New  my  chrom version 94.0.4606.81
# my chrome version is Version 92.0.4515.159



Driver_path='./chromedriver.exe'
search_term='flower'

number_of_images=10
search_and_download(search_term= search_term, driver_path=Driver_path, number_of_images=10 )