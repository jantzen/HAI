import videoTest
from bot import Bot


greyscale = cv2.cvtColor(frame.array, cv2.COLOR_BGR2GRAY)

mask_right = np.zeros(frame.array.shape, dtype="uint8")
mask_center = np.zeros(frame.array.shape, dtype="uint8")
mask_left = np.zeros(frame.array.shape, dtype="uint8")

cv2.rectangle(mask_right, 
cv2.rectangle(mask_center,
cv2.rectangle(mask_left,

masked_right = cv2.bitwise_and(frame.array, frame.array, mask = mask_right)
masked_center = cv2.bitwise_and(frame.array, frame.array, mask = mask_center)
masked_left = cv2.bitwise_and(frame.array, frame.array, mask = mask_left)



hist_right = cv2.calcHist([masked],[0],mask_right,[256],[0,256])
hist_center = cv2.calcHist([masked],[0],mask_center,[256],[0,256])
hist_left = cv2.calcHist([masked],[0],mask_left,[256],[0,256])


cv2.imshow("Gray image", gray)
