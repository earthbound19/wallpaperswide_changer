import commands
import urllib2
import os
from random import choice
from bs4 import BeautifulSoup


website = "http://wallpaperswide.com"
directory = "/home/ed/Downloads/"
resolution = "3840x1080"
url = urllib2.urlopen(website + "/" + resolution + "-wallpapers-r.html")


def get_pagination(url):
    code = url.read()
    soup = BeautifulSoup(code)
    num_listas = []

    for numbers in soup.find_all('div', {'class': 'pagination'}):
        num_listas.append(numbers.find_all('a'))

    tag = num_listas[0][-2]
    highest_number = tag.next_element
    pagination_list = [x for x in xrange(int(highest_number) + 1)]
    get_all_images(choice(pagination_list))


def get_all_images(pagination):
    if pagination == 0 or pagination == 1:
        url = urllib2.urlopen(website + "/" + resolution +
                              "-wallpapers-r.html")
    else:
        url = urllib2.urlopen(website + "/" + resolution +
                              "-wallpapers-r/page/" + str(pagination))
    code = url.read()
    soup = BeautifulSoup(code)
    all_wall = soup.find_all("li", {'class': 'wall'})
    soup = BeautifulSoup(str(all_wall))
    links = []
    for link in soup.findAll('a'):
        img_url = link.get('href')
        if img_url not in links:
            links.append(img_url)
    img_full_url = website + choice(links)
    download_image(img_full_url)


def download_image(img_full_url):
    url = urllib2.urlopen(img_full_url)
    html_code = url.read()
    soup = BeautifulSoup(html_code)
    for link in soup.find_all(id="wallpaper-resolutions"):
        for downloadable_link in link.find_all('a'):
            if resolution in downloadable_link.get('href'):
                full_image_url = urllib2.urlopen(website +
                                                downloadable_link.get('href'))
                output = full_image_url.read()
                image_out = open(directory +
                                 downloadable_link.get('href').strip(
                                                        "/download/"), "wb")
                image_out.write(output)
                image_out.close()
                abs_path = os.path.abspath(image_out.name)
                set_wallpaper(abs_path)
                break


def set_wallpaper(path_to_img):
    command = "gsettings set org.gnome.desktop.background picture-uri file://" + path_to_img
    status, output = commands.getstatusoutput(command)

if __name__ == '__main__':
    get_pagination(url)
