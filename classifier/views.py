from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
import shutil
import cv2
import os
from django.core.files.base import ContentFile

# Create your views here.


class FaceClassifier(APIView):
	
	# def get(self, request): 
	# 	stocks = Stock.objects.all() 
	# 	serializer = StockSerializer(stocks, many=True) 
	# 	return Response(serializer.data) 
	
	def post(self, request):

		emotions = ["angry", "happy", "sad", "neutral"]
		img = request.FILES['image'].name
		
		#edited here
		#image = cv2.imread(img, 0)
		print(img)
		print(str(request.FILES['image'].size))
		BASE_PATH = 'Images/'
		# f= open("guru.jpg","w+")
		# f.close()
		
		print("shape")
		# print(image.shape)
		# cv2.imwrite(''+img,image)
		# shutil.copy(img,"guru.jpg")
		folder = ""
		try:
			print("try")
			os.mkdir(os.path.join(BASE_PATH, folder))
		except:
			print("except")
			pass

		# save the uploaded file inside that folder.
		full_filename = os.path.join(BASE_PATH, folder, img)
		fout = open(full_filename, 'wb+')
		# Iterate through the chunks.
		file_content = ContentFile( request.FILES['image'].read() )
		for chunk in file_content.chunks():
			fout.write(chunk)
		fout.close()
		
		image = cv2.imread("Images/"+img, 0)
		height, width = image.shape[:2]
		print(str(height)+"-"+str(width))
		
		#edit complete
		
		facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
		fishface = cv2.face.FisherFaceRecognizer_create()
		# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
		image = clahe.apply(image)

		face = facecascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=15, minSize=(10, 10), flags=cv2.CASCADE_SCALE_IMAGE)
		
		for (x, y, w, h) in face:
			faceslice = image[y:y+h, x:x+w]
			faceslice = cv2.resize(faceslice, (350, 350))
		try:
			fishface.read("trained_emoclassifier.xml")
			# print("loaded")
		except:
			return Response('NOT DONE', status=status.HTTP_201_CREATED)
			# print("no xml found. Using --update will create one.")
		pred, conf = fishface.predict(faceslice)
		os.remove("Images/"+img)
		return Response(emotions[pred], status=status.HTTP_201_CREATED)

