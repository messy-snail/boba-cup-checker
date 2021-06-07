#include "CamManager.h"
using namespace rainbow::vision;
CamManager::CamManager()
{

}

bool CamManager::Open()
{
    capture_.open(0);

    if (!capture_.isOpened()) {
        cout << "Error : Cam open"<<endl;
        return false;
    }

//    bool bWidth = capture_.set(CAP_PROP_FRAME_WIDTH, CAM_WIDTH);
//    bool bHeight = capture_.set(CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT);

//    capture_.set(CAP_PROP_AUTOFOCUS, false);
//    capture_.set(CAP_PROP_AUTO_EXPOSURE, false);
//    capture_.set(CAP_PROP_AUTO_WB, false);


//    bool bCondition = bWidth & bHeight;
//    if (bCondition) {
//        return true;
//    }
//    else {
//        return false;
//    }
    return true;
}

bool CamManager::Run()
{
    while(true){
        if (!capture_.read(frame_)) {
            return false;
        }
        imshow("frame", frame_);
    }

    return true;
}
