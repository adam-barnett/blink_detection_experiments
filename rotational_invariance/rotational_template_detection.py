import cv2
import math
import os


"""

"""

class RotationalTester():
    def __init__(self):      
        video_src = 0
        self.cam = cv2.VideoCapture(video_src)
        self.eyes_image = cv2.imread('eyes.png', 0)
        self.save_count = 0
        self.current_angle = 0
        self.angles = [0,5, -5]#[0,2,-2]#,5,-5]#,10,-10, 15, -15, 20, -20, 25, -25, 30, -30,
                       #35, -35, 40, -40, 45, -45]
        self.modifiers_used = [[],[]]
        self.COMP_METHOD = 'cv2.TM_CCOEFF_NORMED'
        self.prev_loc = None

    def rotate_image(self, image, angle):
        if angle == 0: return image
        height, width = image.shape[:2]
        rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, (width, height),
                                flags=cv2.INTER_LINEAR)
        return result

    def set_angle(self, image):
        method = eval(self.COMP_METHOD)
        results = []
        max_val = 0.0
        max_ang = 0
        max_loc = (0,0)
        vals = []
        for angle_mod in self.angles:
            angle_test = self.current_angle + angle_mod
            rot = self.rotate_image(image, angle_test)
            matches = cv2.matchTemplate(rot,self.eyes_image,method)
            _, val, _, loc = cv2.minMaxLoc(matches)
            vals.append(val)
            if val > max_val:
               max_val = val
               max_loc = loc
               max_ang = angle_mod
        self.current_angle = self.current_angle + max_ang
        self.modifiers_used[0].append(max_ang)
        self.modifiers_used[1].append(max_val)
        self.prev_loc = max_loc
        return max_loc

    def Run(self):
        while True:
            ret, img = self.cam.read()
            if ret:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                eyes_loc = self.set_angle(gray)
                if eyes_loc != (0,0):
                    gray_rot = self.rotate_image(gray, self.current_angle)
                    cv2.rectangle(gray_rot, eyes_loc, (eyes_loc[0] +
                                                       self.eyes_image.shape[1],
                                                       eyes_loc[1] +
                                                       self.eyes_image.shape[0]),
                                                      (255,0,0), 2)
                    eye_capt = gray_rot[eyes_loc[1]:eyes_loc[1] +
                                        self.eyes_image.shape[0],
                                        eyes_loc[0]:eyes_loc[0] +
                                        self.eyes_image.shape[1]]
                    cv2.imshow('eyes_found', eye_capt)
                    save_loc = os.path.join('eyes_from_rotations',
                                                'eyes%d.png'
                                                % self.save_count)
                    self.save_count += 1
                    cv2.imwrite(save_loc, eye_capt)
                    cv2.imshow('current_face_detection', gray_rot)
                else:
                    cv2.imshow('current_face_detection', gray)
                key_press = cv2.waitKey(20)
                if key_press == 27:
                    print 'closing'
                    cv2.destroyAllWindows()
                    self.cam.release()
                    break

            else:
                cam.release()
                break

        print 'angle modifications:'
        print self.modifiers_used

    def Close(self):
        cv2.destroyAllWindows()
        self.cam.release()
                            

if __name__ == "__main__":


    tester = RotationalTester()
    test_img = cv2.imread('face.png', 0)
    tester.Run()

