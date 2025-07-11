#include <fstream>
#include <opencv2/opencv.hpp>

#include "filesystem_include.h"
#include "lane_detector.h"

using namespace std;
using namespace cv;

int main(int argc, char** argv) {

    std::string input_folder = "../input_folder";
    std::string output_folder = "output_folder";
    std::string video_file_path ="../lane_line.mp4";
    fs::create_directory(output_folder);

    cout << "Input folder: " << input_folder << endl;

    LaneDetector lane_detector;
    cv::Mat lane_line_mask;
    cv::Mat detected_line_img;
    cv::Mat reduced_line_img;
    cv::Mat dst;
    bool lane_departure;
    using namespace std::chrono;
    double total_time = 0;
    size_t n_images = 0;
    double alpha = 0.5;
    double beta = 1.0 - alpha;
    VideoCapture cap(video_file_path);

    cv::namedWindow("CSI Camera", cv::WINDOW_AUTOSIZE);

    while(true) {
        n_images += 1;
        cv::Mat input_img;
        cap >> input_img;
        auto start = high_resolution_clock::now();

        //cv::Mat output_mask = lane_detector.getLaneMask(input_img);
        std::vector<LaneLine> detected_lines = lane_detector.detectLaneLines(input_img, lane_line_mask, detected_line_img, reduced_line_img, lane_departure);

        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        long long int execution_time = duration.count();
        double milliseconds = 0.001 * execution_time;
        total_time += milliseconds;

        // cv::Mat output_img = cv::Mat::zeros(input_img.size(), CV_8UC1);
        // output_img.setTo(Scalar(255), output_mask > 0.5);
        //cv::addWeighted(input_img, alpha, reduced_line_img, beta, 0.0, dst);
        cv::imshow("CSI Camera",lane_line_mask);
        int keycode = cv::waitKey(30) & 0xff ; 
        if (keycode == 27) break ;
        
    }

    return 0;
}