#ifndef CAMMANAGER_H
#define CAMMANAGER_H
#include "VisionCommon.h"

namespace rainbow {
    namespace vision {
        class CamManager
        {
        public:
            CamManager();
            bool Open();
            bool Run();

        private:
            VideoCapture capture_;
            Mat frame_;
        };
    }
}


#endif // CAMMANAGER_H
