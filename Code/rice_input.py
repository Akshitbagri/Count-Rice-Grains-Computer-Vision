import cv2
import numpy as np

#Creating A function which Returns string Full if the ratio is greater than 2.1 and Returns string Broken if the Ratio is in
#Between Range 1 and 2.1
def get_classificaton(ratio):
	ratio =round(ratio,1)
	toret=""
	if(ratio>=2.1):
		toret="Full"
	elif(ratio>=1 and ratio<2.1):
		toret="Broken"
	toret="("+toret+")"
	return toret
#Loads the image in greyscale mode
img_name = input("Enter Image name with its format(img_name.jpg):")
img = cv2.imread(img_name,0)

#Converts the Image into Binary
ret,binary = cv2.threshold(img,160,255,cv2.THRESH_BINARY)

#Averaging Filter
kernel = np.ones((5,5),np.float32)/9
# -1 : depth of the destination image
dst = cv2.filter2D(binary,-1,kernel)


kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

#erosion
erosion = cv2.erode(dst,kernel2,iterations = 1)

#dilation 
dilation = cv2.dilate(erosion,kernel2,iterations = 1)

#edge detection
edges = cv2.Canny(dilation,100,200)

# Size detection
contours,hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print ("No. of rice grains=",len(contours))
total_ar=0
count = 0
for cnt in contours:
	x,y,w,h = cv2.boundingRect(cnt)
	aspect_ratio = float(w)/h
	if(aspect_ratio<1):
		aspect_ratio=1/aspect_ratio
	if(aspect_ratio<2.1):
		count = count+1
	total_ar+=aspect_ratio
avg_ar=total_ar/len(contours)
percentage_broken_rice = (count/len(contours))*100
print("Percentage of Broken Rice=", round(percentage_broken_rice, 2)) 

#Credits to Open source Code https://bit.ly/2QP6rdo
