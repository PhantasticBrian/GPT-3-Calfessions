from google.cloud import vision
import json


def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web."""

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print("Texts:")

    for text in texts:
        # print('\n"{}"'.format(text.description))

        vertices = [
            "({},{})".format(vertex.x, vertex.y)
            for vertex in text.bounding_poly.vertices
        ]

        # print("bounds: {}".format(",".join(vertices)))
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return [text.description for text in texts[1:]]


def get_text(uri):
    text = detect_text_uri(uri)
    len_text = len(text)
    if len_text < 3:
        return None
    elif text[0:3] == ["CALFESSION", "CAL", "CONFESSION"]:
        text = text[3:]
    elif text[-1] == "CALFESSION":
        text = text[:-1]
    else:
        return None
    return text


posts_file = open("posts.json", "r")
posts_content = posts_file.read()
posts_uris = [item["value"] for item in json.loads(posts_content)]

confessions = []


def write_confessions():
    confessions_file = open("confessions.json", "w")
    confessions_file.write(json.dumps(confessions))
    confessions_file.close()


num_posts = len(posts_uris)
for index, uri in enumerate(posts_uris):
    print(index + 1, "/", num_posts, ":", uri)
    text = get_text(uri)
    if text:
        confessions.append(" ".join(text))
    if index % 10 == 0:
        write_confessions()
write_confessions()

"""
/** Jank browser console scraper code: */
// Create new set
stuff = new Set()

// Append confession image URIs
fields = document.getElementsByClassName("FFVAD")
for (var i = 0; i < fields.length; i++) {
    uris.add(stuff[i].getAttribute("src"))
}
window.scrollBy(0, 3000)
"""
