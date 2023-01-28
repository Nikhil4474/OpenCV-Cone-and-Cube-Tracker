package frc.robot;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;
import org.opencv.videoio.VideoCapture;
import java.util.*;
import org.opencv.imgproc.Moments;

public class ObjectTracking {

    public static void main(String[] args) {
        // Load the OpenCV library
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

        // Create a new video capture object
        VideoCapture cap = new VideoCapture("Coen.mp4");

        // Check if the video capture object is opened correctly
        if (!cap.isOpened()) {
            System.out.println("Error opening video capture");
            return;
        }

        // Create a new frame
        Mat frame = new Mat();

        // Main loop
        while (true) {
            // Read a new frame from the video capture
            cap.read(frame);

            // Convert the frame to HSV color space
            Mat hsv = new Mat();
            Imgproc.cvtColor(frame, hsv, Imgproc.COLOR_BGR2HSV);

            // Define the range of colors for the orange cone
            Scalar lower_orange = new Scalar(10, 100, 100);
            Scalar upper_orange = new Scalar(25, 255, 255);

            // Define the range of colors for the purple cube
            Scalar lower_purple = new Scalar(140, 100, 100);
            Scalar upper_purple = new Scalar(160, 255, 255);

            // Create a mask for the orange cone
            Mat orange_mask = new Mat();
            Core.inRange(hsv, lower_orange, upper_orange, orange_mask);

            // Create a mask for the purple cube
            Mat purple_mask = new Mat();
            Core.inRange(hsv, lower_purple, upper_purple, purple_mask);

            // Find the contours in the orange mask
            List<MatOfPoint> orange_contours = new ArrayList<>();
            Imgproc.findContours(orange_mask, orange_contours, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);

            // Find the largest orange contour
            double max_orange_area = 0;
            MatOfPoint orange_cone = null;
            for (MatOfPoint contour : orange_contours) {
                double area = Imgproc.contourArea(contour);
                if (area > max_orange_area) {
                    max_orange_area = area;
                    orange_cone = contour;
                }
            }

            // Draw the orange contour on the frame
            Imgproc.drawContours(frame, Arrays.asList(orange_cone), -1, new Scalar(0, 255, 0), 2);

            // Compute the center of the orange cone
            Moments orange_moments = Imgproc.moments;

            // Compute the center of the orange cone
            Moments orange_moments = Imgproc.moments(orange_cone);
            Point orange_center = new Point();
            orange_center.x = orange_moments.get_m10() / orange_moments.get_m00();
            orange_center.y = orange_moments.get_m01() / orange_moments.get_m00();

            // Draw the center of the orange cone on the frame
            Imgproc.circle(frame, orange_center, 3, new Scalar(0, 0, 255), -1);

            // Find the contours in the purple mask
            List<MatOfPoint> purple_contours = new ArrayList<>();
            Imgproc.findContours(purple_mask, purple_contours, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);

            // Find the largest purple contour
            double max_purple_area = 0;
            MatOfPoint purple_cube = null;
            for (MatOfPoint contour : purple_contours) {
                double area = Imgproc.contourArea(contour);
                if (area > max_purple_area) {
                    max_purple_area = area;
                    purple_cube = contour;
                }
            }

            // Draw the purple contour on the frame
            Imgproc.drawContours(frame, Arrays.asList(purple_cube), -1, new Scalar(255, 0, 0), 2);

            // Compute the center of the purple cube
            Moments purple_moments = Imgproc.moments(purple_cube);
            Point purple_center = new Point();
            purple_center.x = purple_moments.get_m10() / purple_moments.get_m00();
            purple_center.y = purple_moments.get_m01() / purple_moments.get_m00();

            // Draw the center of the purple cube on the frame
            Imgproc.circle(frame, purple_center, 3, new Scalar(255, 0, 0), -1);

            // Compute the position and angle of the orange cone relative to the camera
            double orange_angle = Math.atan2(orange_center.y - frame.rows() / 2, orange_center.x - frame.cols() / 2);
            double orange_distance = Math.sqrt(Math.pow(orange_center.x - frame.cols() / 2, 2) + Math.pow(orange_center.y - frame.rows() / 2, 2));

            // Compute the position and angle of the purple cube relative to the camera
            double purple_angle = Math.atan2(purple_center.y - frame.rows() / 2, purple_center.x - frame.cols() / 2);
            double purple_distance = Math.sqrt(Math.pow(purple_center.x - frame.cols() / 2, 2) + Math.pow(purple_center.y - frame.rows() / 2, 2));

            // Print the position and angle of the orange cone and purple cube
            // Print the position and angle of the orange cone and purple cube
            System.out.println("Orange cone angle: " + orange_angle + " Orange cone distance: " + orange_distance);
            System.out.println("Purple cube angle: " + purple_angle + " Purple cube distance: " + purple_distance);

            // Show the frame with the orange cone and purple cube detections
            imshow("Frame", frame);
            // Wait for a key press before continuing to the next frame
            if (waitKey(30) >= 0) break;
        }
    }
}
