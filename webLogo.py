from google.cloud import vision
import io
def detect_logos():
    """Detects logos in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()
    #path = './naver2.png'
    path = './google.jpeg'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_logos()