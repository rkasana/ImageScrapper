# Import the necessary libraries
from flask_cors import CORS, cross_origin
from imagesscrapperservice.ImageScrapperService import ImageScrapperService
from imagesscrapper.ImageScrapper import ImageScrapper
# from imagesscrapper import ImageScrapper
from flask import Flask, render_template, request, jsonify, url_for

# Initialize the flask app
app = Flask(__name__, static_folder='static',template_folder='template')


# Create the routes to redirect the control inside the application itself
# 1. The route for redirecting to home page
@app.route('/', methods=['GET'])  # route for redirecting to the home page
@cross_origin()
def home():
    return render_template('index.html')


# 2. Showing the images on the screen once our parser successfully gives the list of images
@app.route('/showImages')  # route to show the images on a web page
@cross_origin()
def show_images():
    scrapper_object = ImageScrapper()  # Instantiating the object of class ImageScrapper
    list_of_jpg_files = scrapper_object.list_only_jpg_files('static')  # obtainig the list of image files from the images folder
    print(list_of_jpg_files)
    print("Length is", len(list_of_jpg_files))
    try:
        if len(list_of_jpg_files) > 0:  # if there are images present, show them
            return render_template('showImage.html', show_images=list_of_jpg_files)
        else:
            return "Please try with a different keyword"
    except Exception as e:
        print("no images found", e)
        return "Please try with diffrent keyword"


# 3. Show the images to the user
@app.route('/searchImages', methods=['GET', 'POST'])
def searchImages():
    if request.method == 'POST':
        print("entered post")
        keyword = request.form['keyword']  # assigning the value of the input keyword to the variable keyword
    else:
        print("did not enter post")
    print("printing=" + keyword)

    scraper_object = ImageScrapper()  # instantiating the class
    list_of_jpg_files = scraper_object.list_only_jpg_files('static')  # obtain the list of image files from images folder
    scraper_object.delete_existing_image(list_of_jpg_files)  # delete the old image files stored from the previous search
    # split and combine the keyword for a string containing multiple words
    image_name = keyword.split()
    image_name = '+'.join(image_name)
    print(image_name)

    # add the header metadata
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                            "43.0.2357.134 Safari/537.36"}

    service = ImageScrapperService  # instantiate the object of class ImageScrapperService
    masterListOfImages = service.downloadImages(keyword, header)  # getting the master list from keyword
    imageList = masterListOfImages[0]  # extract the list of images from the master list
    imageTypeList = masterListOfImages[1]  # extract the list of type of images from the masterlist

    response = "We have downloaded", len(imageList), "images of " + image_name + "for you"
    return show_images()  # redirect the control to the show images method'


@app.route('/api/showImages', methods=['GET', 'POST'])  # route to return the list of file locations for API calls
@cross_origin()
def get_image_url():
    if request.method == 'POST':
        print("entered post")
        keyword = request.json['keyword']  # assign the value of the input keyword to the variable keyword

    else:
        print("did not enter post")
    print('printing= ' + keyword)
    # split and combine the keyword for a string containing multiple words
    image_name = keyword.split()
    image_name = '+'.join(image_name)

    # adding the header metadata
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    service = ImageScrapperService  # Instantiate the  object of class ImageScrapperService
    url_enum = service.get_image_urls(keyword, header)
    # getting the URL enumeration
    url_list = []  # initialize empty url list
    for i, (img, Type) in enumerate(url_enum[0:5]):
        # create key value pairs of  image URLs to be sent as json
        dict = {'image_url': img}
        url_list.append(dict)
    return jsonify(url_list)  # send the url list in JSON format


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)  # running the app on local machine 8000
    # app.run(debug=True)
