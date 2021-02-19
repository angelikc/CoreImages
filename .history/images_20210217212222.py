
# 
# %%
import glob
import cv2
import os.path
import numpy as np
import matplotlib.pyplot as plt



# %%
cores_per_image = 6

uvFiles = glob.glob('./*.jpg')
# Picture path
img = cv2.imread(uvFiles[0])
a = []
b = []

# %%


def oneventlbuttondown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 10, (0, 0, 255), thickness=-1)
        #        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)


core_length = 3
vc = []
do = int(uvFiles[0][2:6])
dn = int(uvFiles[0][7:11])

for i in range(cores_per_image):
    if i == 0:
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("output", 400, 300)

        cv2.setMouseCallback("image", oneventlbuttondown)
        cv2.imshow("image", img)
        print(
            'Click 1) left upper corner 2) right lower corner in leftmost core and 3) leftupper corner in second core')
        cv2.waitKey(0)
        y = b[0];
        x = a[0];
        dy = b[1] - b[0];
        dx = a[1] - a[0]
        gap = a[2] - a[1]

    if i == 3:
        midgap = gap * 4
    else:
        midgap = 0
    if i > 0: x = x + (dx + gap) + midgap

    crop_img = img[y:y + dy, x:x + dx]
    if i == 0:
        vc = crop_img
    else:
        vc = cv2.vconcat([vc, crop_img])

    crop_name = str(int(uvFiles[0][2:6]) + (core_length * i)) + ".jpg"

    path = os.path.join(os.path.relpath('Cropped', start=os.curdir), crop_name)
    cv2.imwrite(path, crop_img)

concat_name = uvFiles[0][2:6] + "-" + uvFiles[0][7:11] + ".jpg"
path = os.path.join(os.path.relpath('Cropped', start=os.curdir), concat_name)
cv2.imwrite(path, vc)
p = vc.shape
vc_gray = cv2.cvtColor(vc, cv2.COLOR_BGR2GRAY)

print(vc.shape)  # Dimensions of Image
print(vc_gray.shape)  # It is already a numpy array

print(type(vc_gray))

# print(p[:10, :10, 1 ])

img_log = np.average(vc_gray[:, 80:120], axis=1)
depths = np.arange(do, dn, (dn - do) / len(img_log))

plt.figure()
# plt.subplot(1, 2, 1)
plt.subplot2grid((1, 10), (0, 0), colspan=3)
plt.plot(img_log, depths, 'green');
plt.axis([0, 120, do, dn]);
plt.gca().invert_yaxis();
plt.gca().invert_xaxis()
# plt.subplot(1, 2 ,2)
plt.subplot2grid((1, 10), (0, 3), colspan=7)
plt.imshow(vc_gray[:, 40:120], aspect='auto', origin='upper');
plt.colorbar()
p_50 = np.percentile(img_log, 50)

plt.show()
