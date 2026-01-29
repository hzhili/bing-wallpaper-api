import settings
import requests
import utils
import time
def main():
    for region_type in settings.LOCATION:
        response = requests.get(settings.BING_API_TEMPLATE.format(1, region_type))
        data = response.json()
        images = []
        for index in range(len(data['images'])):
            item = data['images'][index]          
            image ={}
            image['title'] = item['title']
            image['url'] = settings.BING_BASE_URL + item['url'].replace("&rf=LaDigue_1920x1080.jpg&pid=hp","")
            image['startdate'] = time.strftime("%Y-%m-%d", time.strptime(item['startdate'], "%Y%m%d"))
            image['enddate'] = time.strftime("%Y-%m-%d", time.strptime(item['enddate'], "%Y%m%d"))
            image['copyright'] = item['copyright']
            image['copyrightlink'] = item['copyrightlink']
            if index == 0:
                utils.writer_today(region_type,image)
            images.append(image)
        # utils.append_json(region_type, images)
if __name__ == '__main__':
    main()