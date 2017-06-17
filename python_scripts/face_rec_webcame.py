import face_recognition
import cv2
import pyrebase
import urllib
import thread

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


names = ["Varun"]

# Load a sample picture and learn how to recognize it.
varun_image = face_recognition.load_image_file("varun")
varun_face_encoding = face_recognition.face_encodings(varun_image)[0]
# second_image = face_recognition.load_image_file("peter2.png")
# second_face_encoding = face_recognition.face_encodings(second_image)[0]

# store face encodings in an array
known_encodings = [varun_face_encoding]


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# configure firebase
config = {
  "apiKey": "AIzaSyDoGaO58eRibD1--3xVXLJz9a4o_Xfnv3s",
  "authDomain": "hacking-for-gooooooood.firebaseapp.com",
  "databaseURL": "https://hacking-for-gooooooood.firebaseio.com/",
  "storageBucket": "hacking-for-gooooooood.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


# stream real time data
def stream_handler(message):
    print("got a message")
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI

    if message["data"]:

        data = message["data"]
        print(data)
        if type(data) is dict:
            if "mediaURL" in data:
                print("SINGLE ITEM")
                mediaURL = str(data["mediaURL"])
                name = str(data["name"])
                print(mediaURL, name)
                urllib.urlretrieve(mediaURL, name)
                names.append(name)
                known_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(name))[0])
                
                
            else:
                print("MULTIPLE ITEMS")

                for key,value in data.items():
                    mediaURL = str(value["mediaURL"])
                    name = str(value["name"])
                    print(mediaURL, name)
                    urllib.urlretrieve(mediaURL, name)
                    names.append(name)
                    print(names)
                    known_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(name))[0])
                    
                    
                    # encode image into array
                    # add name to array
        else:
            print("data is not a dictttt")
    else:
        print("NO DATA LOL")



def startStream():
    db.child("test").stream(stream_handler)

thread.start_new_thread(startStream, ())
# my_stream = db.child("test").stream(stream_handler)



while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            for i in range(len(match)):
                if match[i]:
                    name = names[i]
            # if match[0]:
            #     name = "Varun"
            # if match[1]:
            #     name = "Peter"

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (254,110,111), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (254,110,111), -1)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()